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


async def parse_ads_task(task_id: str, url: str, max_results: int = 15):
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
                    "error": "No ads found",
                    "updated_at": datetime.utcnow()
                }}
            )
            return
        
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
        for ad in raw_ads:
            try:
                video_url = _pick_video_url(ad)
                if not video_url:
                    logger.warning(f"No video for ad {ad.get('ad_archive_id')}")
                    continue
                
                # Cache video
                cached_path = _cache_video(video_url)
                
                # Analyze with Gemini
                result = analyze_video_file(
                    cached_path,
                    meta={
                        "page_name": ad.get("page_name"),
                        "ad_archive_id": ad.get("ad_archive_id")
                    }
                )
                
                # Create analysis object
                analysis = CreativeAnalysis(
                    creative_id=ad.get("ad_archive_id"),
                    ad_archive_id=ad.get("ad_archive_id"),
                    page_name=ad.get("page_name"),
                    hook=result.get("hook"),
                    visual_style=result.get("visual_style"),
                    on_screen_text=result.get("on_screen_text", []),
                    product_showcase=result.get("product_showcase"),
                    cta=result.get("cta", []),
                    pains=result.get("pains", []),
                    value_props=result.get("value_props", []),
                    audio=result.get("audio"),
                    storyboard=result.get("storyboard", []),
                    scores=result.get("scores"),
                    summary=result.get("summary"),
                    video_url=video_url,
                    cached_video_path=cached_path,
                    analyzed_at=datetime.utcnow()
                )
                
                analyses.append(analysis)
                logger.info(f"✅ Analyzed creative {ad.get('ad_archive_id')}")
                
            except Exception as e:
                logger.error(f"Error analyzing {ad.get('ad_archive_id')}: {e}")
                continue
        
        if not analyses:
            raise ValueError("No creatives could be analyzed")
        
        # Aggregate analysis with LLM
        aggregated = await _aggregate_analysis(analyses)
        
        # Update task with results
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": TaskStatus.COMPLETED,
                "creatives_analyzed": [a.model_dump() for a in analyses],
                "aggregated_analysis": aggregated.model_dump() if aggregated else None,
                "updated_at": datetime.utcnow()
            }}
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
    
    # LLM aggregation prompt
    result = generate_analysis({
        "task": "aggregate_competitor_analysis",
        "creatives_count": len(analyses),
        "analyses_summary": prompt_context
    }, schema=None)
    
    return AggregatedAnalysis(
        pain_points=result.get("pain_points", []),
        concepts=result.get("concepts", []),
        visual_trends=result.get("visual_trends", {}),
        hooks=result.get("hooks", []),
        core_idea=result.get("core_idea"),
        theme=result.get("theme"),
        message=result.get("message"),
        recommendations=result.get("recommendations"),
        video_prompt=result.get("video_prompt")
    )
