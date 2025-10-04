"""
LLM-powered chat planner for brief collection.

Uses Gemini 2.0 to guide conversation and extract brief fields.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from src.services.patterns_extractor import (
    extract_patterns_summary,
    format_patterns_for_prompt,
    get_default_patterns
)
from src.services.chat_planner_helpers import (
    add_policy_hints_to_response,
    generate_enhanced_final_prompt
)

logger = logging.getLogger(__name__)

# Required fields for brief completion (extended)
REQUIRED_FIELDS = ["product_offer", "audience", "objective", "platform", "duration_s", "cta"]

# Creative fields (optional but recommended)
CREATIVE_FIELDS = ["hook", "structure", "style"]


class ChatPlanner:
    """LLM planner for conversational brief collection."""

    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize chat planner with Gemini model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        )
        logger.info(f"✅ ChatPlanner initialized with model: {model_name}")

    def plan_next_step(
        self,
        user_message: str,
        known_fields: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        patterns: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze user message and decide next step.

        Args:
            user_message: Latest message from user
            known_fields: Currently known brief fields
            conversation_history: Previous messages [{role, text}]
            patterns: Optional patterns from Step-1 analysis

        Returns:
            Dict with either:
            - Ask mode: {"need_more_info": true, "question": "...", "options": [...], "suggestions": [...], "examples": [...], ...}
            - Final mode: {"need_more_info": false, "final_prompt": "...", "brief": {...}, "creative_spec": {...}}
        """
        try:
            prompt = self._build_prompt(user_message, known_fields, conversation_history, patterns)

            logger.info(f"📤 Sending request to Gemini (history: {len(conversation_history)} messages, patterns: {bool(patterns)})")
            response = self.model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty response from Gemini")

            result = json.loads(response.text)
            logger.info(f"📥 Received response: need_more_info={result.get('need_more_info', 'unknown')}")

            # Add policy hints if detected risks
            if result.get("need_more_info"):
                result = add_policy_hints_to_response(result, user_message, known_fields)

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Raw response: {response.text if 'response' in locals() else 'N/A'}")
            # Fallback: return generic ask
            return {
                "need_more_info": True,
                "question": "Вибачте, виникла помилка. Давайте спробуємо ще раз. Що ви хочете рекламувати?",
                "missing_fields": REQUIRED_FIELDS,
                "updates": {}
            }

        except Exception as e:
            logger.error(f"Error in ChatPlanner.plan_next_step: {e}")
            raise

    def _build_prompt(
        self,
        user_message: str,
        known_fields: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        patterns: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build system prompt for Gemini with patterns context."""

        # Build conversation context
        history_text = ""
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            role = msg.get("role", "user")
            text = msg.get("text", "")
            history_text += f"{role.upper()}: {text}\n"

        # Current known fields
        known_text = json.dumps(known_fields, indent=2, ensure_ascii=False)

        # Missing fields
        missing = [f for f in REQUIRED_FIELDS if not known_fields.get(f)]
        missing_creative = [f for f in CREATIVE_FIELDS if not known_fields.get(f)]
        missing_text = ", ".join(missing + missing_creative) if (missing or missing_creative) else "none"

        # Patterns context
        patterns_text = ""
        if patterns:
            patterns_text = "\n\nCOMPETITOR PATTERNS (from Step-1 analysis):\n" + format_patterns_for_prompt(patterns)
        else:
            # Use defaults
            default_patterns = get_default_patterns()
            patterns_text = "\n\nDEFAULT BEST PRACTICES:\n" + format_patterns_for_prompt(default_patterns)

        prompt = f"""You are an expert creative producer helping to collect information for a performance video brief.

Your goal is to ask concise, friendly questions to gather these fields:

REQUIRED:
- product_offer (string): What product/service/offer to promote
- audience (string): Target audience description
- objective (enum): install | lead | purchase | signup | traffic
- platform (enum): tiktok | instagram | youtube
- duration_s (integer): 6 | 9 | 15 | 30 seconds
- cta (string): Call-to-action text

CREATIVE (optional but recommended):
- hook (string): Hook concept/type (first 3s)
- structure (string): Narrative structure (problem-solution, before-after, testimonial, etc.)
- style (string): Visual style (UGC, screencast, testimonial, etc.)

RULES:
1. Ask ONE question at a time, in Ukrainian language
2. Be concise and friendly (max 2 sentences)
3. Provide 3-4 quick-click OPTIONS for common fields (platform, objective, duration, structure, style)
4. Provide SUGGESTIONS from competitor patterns when relevant (use patterns_text below)
5. Give 1-2 EXAMPLES of good answers for open fields (audience, hook, cta)
6. Extract info from user's answer and update known fields
7. When ALL REQUIRED fields filled → collect creative fields (hook/structure/style) if missing
8. When ready → switch to final mode with creative_spec
9. Infer reasonable defaults (e.g., "Instagram Reels" → platform=instagram, format=reels, duration_s=15)
{patterns_text}

CURRENT STATE:
Known fields: {known_text}
Missing fields: {missing_text}

CONVERSATION HISTORY:
{history_text}

USER'S LATEST MESSAGE:
{user_message}

OUTPUT JSON FORMAT:

If need more info (missing fields remain):
{{
  "need_more_info": true,
  "question": "Concise question in Ukrainian (max 2 sentences)",
  "missing_fields": ["field1", "field2"],
  "updates": {{"field_name": "extracted_value"}},
  "options": ["Option 1", "Option 2", "Option 3"],  // Optional: quick-click choices
  "suggestions": [  // Optional: from patterns or defaults
    {{"text": "Suggestion 1", "source": "patterns|default"}},
    {{"text": "Suggestion 2", "source": "patterns|default"}}
  ],
  "examples": ["Example 1", "Example 2"]  // Optional: example answers
}}

If ready (all required fields present + creative fields collected):
{{
  "need_more_info": false,
  "final_prompt": "Detailed video generation prompt in Ukrainian",
  "brief": {{
    "product_offer": "...",
    "audience": "...",
    "objective": "install|lead|purchase|signup|traffic",
    "platform": "tiktok|instagram|youtube",
    "format": "reels|shorts|tiktok|feed",
    "aspect_ratio": "9:16",
    "duration_s": 15,
    "cta": "..."
  }},
  "creative_spec": {{  // Optional but recommended
    "hook": {{"type": "problem-solution", "description": "..."}},
    "structure": "hook-body-cta",
    "style": {{"production": "UGC", "pacing": "dynamic"}},
    "voiceover": ["Line 1 (0-3s)", "Line 2 (3-8s)", "Line 3 (8-15s)"],
    "on_screen_text": ["Hook text", "Value prop", "CTA"],
    "cta_spec": {{"text": "...", "timestamp": 12, "urgency": "high"}}
  }}
}}

Respond with valid JSON only."""

        return prompt

    def generate_fallback_prompt(self, brief: Dict[str, Any]) -> str:
        """
        Generate fallback final prompt if LLM doesn't provide one.

        Args:
            brief: Complete brief fields

        Returns:
            Formatted prompt string
        """
        platform = brief.get("platform", "instagram")
        format_type = brief.get("format", "reels")
        duration = brief.get("duration_s", 15)
        product = brief.get("product_offer", "продукт")
        audience = brief.get("audience", "цільова аудиторія")
        objective = brief.get("objective", "install")
        cta = brief.get("cta", "Дізнатися більше")

        return f"""Створи сценарій {duration}с вертикального перформанс-відео для {platform}/{format_type}.

КОНТЕКСТ:
- Продукт/Оффер: {product}
- Аудиторія: {audience}
- Мета: {objective}
- Тривалість: {duration}с
- CTA: {cta}

ПОТРІБНО:
- Shot list на 3-4 сцени з тайм-кодами
- Текст войсовера
- Текст на екрані
- Хук (0-3с) та розміщення CTA

Формат: вертикальне відео 9:16 для мобільних пристроїв."""


def calculate_completeness(known_fields: Dict[str, Any]) -> float:
    """
    Calculate brief completeness percentage.

    Args:
        known_fields: Dictionary with brief fields

    Returns:
        Completeness from 0.0 to 1.0
    """
    filled = sum(1 for field in REQUIRED_FIELDS if known_fields.get(field))
    return round(filled / len(REQUIRED_FIELDS), 2)


def get_missing_fields(known_fields: Dict[str, Any]) -> List[str]:
    """
    Get list of missing required fields.

    Args:
        known_fields: Dictionary with brief fields

    Returns:
        List of missing field names
    """
    return [field for field in REQUIRED_FIELDS if not known_fields.get(field)]


def is_brief_complete(known_fields: Dict[str, Any]) -> bool:
    """
    Check if brief has all required fields.

    Args:
        known_fields: Dictionary with brief fields

    Returns:
        True if all required fields present
    """
    return len(get_missing_fields(known_fields)) == 0
