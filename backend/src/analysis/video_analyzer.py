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
    
    # Prompt for video analysis (Ukrainian) - Performance Marketing oriented
    prompt = f"""Роль: Ти — експертний Performance Marketing Creative Strategist. Твоє завдання — не просто описати відео, а проаналізувати його ефективність, визначити психологічні тригери та надати дієві гіпотези для тестування.

Проаналізуй цей відеокреатив конкурента, спираючись на наданий контекст.

1. Контекст:
{context}

2. Завдання Аналізу:

Проведи глибокий аналіз за наступною структурою та надай відповідь виключно у форматі JSON.

Hook (0-3 секунди): Визнач основний гачок. Який психологічний принцип він використовує (напр., Curiosity Gap, Social Proof, Loss Aversion, Shock)? Наскільки він релевантний для ЦА?

Візуальний Стиль та Динаміка: Оціни стиль, ефекти та кольорову гаму. Який темп у відео (повільний, швидкий, змішаний)? Як це впливає на сприйняття?

Текст на екрані (OCR): Розпізнай та випиши весь текст з екрану з таймкодами.

Показ Продукту/Цінності: Як продукт інтегрований у сюжет? Чи показують лише фічі, чи демонструють результат/трансформацію для користувача?

CTA (Call-to-Action): Проаналізуй заклик до дії. Чи є в ньому терміновість, обмеження або додатковий стимул (incentive)?

Ключове Повідомлення (Messaging): Які болі ЦА зачіпаються і які ціннісні пропозиції (value props) пропонуються як рішення? Як вони сформульовані (наприклад, через сторітелінг, пряме звернення, демонстрацію "до/після")?

Аудіо: Оціни музику, голос та звукові ефекти. Чи доповнюють вони візуальний ряд і підсилюють емоції?

Наратив та Емоційний Шлях: Розбий відео на ключові сцени. Яку емоційну подорож проходить глядач (напр., від інтриги -> до проблеми -> до рішення -> до бажаного результату)?

Карта Сильних та Слабких Сторін: Оціни ключові елементи за шкалою від 0 до 1, де 1 — максимальна ефективність.

Ключові Висновки та Гіпотези: Сформулюй головну стратегію креативу, ключові інсайти та 2-3 конкретні гіпотези, які ми можемо протестувати у наших власних креативах.

Відповідь виключно у форматі JSON:
{{
  "hook": {{
    "time_start_s": 0.0,
    "time_end_s": 3.0,
    "description": "детальний опис гачка",
    "psychological_principle": "Curiosity Gap / Social Proof / Loss Aversion / Shock / інше",
    "relevance_to_audience": "оцінка релевантності для ЦА",
    "strength": 0.8
  }},
  "visual_style": {{
    "style": "UGC/screencast/motion graphics/real footage/інше",
    "effects": ["jump cuts", "zooms", "transitions", "filters"],
    "color_palette": "опис кольорової гами",
    "pacing": "slow/fast/mixed",
    "pacing_impact": "як темп впливає на сприйняття",
    "has_captions": true/false,
    "caption_style": "опис стилю субтитрів"
  }},
  "on_screen_text": [
    {{"timecode_s": 1.5, "text": "текст на екрані"}}
  ],
  "product_showcase": {{
    "type": "UI demo/Real product/Transformation/Result-focused/Feature-focused",
    "integration_quality": "наскільки природньо інтегрований продукт",
    "shows_transformation": true/false,
    "timecodes_s": [2.0, 5.5, 10.0],
    "key_features": ["feature1", "feature2"],
    "clarity_score": 0.7
  }},
  "cta": [
    {{
      "timecode_s": 12.0,
      "text": "точний текст CTA",
      "channel": "on-screen/voice/both",
      "has_urgency": true/false,
      "has_incentive": true/false,
      "incentive_description": "опис стимулу, якщо є",
      "strength": 0.9
    }}
  ],
  "messaging": {{
    "pains": [
      {{"text": "біль ЦА", "timecode_s": 1.0, "presentation_style": "storytelling/direct/visual"}}
    ],
    "value_props": [
      {{"text": "ціннісна пропозиція", "timecode_s": 3.5, "presentation_style": "before-after/testimonial/demonstration"}}
    ],
    "messaging_approach": "storytelling/direct address/problem-solution/before-after"
  }},
  "audio": {{
    "has_voiceover": true/false,
    "voiceover_tone": "опис тону голосу",
    "music_mood": "energetic/calm/dramatic/uplifting/none",
    "sound_effects": true/false,
    "audio_visual_alignment": "як аудіо доповнює візуальний ряд"
  }},
  "emotional_journey": [
    {{
      "scene": 1,
      "time_start_s": 0.0,
      "time_end_s": 3.0,
      "what_we_see": "опис візуалу",
      "what_we_hear": "опис аудіо",
      "emotional_state": "intrigue/problem/solution/desire/action",
      "viewer_emotion": "яку емоцію відчуває глядач"
    }}
  ],
  "scores": {{
    "hook_strength": 0.8,
    "cta_clarity": 0.9,
    "product_visibility": 0.7,
    "message_density": 0.6,
    "execution_quality": 0.8,
    "emotional_impact": 0.7,
    "relevance_to_audience": 0.8
  }},
  "key_insights": {{
    "main_strategy": "головна стратегія креативу в 1-2 реченнях",
    "key_insights": [
      "інсайт 1: що робить цей креатив ефективним",
      "інсайт 2: ключова тактика або підхід",
      "інсайт 3: унікальний елемент"
    ],
    "hypotheses_to_test": [
      "Гіпотеза 1: конкретна ідея для тестування в наших креативах",
      "Гіпотеза 2: альтернативний підхід на основі аналізу",
      "Гіпотеза 3: елемент для A/B тестування"
    ]
  }},
  "summary": "коротке резюме аналізу в 2-3 реченнях з фокусом на ефективності та застосуванні"
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
