import os
import json
from typing import Any, Dict, Optional

import google.generativeai as genai


DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "models/gemini-2.0-flash")


def _ensure_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set. Please export your Google AI Studio API key.")
    genai.configure(api_key=api_key)


def generate_analysis(
    video_facts: Dict[str, Any],
    schema: Optional[Dict[str, Any]] = None,
    model_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Call Gemini to produce a structured analysis JSON based on provided video_facts.

    Notes:
    - MVP uses only textual/meta fields; do not hallucinate visual details.
    - If schema is provided, we request JSON output accordingly.
    """
    _ensure_api_key()

    model_to_use = model_name or DEFAULT_MODEL
    if not model_to_use.startswith("models/"):
        model_to_use = f"models/{model_to_use}"
    
    model = genai.GenerativeModel(model_to_use)

    system_msg = (
        "Ти — Senior Creative Strategist & Performance Marketer. "
        "Проаналізуй відеорекламу конкурента. Не вигадуй фактів: якщо даних бракує — став null."
    )

    user_msg = (
        "Контекст — текст/метадані креативу (не відео):\n"
        f"{json.dumps(video_facts, ensure_ascii=False)}\n\n"
        "Завдання: побудуй структурований JSON з hook/CTA/болі/value props/стиль/сторіборд/музика/підсумок. "
        "Якщо немає даних (бо немає STT/OCR/сцен) — повертай null/порожні масиви."
    )

    generation_config = {
        "temperature": 0.3,
    }

    if schema is not None:
        # Request JSON output with a target schema
        generation_config.update({
            "response_mime_type": "application/json",
            "response_schema": schema,
        })
        prompt = [system_msg, user_msg]
    else:
        prompt = [system_msg, user_msg, "Відповідь виключно у форматі JSON."]

    resp = model.generate_content(
        prompt,
        generation_config=generation_config,
    )

    if resp.prompt_feedback and getattr(resp.prompt_feedback, "block_reason", None):
        raise RuntimeError(f"Gemini blocked the request: {resp.prompt_feedback.block_reason}")

    text = resp.text or "{}"
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract fenced JSON if any
        import re
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            return json.loads(m.group(0))
        raise
