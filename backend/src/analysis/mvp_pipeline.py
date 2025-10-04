import os
import json
import hashlib
from typing import List, Dict, Any, Tuple
from datetime import datetime

import httpx

from src.api.models import AdCreative
from src.services.data_processor import DataProcessor
from src.analysis.models import VideoFacts, VideoAsset, TextVariant, AnalysisResult, AnalysisScores, HookItem, CTAItem, PainItem, ValuePropItem, ConceptStyle, StoryboardItem, ProductShowcase, MusicInfo

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".cache", "videos")
ANALYSIS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "analysis")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _now_utc() -> datetime:
    return datetime.utcnow()


def _parse_date(s: str) -> datetime:
    # Input like "2025-09-24 07:00:00" (assume UTC naive)
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def _active_days(start_date_formatted: str) -> int:
    try:
        start = _parse_date(start_date_formatted)
        delta = _now_utc() - start
        return max(0, delta.days)
    except Exception:
        return 0


def _pick_video_url(raw_item: Dict[str, Any]) -> str | None:
    snap = raw_item.get("snapshot", {})
    # Prefer cards HD
    for card in snap.get("cards", []) or []:
        if card.get("video_hd_url"):
            return card["video_hd_url"]
    for card in snap.get("cards", []) or []:
        if card.get("video_sd_url"):
            return card["video_sd_url"]
    # Fallback: snapshot.videos
    for v in snap.get("videos", []) or []:
        if v.get("video_hd_url"):
            return v["video_hd_url"]
    for v in snap.get("videos", []) or []:
        if v.get("video_sd_url"):
            return v["video_sd_url"]
    return None


