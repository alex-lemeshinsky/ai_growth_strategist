"""
Video analysis prototype using Gemini vision capabilities.
Extracts hooks, CTAs, visual elements, on-screen text, and product showcase from video ads.
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "models/gemini-2.0-flash")


def _ensure_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set. Please export your Google AI Studio API key.")
    genai.configure(api_key=api_key)


def analyze_video_file(
    video_path: str,
    meta: Optional[Dict[str, Any]] = None,
    model_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze a video file using Gemini vision model.
    
    Args:
        video_path: Path to the cached video file
        meta: Optional metadata about the creative (page_name, platforms, etc.)
        model_name: Gemini model to use (default: gemini-1.5-flash)
    
    Returns:
        Dictionary with structured analysis
    """
    _ensure_api_key()
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Upload video to Gemini
    print(f"📤 Uploading video: {Path(video_path).name}")
    video_file = genai.upload_file(path=video_path)
    print(f"✅ Uploaded as: {video_file.name}")
    
    # Wait for file to become active
    import time
    print("⏳ Waiting for file to be processed...")
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)
    
    if video_file.state.name != "ACTIVE":
        raise RuntimeError(f"File processing failed: {video_file.state.name}")
    print("✅ File is ready")
    
    # Try to use specified model, fallback to working alternatives
    model_to_use = model_name or DEFAULT_MODEL
    
    # Ensure model name has correct prefix
    if not model_to_use.startswith("models/"):
        model_to_use = f"models/{model_to_use}"
    
    try:
        model = genai.GenerativeModel(model_to_use)
    except Exception as e:
        print(f"⚠️  Model {model_to_use} not available, trying models/gemini-2.0-flash...")
        try:
            model = genai.GenerativeModel("models/gemini-2.0-flash")
        except Exception:
            print("⚠️  Trying models/gemini-2.0-pro-exp...")
            model = genai.GenerativeModel("models/gemini-2.0-pro-exp")
    
    # Build context
    context = ""
    if meta:
        context = f"\nМетадані креативу:\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n"
    
    # Prompt for video analysis (Ukrainian)
    prompt = f"""Проаналізуй цей відеокреатив конкурента детально.

{context}

Завдання:
1. **Hook (0-3 сек)**: Що відбувається в перші 3 секунди? Який хук використовується? На якій секунді точно? Яка тактика (швидкі зміни, запитання, bold claim, демо продукту, проблема)?

2. **Візуальні елементи**: 
   - Стиль (UGC, screencast, motion graphics, real footage)?
   - Ефекти (jump cuts, zooms, transitions, filters)?
   - Субтитри/текст на екрані (є/немає, стиль, колір)?
   - Колір/настрій (яскраві/темні/мінімалізм)?

3. **Текст на екрані (OCR)**: Випиши весь видимий текст з екрану по таймкодах (якщо є).

4. **Показ продукту**:
   - Як показують продукт (UI демо, реальний продукт, до/після, тільки текст)?
   - На яких секундах показують UI/функції?
   - Які ключові фічі підкреслюють?

5. **CTA (Call-to-Action)**:
   - Де з'являється CTA (голос, текст на екрані, кінцева заставка)?
   - Точний таймкод і текст CTA?
   - Чи повторюється?

6. **Болі/Value Props**:
   - Які проблеми/болі показують або згадують?
   - Які переваги/рішення пропонують?

7. **Музика/Звук**:
   - Настрій музики (енергійна, спокійна, драматична)?
   - Чи є закадровий голос?
   - Звукові ефекти?

8. **Покадровий сторіборд** (по сценах):
   - Сцена 1 (0-X сек): що бачимо, що чуємо
   - Сцена 2 (X-Y сек): що бачимо, що чуємо
   - ... (для кожної зміни сцени)

9. **Загальна оцінка** (0-1):
   - Сила хука
   - Чіткість CTA
   - Видимість продукту
   - Щільність меседжів
   - Якість виконання

Відповідь виключно у форматі JSON:
{{
  "hook": {{
    "time_start_s": 0.0,
    "time_end_s": 3.0,
    "description": "детальний опис",
    "tactic": "назва тактики",
    "strength": 0.8
  }},
  "visual_style": {{
    "style": "UGC/screencast/etc",
    "effects": ["effect1", "effect2"],
    "has_captions": true/false,
    "caption_style": "опис стилю",
    "color_mood": "опис"
  }},
  "on_screen_text": [
    {{"timecode_s": 1.5, "text": "текст на екрані"}},
    {{"timecode_s": 5.0, "text": "інший текст"}}
  ],
  "product_showcase": {{
    "type": "UI demo/Real product/Before-After/Text only",
    "timecodes_s": [2.0, 5.5, 10.0],
    "key_features": ["feature1", "feature2"],
    "clarity_score": 0.7
  }},
  "cta": [
    {{
      "timecode_s": 12.0,
      "text": "Download Now",
      "channel": "on-screen/voice/both",
      "strength": 0.9
    }}
  ],
  "pains": [
    {{"text": "опис болю", "timecode_s": 1.0}}
  ],
  "value_props": [
    {{"text": "опис переваги", "timecode_s": 3.5}}
  ],
  "audio": {{
    "has_voiceover": true/false,
    "music_mood": "energetic/calm/dramatic/none",
    "sound_effects": true/false
  }},
  "storyboard": [
    {{
      "scene": 1,
      "time_start_s": 0.0,
      "time_end_s": 3.0,
      "what_we_see": "опис візуалу",
      "what_we_hear": "опис аудіо"
    }}
  ],
  "scores": {{
    "hook_strength": 0.8,
    "cta_clarity": 0.9,
    "product_visibility": 0.7,
    "message_density": 0.6,
    "execution_quality": 0.8
  }},
  "summary": "коротке резюме 2-3 речення"
}}

Не вигадуй: якщо чогось не видно або не чути — пиши null або порожній масив."""

    # Generate analysis
    print("🤖 Аналізую відео з Gemini...")
    response = model.generate_content(
        [video_file, prompt],
        generation_config={
            "temperature": 0.3,
            "response_mime_type": "application/json",
        }
    )
    
    # Parse JSON response
    try:
        result = json.loads(response.text)
        print("✅ Аналіз завершено")
        return result
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse error: {e}")
        # Try to extract JSON from response
        import re
        m = re.search(r"\{[\s\S]*\}", response.text)
        if m:
            return json.loads(m.group(0))
        # Fallback
        return {
            "error": "Failed to parse JSON",
            "raw_response": response.text[:500]
        }


def analyze_video_prototype(video_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Simple wrapper for prototype testing.
    
    Args:
        video_path: Path to video file
        output_path: Optional path to save JSON result
    
    Returns:
        Analysis dictionary
    """
    result = analyze_video_file(video_path)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved to: {output_path}")
    
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.analysis.video_analyzer <video_path> [output_json]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = analyze_video_prototype(video_path, output_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
