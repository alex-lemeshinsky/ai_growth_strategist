"""
Background task service for parsing and analyzing competitor ads.
"""
import json
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from src.db import MongoDB, Task, TaskStatus, CreativeAnalysis, AggregatedAnalysis
from src.services.apify_service import ApifyService
from src.analysis.video_analyzer import analyze_video_file
import httpx

logger = logging.getLogger(__name__)

# Cache directory
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache" / "videos"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


async def parse_ads_task(task_id: str, url: str, max_results: int = 15, auto_analyze: bool = True):
    """
    Background task: Parse ads from Facebook Ads Library.
    """
    db = MongoDB.get_db()
    
    try:
        # Update status
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {"status": TaskStatus.PARSING, "updated_at": datetime.utcnow()}}
        )
        
        # Extract ads
        apify_service = ApifyService()
        raw_ads = await apify_service.extract_ads_from_url(url, max_results, True)
        
        if not raw_ads:
            await db.tasks.update_one(
                {"task_id": task_id},
                {"$set": {
                    "status": TaskStatus.FAILED,
                    "error": "No video ads found after filtering",
                    "updated_at": datetime.utcnow()
                }}
            )
            logger.warning(f"⚠️ Task {task_id}: No video ads found after filtering")
            return
        
        # Count video ads
        video_count = 0
        for ad in raw_ads:
            snapshot = ad.get('snapshot', {})
            if (snapshot.get('videos') and len(snapshot.get('videos', [])) > 0) or \
               any(card.get('video_hd_url') or card.get('video_sd_url') 
                   for card in snapshot.get('cards', [])):
                video_count += 1
        
        logger.info(f"🎥 Found {video_count}/{len(raw_ads)} video ads after filtering")
        
        # Save to creatives file
        page_name = raw_ads[0].get("page_name", "unknown") if raw_ads else "unknown"
        page_id = raw_ads[0].get("page_id", "unknown") if raw_ads else "unknown"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{page_name}_{page_id}_{timestamp}.json"
        filepath = Path("creatives") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "extraction_metadata": {
                    "url": url,
                    "extracted_at": datetime.now().isoformat(),
                    "total_ads": len(raw_ads),
                    "page_name": page_name,
                    "page_id": page_id
                },
                "ads": raw_ads
            }, f, indent=2, ensure_ascii=False)
        
        # Update task
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": TaskStatus.PARSED,
                "page_name": page_name,
                "page_id": page_id,
                "total_ads": len(raw_ads),
                "creatives_file": str(filepath),
                "updated_at": datetime.utcnow()
            }}
        )
        
        logger.info(f"✅ Task {task_id}: Parsed {len(raw_ads)} ads")
        
        # Auto-trigger analysis if enabled
        if auto_analyze and len(raw_ads) > 0:
            logger.info(f"🚀 Auto-starting analysis for task {task_id}")
            import asyncio
            asyncio.create_task(analyze_creatives_task(task_id))
        
    except Exception as e:
        logger.error(f"❌ Task {task_id} failed: {e}")
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": TaskStatus.FAILED,
                "error": str(e),
                "updated_at": datetime.utcnow()
            }}
        )