def _cache_video(url: str) -> str:
    fname = _sha256(url) + ".mp4"
    path = os.path.join(CACHE_DIR, fname)
    if os.path.exists(path):
        return path
    # Download with httpx
    with httpx.stream("GET", url, timeout=30.0, follow_redirects=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_bytes():
                if chunk:
                    f.write(chunk)
    return path


def _detect_locale_from_link(link_url: str | None) -> str | None:
    if not link_url:
        return None
    # naive patterns for language tag inside URL params (e.g., 3_46_fr, 3_46_de, 3_46_it, 3_46_ar)
    import re
    m = re.search(r"[_=](fr|de|it|ar|en)(?:[&_]|$)", link_url)
    if m:
        return m.group(1)
    return None


def _build_variants(ad: AdCreative) -> List[TextVariant]:
    variants: List[TextVariant] = []
    for c in ad.cards or []:
        locale = _detect_locale_from_link(getattr(c, "link_url", None))
        variants.append(TextVariant(
            locale_hint=locale,
            body=c.body if isinstance(c.body, str) else (c.body.get("text") if isinstance(c.body, dict) else None),
            title=c.title,
            caption=c.caption,
            cta_text=c.cta_text,
        ))
    return variants


def _build_video_facts(ad: AdCreative, raw_item: Dict[str, Any], cached_video: str | None, video_url: str | None) -> VideoFacts:
    return VideoFacts(
        creative_id=ad.ad_archive_id,
        page_name=ad.page_name,
        is_active=ad.is_active,
        active_days=_active_days(raw_item.get("start_date_formatted", "")) if raw_item.get("start_date_formatted") else None,
        publisher_platform=raw_item.get("publisher_platform", []) or ad.publisher_platform,
        start_date=raw_item.get("start_date_formatted"),
        end_date=raw_item.get("end_date_formatted"),
        text_primary=ad.body,
        title_primary=ad.title,
        caption_primary=ad.caption,
        variants=_build_variants(ad),
        assets=[VideoAsset(url=video_url, cached_path=cached_video)] if video_url else [],
    )


def _rank_score(vf: VideoFacts, analysis: AnalysisResult | None) -> float:
    # Very simple MVP ranking
    placements = len(vf.publisher_platform) / 5.0
    variants = max(1, len(vf.variants)) / 5.0
    has_cta = 1.0 if (any(v.cta_text for v in vf.variants) or (vf.text_primary and "download" in (vf.text_primary.lower()))) else 0.5
    recency = 1.0 if (vf.active_days is not None and vf.active_days <= 7) else 0.6
    llm = (analysis.scores.overall or 0.0) if (analysis and analysis.scores) else 0.0
    return round(0.35*placements + 0.25*variants + 0.2*has_cta + 0.1*recency + 0.1*llm, 4)


def load_ads_from_json(json_path: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = data.get("extraction_metadata", {})
    ads = data.get("ads", [])
    return meta, ads


def process_raw_ads(raw_ads: List[Dict[str, Any]]) -> List[AdCreative]:
    # DataProcessor expects a list of raw items with our snapshot layout
    return DataProcessor.process_ads(raw_ads)


def filter_candidates(raw_ads: List[Dict[str, Any]], min_days: int = 3, max_days: int = 14) -> List[Dict[str, Any]]:
    out = []
    for item in raw_ads:
        if not item.get("is_active", False):
            continue
        sd = item.get("start_date_formatted")
        if not sd:
            continue
        days = _active_days(sd)
        if min_days <= days <= max_days:
            out.append(item)
    return out


def _rule_based_analysis(vf: VideoFacts) -> AnalysisResult:
    # Build meta
    meta = {
        "creative_id": vf.creative_id,
        "page_name": vf.page_name,
        "is_active": vf.is_active,
        "active_days": vf.active_days,
        "publisher_platform": vf.publisher_platform,
        "start_date": vf.start_date,
        "end_date": vf.end_date,
        "text_primary": vf.text_primary,
        "title_primary": vf.title_primary,
        "caption_primary": vf.caption_primary,
        "variants_count": len(vf.variants),
        "cta_variants": [v.cta_text for v in vf.variants if v.cta_text],
        "locales": [v.locale_hint for v in vf.variants if v.locale_hint],
    }

    hooks: List[HookItem] = []
    ctas: List[CTAItem] = []
    pains: List[PainItem] = []
    vals: List[ValuePropItem] = []

    # Very naive extraction from text variants
    seen_cta = set()
    for v in vf.variants:
        if v.body and isinstance(v.body, str):
            text = v.body.strip()
            # Use first sentence or up to 12 words as a hook
            import re
            sentence = re.split(r"[\.!?]\s|\n", text)[0]
            words = sentence.split()
            desc = " ".join(words[:12])
            tactic = "question" if "?" in text else "value_claim"
            hooks.append(HookItem(time_s=None, tactic=tactic, desc=desc, strength=None))

            # detect pains/value props by keyword heuristics
            lowered = text.lower()
            pain_triggers = ["low storage", "stockage faible", "wenig speicher", "memoria quasi piena", "التخزين منخفض"]
            value_triggers = ["free up", "libérez", "gib speicher", "libera spazio", "حرر مساحة"]
            if any(p in lowered for p in pain_triggers):
                pains.append(PainItem(text=sentence, timecodes=[], severity=None))
            if any(p in lowered for p in value_triggers):
                vals.append(ValuePropItem(text=sentence, timecodes=[], strength=None))
        if v.cta_text and v.cta_text not in seen_cta:
            seen_cta.add(v.cta_text)
            ctas.append(CTAItem(text=v.cta_text, channels=["on-screen"], time_s=None, strength=None))

    if not ctas:
        # derive from titles
        for v in vf.variants:
            if v.title and any(k in v.title.lower() for k in ["install", "download"]):
                key = v.title
                if key not in seen_cta:
                    seen_cta.add(key)
                    ctas.append(CTAItem(text=key, channels=["on-screen"], time_s=None, strength=None))

    concept = ConceptStyle(style=("DCO multi-language" if len(vf.variants) > 1 else "VIDEO"), effects=[], captions={"present": bool(vf.variants), "style": "unknown"})
    storyboard = [StoryboardItem(scene=1, start_s=None, end_s=None, what_we_see="Video ad (details N/A)", what_we_hear=None)] if vf.assets else []
    showcase = ProductShowcase(type="App promotion", scenes=[1] if storyboard else [], features=[], clarity_score=None)
    music = MusicInfo(bpm=None, mood=None, notes=None)

    scores = AnalysisScores(
        hook=0.6 if hooks else 0.3,
        cta=0.7 if ctas else 0.3,
        product_visibility=0.5,
        message_density=min(1.0, len(vf.variants)/5.0),
        structure=0.5,
        music_fit=0.5,
        overall=None,
    )

    result = AnalysisResult(
        creative_id=vf.creative_id,
        meta=meta,
        scores=scores,
        hooks=hooks,
        cta=ctas,
        pains=pains,
        value_props=vals,
        concept_style=concept,
        storyboard=storyboard,
        product_showcase=showcase,
        music=music,
        summary="Rule-based analysis from available text fields (MVP)."
    )
    return result


def run_mvp(json_path: str, top_k: int = 3, window: Tuple[int, int] = (3, 14), use_schema: bool = False, mode: str = "simple") -> List[AnalysisResult]:
    meta, raw_ads = load_ads_from_json(json_path)
    if not raw_ads:
        return []

    candidates = filter_candidates(raw_ads, window[0], window[1])
    if not candidates:
        # fallback: take first few
        candidates = raw_ads[: min(top_k*2, len(raw_ads))]

    processed = process_raw_ads(candidates)

    results: List[AnalysisResult] = []
    for ad, raw in zip(processed, candidates):
        video_url = _pick_video_url(raw)
        cached_path = _cache_video(video_url) if video_url else None
        vf = _build_video_facts(ad, raw, cached_path, video_url)

        # Build meta for LLM/simple
        llm_meta = {
            "creative_id": ad.ad_archive_id,
            "page_name": ad.page_name,
            "is_active": ad.is_active,
            "active_days": vf.active_days,
            "publisher_platform": vf.publisher_platform,
            "start_date": vf.start_date,
            "end_date": vf.end_date,
            "text_primary": vf.text_primary,
            "title_primary": vf.title_primary,
            "caption_primary": vf.caption_primary,
            "variants_count": len(vf.variants),
            "cta_variants": [v.cta_text for v in vf.variants if v.cta_text],
        }

        analysis: AnalysisResult
        if mode == "gemini":
            schema = None if not use_schema else {
                "type": "object",
                "properties": {
                    "creative_id": {"type": "string"},
                    "meta": {"type": "object", "properties": {"note": {"type": "string"}}},
                    "scores": {
                        "type": "object",
                        "properties": {
                            "hook": {"type": "number"},
                            "cta": {"type": "number"},
                            "product_visibility": {"type": "number"},
                            "message_density": {"type": "number"},
                            "structure": {"type": "number"},
                            "music_fit": {"type": "number"},
                            "overall": {"type": "number"}
                        }
                    },
                    "hooks": {"type": "array", "items": {"type": "object", "properties": {"time_s": {"type": "number"}}}},
                    "cta": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    "pains": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    "value_props": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    "concept_style": {"type": "object", "properties": {"style": {"type": "string"}}},
                    "storyboard": {"type": "array", "items": {"type": "object", "properties": {"scene": {"type": "number"}}}},
                    "product_showcase": {"type": "object", "properties": {"type": {"type": "string"}}},
                    "music": {"type": "object", "properties": {"mood": {"type": "string"}}},
                    "summary": {"type": "string"}
                },
                "required": ["creative_id", "scores", "hooks", "cta", "pains", "value_props", "concept_style", "storyboard", "product_showcase", "music", "summary"]
            }
            try:
                from src.analysis.gemini_client import generate_analysis
                llm_out = generate_analysis({"meta": llm_meta, "assets": [a.model_dump() for a in vf.assets], "texts": [v.model_dump() for v in vf.variants]}, schema)
                analysis = AnalysisResult(**llm_out)
            except Exception:
                analysis = _rule_based_analysis(vf)
        else:
            analysis = _rule_based_analysis(vf)

        analysis.creative_id = ad.ad_archive_id
        analysis.meta = llm_meta
        analysis.overall_rank_score = _rank_score(vf, analysis)

        # Save per-creative analysis
        out_path = os.path.join(ANALYSIS_DIR, f"analysis_{ad.ad_archive_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(analysis.model_dump(), f, ensure_ascii=False, indent=2)

        results.append(analysis)

    # Sort by overall_rank_score desc and return top_k
    results.sort(key=lambda r: (r.overall_rank_score or 0.0), reverse=True)
    return results[:top_k]
