"""
LLM-powered chat planner for brief collection.

Uses Gemini 2.0 to guide conversation and extract brief fields.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Required fields for brief completion
REQUIRED_FIELDS = ["product_offer", "audience", "objective", "platform", "duration_s", "cta"]


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
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Analyze user message and decide next step.

        Args:
            user_message: Latest message from user
            known_fields: Currently known brief fields
            conversation_history: Previous messages [{role, text}]

        Returns:
            Dict with either:
            - Ask mode: {"need_more_info": true, "question": "...", "missing_fields": [...], "updates": {...}}
            - Final mode: {"need_more_info": false, "final_prompt": "...", "brief": {...}}
        """
        try:
            prompt = self._build_prompt(user_message, known_fields, conversation_history)

            logger.info(f"📤 Sending request to Gemini (history: {len(conversation_history)} messages)")
            response = self.model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty response from Gemini")

            result = json.loads(response.text)
            logger.info(f"📥 Received response: need_more_info={result.get('need_more_info', 'unknown')}")

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
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Build system prompt for Gemini."""

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
        missing_text = ", ".join(missing) if missing else "none"

        prompt = f"""You are a creative producer helping to collect information for a performance video brief.

Your goal is to ask concise, friendly questions to gather ONLY these required fields:
- product_offer (string): What product/service/offer to promote
- audience (string): Target audience description
- objective (enum): install | lead | purchase | signup | traffic
- platform (enum): tiktok | instagram | youtube
- duration_s (integer): 6 | 9 | 15 | 30 seconds
- cta (string): Call-to-action text

RULES:
1. Ask ONE question at a time, in Ukrainian language
2. Be concise and friendly
3. Extract info from user's answer and update known fields
4. When ALL required fields are filled → switch to final mode
5. Infer reasonable defaults when possible (e.g., if user says "Instagram Reels" → platform=instagram, format=reels)

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
  "question": "Concise question in Ukrainian",
  "missing_fields": ["field1", "field2"],
  "updates": {{"field_name": "extracted_value"}}
}}

If ready (all required fields present):
{{
  "need_more_info": false,
  "final_prompt": "Detailed prompt for video generation in Ukrainian",
  "brief": {{
    "product_offer": "...",
    "audience": "...",
    "objective": "install|lead|purchase|signup|traffic",
    "platform": "tiktok|instagram|youtube",
    "format": "reels|shorts|tiktok|feed",
    "aspect_ratio": "9:16",
    "duration_s": 15,
    "cta": "..."
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