def _cache_video(url: str) -> str:
    """Download and cache video."""
    import hashlib
    fname = hashlib.sha256(url.encode()).hexdigest()[:16] + ".mp4"
    path = CACHE_DIR / fname
    
    if path.exists():
        return str(path)
    
    with httpx.stream("GET", url, timeout=30.0, follow_redirects=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_bytes():
                if chunk:
                    f.write(chunk)
    return str(path)


def _pick_video_url(raw_item: Dict[str, Any]) -> str | None:
    """Extract video URL from ad item."""
    snap = raw_item.get("snapshot", {})
    for card in snap.get("cards", []) or []:
        if card.get("video_hd_url"):
            return card["video_hd_url"]
    for card in snap.get("cards", []) or []:
        if card.get("video_sd_url"):
            return card["video_sd_url"]
    for v in snap.get("videos", []) or []:
        if v.get("video_hd_url"):
            return v["video_hd_url"]
    return None


async def analyze_creatives_task(task_id: str):
    """
    Background task: Analyze creatives with video analysis + LLM aggregation.
    """
    db = MongoDB.get_db()
    
    try:
        # Get task
        task_doc = await db.tasks.find_one({"task_id": task_id})
        if not task_doc:
            raise ValueError(f"Task {task_id} not found")
        
        if task_doc["status"] != TaskStatus.PARSED:
            raise ValueError(f"Task must be in PARSED status, got {task_doc['status']}")
        
        # Update status
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {"status": TaskStatus.ANALYZING, "updated_at": datetime.utcnow()}}
        )
        
        # Load creatives
        creatives_file = task_doc.get("creatives_file")
        if not creatives_file or not Path(creatives_file).exists():
            raise ValueError("Creatives file not found")
        
        with open(creatives_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        raw_ads = data.get("ads", [])[:10]  # Limit to 10 for now
        
        # Analyze each creative
        analyses: List[CreativeAnalysis] = []
        failed_count = 0
        skipped_non_video = 0
        loop = asyncio.get_event_loop()
        
        for idx, ad in enumerate(raw_ads, 1):
            ad_id = ad.get('ad_archive_id', f'unknown_{idx}')
            try:
                logger.info(f"Analyzing creative {idx}/{len(raw_ads)}: {ad_id}")
                
                video_url = _pick_video_url(ad)
                if not video_url:
                    logger.info(f"⏭️ Skipping non-video ad {ad_id} (no video URL found)")
                    skipped_non_video += 1
                    continue
                
                # Cache video (blocking operation - run in executor)
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor() as executor:
                    cached_path = await loop.run_in_executor(
                        executor,
                        _cache_video,
                        video_url
                    )
                
                # Analyze with Gemini (blocking operation - run in executor)
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(
                        executor,
                        analyze_video_file,
                        cached_path,
                        {
                            "page_name": ad.get("page_name"),
                            "ad_archive_id": ad.get("ad_archive_id"),
                            "publisher_platform": ad.get("publisher_platform"),
                            "product_context": ad.get("title") or (ad.get("body", {}) or {}).get("text"),
                        }
                    )
                
                # Map new Performance Marketing schema to CreativeAnalysis fields
                # New prompt returns: visual_style, messaging, emotional_journey, key_insights
                visuals = result.get("visual_style")
                
                # CTA normalization
                cta_raw = result.get("cta")
                if isinstance(cta_raw, dict):
                    cta_list = [cta_raw]
                elif isinstance(cta_raw, list):
                    cta_list = cta_raw
                else:
                    cta_list = []
                
                # Messaging: extract pains and value_props from new structure
                messaging = result.get("messaging", {}) or {}
                pains_list = messaging.get("pains") or []
                pains_norm = [{"text": p.get("text") if isinstance(p, dict) else p} if not isinstance(p, dict) or "text" in p else p for p in pains_list]
                vprops_list = messaging.get("value_props") or []
                vprops_norm = [{"text": v.get("text") if isinstance(v, dict) else v} if not isinstance(v, dict) or "text" in v else v for v in vprops_list]
                
                # Storyboard: map emotional_journey to storyboard format
                storyboard = result.get("emotional_journey") or result.get("storyboard", [])
                
                # Scores remain the same
                scores = result.get("scores")
                
                # Summary: use key_insights for richer summary, fallback to summary field
                key_insights_data = result.get("key_insights") or {}
                if key_insights_data:
                    # Create enriched summary from key_insights
                    main_strat = key_insights_data.get("main_strategy", "")
                    insights_list = key_insights_data.get("key_insights", [])
                    hypotheses = key_insights_data.get("hypotheses_to_test", [])
                    
                    summary_parts = []
                    if main_strat:
                        summary_parts.append(f"**Стратегія:** {main_strat}")
                    if insights_list:
                        summary_parts.append("**Інсайти:** " + "; ".join(insights_list[:2]))
                    if hypotheses:
                        summary_parts.append("**Гіпотези:** " + "; ".join(hypotheses[:2]))
                    
                    summary = " | ".join(summary_parts) if summary_parts else result.get("summary")
                else:
                    summary = result.get("summary")
                
                # Create analysis object
                analysis = CreativeAnalysis(
                    creative_id=ad.get("ad_archive_id"),
                    ad_archive_id=ad.get("ad_archive_id"),
                    page_name=ad.get("page_name"),
                    hook=result.get("hook"),
                    visual_style=visuals,
                    on_screen_text=result.get("on_screen_text", []),
                    product_showcase=result.get("product_showcase"),
                    cta=cta_list,
                    pains=pains_norm,
                    value_props=vprops_norm,
                    audio=result.get("audio"),
                    storyboard=storyboard,
                    scores=scores,
                    summary=summary,
                    video_url=video_url,
                    cached_video_path=cached_path,
                    analyzed_at=datetime.utcnow()
                )
                
                analyses.append(analysis)
                logger.info(f"✅ Successfully analyzed creative {ad_id}")
                
            except Exception as e:
                logger.error(f"❌ Error analyzing {ad_id}: {e}")
                failed_count += 1
                # Continue with other creatives
                continue
        
        logger.info(f"📊 Analysis summary: {len(analyses)} successful, {failed_count} failed, {skipped_non_video} skipped (non-video)")
        
        if not analyses:
            raise ValueError(f"No creatives could be analyzed. All {len(raw_ads)} attempts failed.")
        
        # Aggregate analysis with LLM (with fallback)
        aggregated = None
        aggregation_error = None
        try:
            aggregated = await _aggregate_analysis(analyses)
            logger.info(f"✅ Aggregation completed successfully")
        except Exception as e:
            logger.warning(f"⚠️ Aggregation failed, but saving individual analyses: {e}")
            aggregation_error = str(e)
        
        # Generate HTML report
        html_report = None
        try:
            from src.utils.html_report import generate_html_report
            
            task_data = {
                "page_name": task_doc.get("page_name"),
                "total_ads": task_doc.get("total_ads"),
            }
            
            creatives_data = [a.model_dump() for a in analyses]
            aggregated_data = aggregated.model_dump() if aggregated else None
            
            html_report = generate_html_report(
                task_data=task_data,
                creatives=creatives_data,
                aggregated=aggregated_data,
                aggregation_error=aggregation_error
            )
            logger.info(f"✅ Generated HTML report")
        except Exception as e:
            logger.error(f"❌ Failed to generate HTML report: {e}")
        
        # Update task with results (even if aggregation failed)
        update_data = {
            "status": TaskStatus.COMPLETED,
            "creatives_analyzed": [a.model_dump() for a in analyses],
            "updated_at": datetime.utcnow()
        }
        
        if aggregated:
            update_data["aggregated_analysis"] = aggregated.model_dump()
        
        if aggregation_error:
            update_data["aggregation_error"] = aggregation_error
        
        if html_report:
            update_data["html_report"] = html_report
        
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": update_data}
        )
        
        logger.info(f"✅ Task {task_id}: Analysis completed, {len(analyses)} creatives")
        
    except Exception as e:
        logger.error(f"❌ Task {task_id} analysis failed: {e}")
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": TaskStatus.FAILED,
                "error": str(e),
                "updated_at": datetime.utcnow()
            }}
        )


