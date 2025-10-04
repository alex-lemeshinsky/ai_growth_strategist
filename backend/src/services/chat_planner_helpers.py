"""
Helper functions for chat planner: policy hints, fallbacks, etc.
"""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Policy risk keywords for hints
POLICY_RISK_KEYWORDS = {
    "health_claims": {
        "keywords": ["лікує", "виліковує", "гарантує здоров'я", "cure", "heal", "лечит"],
        "hint": "💡 Увага: уникай медичних claims без підтверджень (ризик відхилення модерацією)"
    },
    "before_after": {
        "keywords": ["до і після", "before after", "результат за", "втратив", "схуднув"],
        "hint": "💡 Підказка: before/after вимагає disclaimers або може бути відхилено"
    },
    "guarantees": {
        "keywords": ["100% гарантія", "обіцяємо", "точно отримаєш", "guarantee", "promised"],
        "hint": "💡 Підказка: абсолютні гарантії часто блокуються модерацією"
    },
    "music_rights": {
        "keywords": ["популярна музика", "хіт", "пісня", "music", "song", "track"],
        "hint": "💡 Підказка: для музики потрібні ліцензії або використовуй royalty-free"
    },
    "celebrities": {
        "keywords": ["знаменитість", "зірка", "celebrity", "famous person", "селебріті"],
        "hint": "💡 Підказка: для зірок потрібен дозвіл, краще використовувати UGC"
    },
    "alcohol_tobacco": {
        "keywords": ["алкоголь", "сигарети", "тютюн", "alcohol", "cigarette", "tobacco"],
        "hint": "⚠️ Увага: алкоголь/тютюн мають жорсткі обмеження на рекламу"
    }
}


def detect_policy_risks(text: str, known_fields: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Detect potential policy risks in user input.

    Args:
        text: User message or known field values
        known_fields: Current brief state

    Returns:
        List of detected risks with hints
    """
    risks = []

    # Safe text handling
    text_lower = text.lower() if text else ""

    # Check product_offer for risks
    product = known_fields.get("product_offer") or ""
    product_lower = product.lower() if isinstance(product, str) else ""

    combined_text = f"{text_lower} {product_lower}"

    for risk_type, config in POLICY_RISK_KEYWORDS.items():
        for keyword in config["keywords"]:
            if keyword in combined_text:
                risks.append({
                    "type": risk_type,
                    "hint": config["hint"],
                    "detected_keyword": keyword
                })
                break  # Only add once per risk type

    return risks


def add_policy_hints_to_response(result: Dict[str, Any], user_message: str, known_fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add policy hints to LLM response if risks detected.

    Args:
        result: LLM response dict
        user_message: User's latest message
        known_fields: Current brief state

    Returns:
        Modified result with policy_hints if applicable
    """
    risks = detect_policy_risks(user_message, known_fields)

    if risks:
        # Add hints to response
        if "policy_hints" not in result:
            result["policy_hints"] = []

        for risk in risks:
            if risk["hint"] not in [h.get("text") for h in result.get("policy_hints", [])]:
                result["policy_hints"].append({
                    "text": risk["hint"],
                    "type": risk["type"]
                })

        logger.info(f"🚨 Policy risks detected: {[r['type'] for r in risks]}")

    return result


def generate_enhanced_final_prompt(brief: Dict[str, Any], creative_spec: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate enhanced final prompt with creative spec.

    Args:
        brief: Complete brief fields
        creative_spec: Optional creative specification

    Returns:
        Detailed generation prompt
    """
    platform = brief.get("platform", "instagram")
    format_type = brief.get("format", "reels")
    duration = brief.get("duration_s", 15)
    product = brief.get("product_offer", "продукт")
    audience = brief.get("audience", "цільова аудиторія")
    objective = brief.get("objective", "install")
    cta = brief.get("cta", "Дізнатися більше")

    hook = brief.get("hook", "Привертаючий увагу хук")
    structure = brief.get("structure", "hook-body-cta")
    style = brief.get("style", "UGC")

    prompt = f"""Створи детальний сценарій {duration}с вертикального перформанс-відео для {platform}/{format_type}.

📋 КОНТЕКСТ:
• Продукт/Оффер: {product}
• Аудиторія: {audience}
• Мета кампанії: {objective}
• Тривалість: {duration}с
• CTA: {cta}

🎬 КРЕАТИВНА КОНЦЕПЦІЯ:
• Hook: {hook}
• Структура: {structure}
• Стиль: {style}
• Формат: вертикальне 9:16 для мобільних

📝 ПОТРІБНО СТВОРИТИ:
"""

    if creative_spec:
        # Detailed spec with creative_spec
        hook_spec = creative_spec.get("hook", {})
        prompt += f"""
1. HOOK (0-3с):
   • Тип: {hook_spec.get('type', 'problem-solution')}
   • Опис: {hook_spec.get('description', 'Привертаючий увагу початок')}

2. STRUCTURE ({structure}):
"""
        voiceover = creative_spec.get("voiceover", [])
        if voiceover:
            prompt += "   • Voiceover:\n"
            for i, line in enumerate(voiceover, 1):
                prompt += f"     {i}. {line}\n"

        on_screen_text = creative_spec.get("on_screen_text", [])
        if on_screen_text:
            prompt += "   • On-screen text:\n"
            for i, text in enumerate(on_screen_text, 1):
                prompt += f"     {i}. {text}\n"

        cta_spec = creative_spec.get("cta_spec", {})
        if cta_spec:
            prompt += f"""
3. CTA:
   • Текст: {cta_spec.get('text', cta)}
   • Таймінг: {cta_spec.get('timestamp', duration-3)}с
   • Urgency: {cta_spec.get('urgency', 'medium')}
"""

        style_spec = creative_spec.get("style", {})
        if style_spec:
            prompt += f"""
4. PRODUCTION STYLE:
   • Тип: {style_spec.get('production', 'UGC')}
   • Pacing: {style_spec.get('pacing', 'dynamic')}
"""
    else:
        # Basic fallback
        prompt += f"""
1. SHOT LIST (3-4 сцени з тайм-кодами)
2. VOICEOVER (текст озвучки з таймінгами)
3. ON-SCREEN TEXT (текст на екрані, коли показувати)
4. HOOK (0-3с): {hook}
5. CTA ({duration-3}-{duration}с): {cta}
"""

    prompt += f"""
🎯 ФОКУС НА PERFORMANCE:
• Швидкий хук (перші 3с критичні для retention)
• Чіткий value proposition
• Сильний CTA з urgency
• Оптимізація під {platform} (вертикальний формат, текст читабельний на mobile)
"""

    return prompt
