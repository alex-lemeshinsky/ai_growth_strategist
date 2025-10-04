"""
Extract patterns from Step-1 analysis task for chat suggestions.
"""
import logging
from typing import Dict, Any, List, Optional
from collections import Counter

logger = logging.getLogger(__name__)


def extract_patterns_summary(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract compact patterns summary from Step-1 task analysis.

    Args:
        task_data: Full task document from MongoDB (with creatives_analyzed + aggregated_analysis)

    Returns:
        Compact patterns summary for LLM context
    """
    try:
        creatives = task_data.get("creatives_analyzed", [])
        aggregated = task_data.get("aggregated_analysis", {})

        if not creatives and not aggregated:
            logger.warning("No analysis data found in task")
            return {}

        patterns = {
            "hooks": _extract_hooks(creatives, aggregated),
            "structures": _extract_structures(creatives),
            "styles": _extract_styles(creatives, aggregated),
            "ctas": _extract_ctas(creatives),
            "messaging": _extract_messaging(aggregated),
            "durations": _extract_durations(creatives),
            "platforms": _extract_platforms(creatives)
        }

        logger.info(f"✅ Extracted patterns: {len(patterns['hooks'])} hooks, {len(patterns['structures'])} structures")

        return patterns

    except Exception as e:
        logger.error(f"Error extracting patterns: {e}")
        return {}


def _extract_hooks(creatives: List[Dict], aggregated: Dict) -> List[Dict[str, Any]]:
    """Extract top hooks from analysis."""
    hooks = []

    # From aggregated analysis
    agg_hooks = aggregated.get("hooks", [])
    for hook in agg_hooks[:5]:  # Top 5
        if isinstance(hook, dict):
            hooks.append({
                "text": hook.get("description", str(hook)),
                "type": hook.get("type", "unknown"),
                "source": "aggregated"
            })
        elif isinstance(hook, str):
            hooks.append({
                "text": hook,
                "type": "text",
                "source": "aggregated"
            })

    # From individual creatives (if aggregated is empty)
    if not hooks:
        for creative in creatives[:10]:
            hook_data = creative.get("hook", {})
            if hook_data and isinstance(hook_data, dict):
                description = hook_data.get("description") or hook_data.get("text")
                if description:
                    hooks.append({
                        "text": description[:100],  # Truncate long hooks
                        "type": hook_data.get("type", "visual"),
                        "source": "creative"
                    })

    return hooks[:8]  # Max 8 hooks


def _extract_structures(creatives: List[Dict]) -> List[Dict[str, Any]]:
    """Extract common narrative structures from storyboards."""
    structures = []
    structure_counter = Counter()

    for creative in creatives:
        storyboard = creative.get("storyboard", [])
        if not storyboard or len(storyboard) < 2:
            continue

        # Extract structure pattern (hook → body → cta)
        structure_type = _classify_structure(storyboard)
        structure_counter[structure_type] += 1

    # Return top 3 structures
    for structure_type, count in structure_counter.most_common(3):
        structures.append({
            "type": structure_type,
            "count": count,
            "confidence": round(count / len(creatives), 2) if creatives else 0
        })

    return structures


def _classify_structure(storyboard: List[Dict]) -> str:
    """Classify narrative structure from storyboard."""
    if len(storyboard) < 2:
        return "simple"

    # Check for common patterns
    scene_descriptions = " ".join([
        s.get("description", "").lower()
        for s in storyboard
    ])

    if "problem" in scene_descriptions and "solution" in scene_descriptions:
        return "problem-solution"
    elif "before" in scene_descriptions and "after" in scene_descriptions:
        return "before-after"
    elif "testimonial" in scene_descriptions or "review" in scene_descriptions:
        return "testimonial"
    elif len(storyboard) >= 4:
        return "multi-scene"
    else:
        return "hook-body-cta"


def _extract_styles(creatives: List[Dict], aggregated: Dict) -> List[Dict[str, Any]]:
    """Extract visual/production styles."""
    styles = []

    # From aggregated visual trends
    visual_trends = aggregated.get("visual_trends", {})
    if visual_trends:
        style = visual_trends.get("style", "")
        pacing = visual_trends.get("pacing", "")
        color_palette = visual_trends.get("color_palette", "")

        if style:
            styles.append({
                "aspect": "production",
                "value": style,
                "source": "aggregated"
            })
        if pacing:
            styles.append({
                "aspect": "pacing",
                "value": pacing,
                "source": "aggregated"
            })
        if color_palette:
            styles.append({
                "aspect": "color",
                "value": color_palette,
                "source": "aggregated"
            })

    # From individual creatives
    if not styles:
        style_counter = Counter()
        for creative in creatives:
            visual_style = creative.get("visual_style", {})
            if isinstance(visual_style, dict):
                style_type = visual_style.get("type") or visual_style.get("style")
                if style_type:
                    style_counter[style_type] += 1

        for style_type, count in style_counter.most_common(3):
            styles.append({
                "aspect": "production",
                "value": style_type,
                "count": count,
                "source": "creatives"
            })

    return styles[:5]


def _extract_ctas(creatives: List[Dict]) -> List[Dict[str, Any]]:
    """Extract common CTAs."""
    ctas = []
    cta_texts = []

    for creative in creatives:
        cta_list = creative.get("cta", [])
        for cta in cta_list:
            if isinstance(cta, dict):
                text = cta.get("text") or cta.get("description")
                timestamp = cta.get("timestamp_seconds")
                urgency = cta.get("urgency")

                if text and text not in cta_texts:
                    ctas.append({
                        "text": text,
                        "timestamp": timestamp,
                        "urgency": urgency,
                        "source": "creative"
                    })
                    cta_texts.append(text)

    return ctas[:6]  # Max 6 unique CTAs


def _extract_messaging(aggregated: Dict) -> Dict[str, List[str]]:
    """Extract pain points and value props."""
    return {
        "pain_points": aggregated.get("pain_points", [])[:5],
        "value_props": [],  # Not in current schema
        "core_message": aggregated.get("message") or aggregated.get("core_idea"),
        "theme": aggregated.get("theme")
    }


def _extract_durations(creatives: List[Dict]) -> List[Dict[str, Any]]:
    """Extract common video durations."""
    # This would come from video metadata if available
    # For now, return common defaults
    return [
        {"duration_s": 15, "count": 0, "recommended": True},
        {"duration_s": 30, "count": 0, "recommended": False}
    ]


def _extract_platforms(creatives: List[Dict]) -> List[str]:
    """Extract platforms from creatives."""
    # This would come from creative metadata
    # For now, infer from page_name or return defaults
    return ["instagram", "facebook"]


def format_patterns_for_prompt(patterns: Dict[str, Any]) -> str:
    """
    Format patterns summary for inclusion in LLM prompt.

    Args:
        patterns: Extracted patterns dictionary

    Returns:
        Formatted string for prompt injection
    """
    if not patterns:
        return ""

    sections = []

    # Hooks
    if patterns.get("hooks"):
        hooks_text = "TOP HOOKS (з аналізу конкурентів):\n"
        for i, hook in enumerate(patterns["hooks"][:5], 1):
            hooks_text += f"{i}. {hook['text']} (type: {hook['type']})\n"
        sections.append(hooks_text)

    # Structures
    if patterns.get("structures"):
        struct_text = "POPULAR STRUCTURES:\n"
        for struct in patterns["structures"][:3]:
            struct_text += f"- {struct['type']} (used in {struct['count']} ads)\n"
        sections.append(struct_text)

    # Styles
    if patterns.get("styles"):
        style_text = "VISUAL STYLES:\n"
        for style in patterns["styles"][:3]:
            style_text += f"- {style['aspect']}: {style['value']}\n"
        sections.append(style_text)

    # CTAs
    if patterns.get("ctas"):
        cta_text = "COMMON CTAs:\n"
        for cta in patterns["ctas"][:4]:
            cta_text += f"- \"{cta['text']}\""
            if cta.get("urgency"):
                cta_text += f" (urgency: {cta['urgency']})"
            cta_text += "\n"
        sections.append(cta_text)

    # Messaging
    if patterns.get("messaging"):
        msg = patterns["messaging"]
        if msg.get("pain_points"):
            msg_text = "KEY PAIN POINTS:\n"
            for pain in msg["pain_points"][:3]:
                msg_text += f"- {pain}\n"
            sections.append(msg_text)

    return "\n".join(sections)


def get_default_patterns() -> Dict[str, Any]:
    """
    Get default patterns when no task_id provided.

    Returns:
        Default patterns for common scenarios
    """
    return {
        "hooks": [
            {"text": "Проблема → швидке рішення (3-5с)", "type": "problem-solution", "source": "default"},
            {"text": "Запитання до аудиторії (риторичне)", "type": "question", "source": "default"},
            {"text": "Несподіваний факт/статистика", "type": "fact", "source": "default"},
            {"text": "До/Після трансформація", "type": "before-after", "source": "default"}
        ],
        "structures": [
            {"type": "hook-body-cta", "confidence": 1.0, "recommended": True},
            {"type": "problem-solution", "confidence": 0.8, "recommended": True},
            {"type": "testimonial", "confidence": 0.6, "recommended": False}
        ],
        "styles": [
            {"aspect": "production", "value": "UGC (user-generated content)", "source": "default"},
            {"aspect": "production", "value": "Screencast (screen recording)", "source": "default"},
            {"aspect": "pacing", "value": "Динамічний (quick cuts)", "source": "default"}
        ],
        "ctas": [
            {"text": "Завантажуй зараз", "urgency": "high", "source": "default"},
            {"text": "Дізнайся більше", "urgency": "medium", "source": "default"},
            {"text": "Спробуй безкоштовно", "urgency": "medium", "source": "default"}
        ],
        "platform_recommendations": {
            "instagram": {"duration_s": [15, 30], "format": "reels", "aspect_ratio": "9:16"},
            "tiktok": {"duration_s": [9, 15], "format": "tiktok", "aspect_ratio": "9:16"},
            "youtube": {"duration_s": [15, 30], "format": "shorts", "aspect_ratio": "9:16"}
        }
    }