async def _aggregate_analysis(analyses: List[CreativeAnalysis]) -> AggregatedAnalysis:
    """Aggregate analysis across all creatives using LLM."""
    from src.analysis.gemini_client import generate_analysis
    from concurrent.futures import ThreadPoolExecutor
    
    # Build summary of all analyses
    summaries = []
    for a in analyses:
        summaries.append({
            "id": a.creative_id,
            "hook": a.hook,
            "visual_style": a.visual_style,
            "pains": a.pains,
            "value_props": a.value_props,
            "cta": a.cta,
            "scores": a.scores,
            "summary": a.summary
        })
    
    prompt_context = json.dumps(summaries, ensure_ascii=False)
    
    # LLM aggregation prompt (blocking operation - run in executor)
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(
            executor,
            generate_analysis,
            {
                "task": "aggregate_competitor_analysis",
                "creatives_count": len(analyses),
                "analyses_summary": prompt_context
            },
            None  # schema parameter
        )
    
    # Validate and clean result
    def _safe_get_list(key, default=None):
        val = result.get(key, default or [])
        if val is None:
            return []
        if isinstance(val, str):
            return [val]
        if isinstance(val, list):
            return val
        return []
    
    def _safe_get_dict(key, default=None):
        val = result.get(key, default or {})
        if isinstance(val, dict):
            return val
        return {}
    
    try:
        return AggregatedAnalysis(
            pain_points=_safe_get_list("pain_points"),
            concepts=_safe_get_list("concepts"),
            visual_trends=_safe_get_dict("visual_trends"),
            hooks=_safe_get_list("hooks"),
            core_idea=result.get("core_idea"),
            theme=result.get("theme"),
            message=result.get("message"),
            recommendations=result.get("recommendations"),
            video_prompt=result.get("video_prompt")
        )
    except Exception as e:
        logger.error(f"Failed to create AggregatedAnalysis from result: {e}")
        logger.error(f"Raw result: {json.dumps(result, ensure_ascii=False)[:500]}")
        raise
