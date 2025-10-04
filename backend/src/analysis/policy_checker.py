"""
Video policy compliance checker using Gemini vision.
Analyzes videos for Facebook Ads Policy violations.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


FACEBOOK_POLICY_PROMPT = """
Ти — експерт з Facebook Ads Policy. Детально проаналізуй це відео і перевір його на відповідність політиці реклами Facebook/Meta.

**ЗАВДАННЯ:**

1. **Детальний опис відео:**
   - Що показано у відео (кадр за кадром)?
   - Хто присутній (люди, їх вигляд, одяг, поведінка)?
   - Які об'єкти, продукти, бренди видно?
   - Який текст з'являється на екрані?
   - Які звуки, музика, голос?
   - Які жести, рухи, дії?
   - Загальний настрій і тон відео

2. **Перевірка брендів і торгових марок:**
   - Чи є логотипи, назви брендів, торгові марки?
   - Чи використовуються чужі бренди без дозволу?
   - Чи є посилання на відомі компанії?

3. **Перевірка заборонених жестів і контенту:**
   - Чи є непристойні жести або символи?
   - Чи є насильство, зброя, небезпечні дії?
   - Чи є дискримінаційний контент?
   - Чи є сексуальний або провокативний контент?
   - Чи є тютюн, алкоголь, наркотики?

4. **Перевірка музики і аудіо:**
   - Чи використовується захищена авторськими правами музика?
   - Чи є образливі або недоречні слова?
   - Чи відповідає аудіо візуальному контенту?

5. **NSFW (Not Safe For Work) фільтр:**
   - Чи безпечне відео для перегляду на роботі?
   - Чи є оголення, інтимний контент?
   - Чи є шокуючий або тривожний контент?

6. **Facebook Ads Policy порушення:**
   Перевір на:
   - Заборонений контент (наркотики, зброя, азартні ігри)
   - Оманливі практики
   - Дискримінацію (раса, стать, вік, релігія)
   - Нереалістичні обіцянки або результати
   - "До/після" зображення без дисклеймерів
   - Медичні/фармацевтичні твердження без підтвердження
   - Залякування або шокуючий контент
   - Зловживання особистими даними
   - Фейкові новини або дезінформацію

7. **Фідбек і рекомендації:**
   - Чи пройде відео модерацію Facebook?
   - Якщо НІ - чому саме і що треба виправити?
   - Конкретні поради для виправлення
   - Альтернативні підходи

**ФОРМАТ ВІДПОВІДІ (JSON):**

```json
{
  "video_description": {
    "visual_content": "детальний опис того, що видно",
    "people": "опис людей, їх вигляд, дії",
    "objects_products": ["список об'єктів/продуктів"],
    "on_screen_text": ["текст1", "текст2"],
    "audio_description": "опис звуку/музики/голосу",
    "gestures_actions": ["жест1", "дія1"],
    "overall_tone": "настрій відео"
  },
  
  "brands_trademarks": {
    "detected_brands": ["brand1", "brand2"],
    "trademark_issues": "чи є проблеми з брендами",
    "brand_usage_ok": true/false
  },
  
  "prohibited_content": {
    "inappropriate_gestures": false,
    "violence_weapons": false,
    "discriminatory_content": false,
    "sexual_content": false,
    "drugs_alcohol_tobacco": false,
    "details": "деталі якщо щось знайдено"
  },
  
  "audio_copyright": {
    "copyrighted_music": false,
    "offensive_language": false,
    "audio_issues": "опис проблем якщо є"
  },
  
  "nsfw_check": {
    "safe_for_work": true/false,
    "nudity": false,
    "shocking_content": false,
    "nsfw_reasons": "причини якщо не safe"
  },
  
  "facebook_policy_violations": [
    {
      "category": "назва категорії порушення",
      "severity": "low/medium/high/critical",
      "description": "опис порушення",
      "timestamp_seconds": 5.2,
      "recommendation": "як виправити"
    }
  ],
  
  "compliance_summary": {
    "will_pass_moderation": true/false,
    "confidence": 0.95,
    "risk_level": "low/medium/high",
    "overall_assessment": "загальна оцінка"
  },
  
  "feedback": {
    "main_issues": ["проблема1", "проблема2"],
    "required_changes": ["зміна1", "зміна2"],
    "recommendations": ["рекомендація1", "рекомендація2"],
    "alternative_approaches": ["підхід1", "підхід2"]
  }
}
```

**ВАЖЛИВО:**
- Будь максимально детальним і точним
- Якщо не впевнений - вкажи це
- Не вигадуй порушень якщо їх немає
- Поясни ЧОМУ щось є порушенням
- Дай конкретні поради для виправлення
"""


def check_video_policy(
    video_path: str,
    platform: str = "facebook",
    model_name: Optional[str] = None,
    video_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check video compliance with platform advertising policy.
    
    Args:
        video_path: Path to video file
        platform: Platform name (currently only 'facebook')
        model_name: Gemini model to use
    
    Returns:
        Dictionary with policy check results
    """
    if platform != "facebook":
        raise ValueError(f"Platform '{platform}' not supported yet. Only 'facebook' is available.")
    
    # Configure Gemini
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")
    
    genai.configure(api_key=api_key)
    
    # Upload video (from path or URL)
    if video_url:
        # Direct upload from URL (no intermediate storage)
        print(f"📤 Uploading video from URL for policy check...")
        import httpx
        import io
        
        with httpx.stream("GET", video_url, follow_redirects=True, timeout=60.0) as response:
            response.raise_for_status()
            
            # Create in-memory file
            video_bytes = io.BytesIO()
            for chunk in response.iter_bytes():
                video_bytes.write(chunk)
            video_bytes.seek(0)
            
            # Upload to Gemini from memory
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                tmp.write(video_bytes.read())
                tmp_path = tmp.name
            
            try:
                video_file = genai.upload_file(path=tmp_path)
                print(f"✅ Uploaded as: {video_file.name}")
            finally:
                os.unlink(tmp_path)
    else:
        # Upload from local path
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"📤 Uploading video for policy check: {Path(video_path).name}")
        video_file = genai.upload_file(path=video_path)
        print(f"✅ Uploaded as: {video_file.name}")
    
    # Wait for processing
    import time
    print("⏳ Waiting for video processing...")
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)
    
    if video_file.state.name != "ACTIVE":
        raise RuntimeError(f"Video processing failed: {video_file.state.name}")
    
    print("✅ Video ready for analysis")
    
    # Get model
    model_to_use = model_name or os.environ.get("GEMINI_MODEL", "models/gemini-2.0-flash")
    if not model_to_use.startswith("models/"):
        model_to_use = f"models/{model_to_use}"
    
    model = genai.GenerativeModel(model_to_use)
    
    # Analyze
    print("🔍 Analyzing video for policy compliance...")
    response = model.generate_content(
        [video_file, FACEBOOK_POLICY_PROMPT],
        generation_config={
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    )
    
    if response.prompt_feedback and getattr(response.prompt_feedback, "block_reason", None):
        raise RuntimeError(f"Gemini blocked the request: {response.prompt_feedback.block_reason}")
    
    # Parse result
    import json
    result_text = response.text or "{}"
    
    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        import re
        match = re.search(r'\{[\s\S]*\}', result_text)
        if match:
            result = json.loads(match.group(0))
        else:
            raise ValueError("Failed to parse Gemini response as JSON")
    
    print("✅ Policy check complete!")
    
    # Add metadata
    result["metadata"] = {
        "video_path": video_path if video_path else "streamed_from_url",
        "video_url": video_url,
        "platform": platform,
        "model": model_to_use,
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return result


def format_policy_report(result: Dict[str, Any]) -> str:
    """
    Format policy check result as readable text report.
    
    Args:
        result: Policy check result dictionary
    
    Returns:
        Formatted text report
    """
    compliance = result.get("compliance_summary", {})
    will_pass = compliance.get("will_pass_moderation", False)
    risk_level = compliance.get("risk_level", "unknown")
    
    report = "="*80 + "\n"
    report += "📋 FACEBOOK ADS POLICY CHECK REPORT\n"
    report += "="*80 + "\n\n"
    
    # Status
    status_emoji = "✅" if will_pass else "❌"
    report += f"{status_emoji} MODERATION STATUS: {'PASS' if will_pass else 'FAIL'}\n"
    report += f"⚠️  RISK LEVEL: {risk_level.upper()}\n"
    report += f"📊 CONFIDENCE: {compliance.get('confidence', 0):.0%}\n\n"
    
    # Main issues
    feedback = result.get("feedback", {})
    main_issues = feedback.get("main_issues", [])
    
    if main_issues:
        report += "🚨 MAIN ISSUES:\n"
        for issue in main_issues:
            report += f"   • {issue}\n"
        report += "\n"
    
    # Violations
    violations = result.get("facebook_policy_violations", [])
    if violations:
        report += f"⛔ POLICY VIOLATIONS ({len(violations)}):\n\n"
        for i, v in enumerate(violations, 1):
            report += f"   {i}. [{v.get('severity', 'unknown').upper()}] {v.get('category', 'Unknown')}\n"
            report += f"      {v.get('description', 'No description')}\n"
            if v.get('timestamp_seconds'):
                report += f"      Timestamp: {v['timestamp_seconds']}s\n"
            if v.get('recommendation'):
                report += f"      💡 Fix: {v['recommendation']}\n"
            report += "\n"
    
    # NSFW check
    nsfw = result.get("nsfw_check", {})
    if not nsfw.get("safe_for_work", True):
        report += "🔞 NSFW WARNING:\n"
        report += f"   {nsfw.get('nsfw_reasons', 'Content not safe for work')}\n\n"
    
    # Required changes
    required_changes = feedback.get("required_changes", [])
    if required_changes:
        report += "✏️  REQUIRED CHANGES:\n"
        for change in required_changes:
            report += f"   • {change}\n"
        report += "\n"
    
    # Recommendations
    recommendations = feedback.get("recommendations", [])
    if recommendations:
        report += "💡 RECOMMENDATIONS:\n"
        for rec in recommendations:
            report += f"   • {rec}\n"
        report += "\n"
    
    # Overall assessment
    report += "📝 OVERALL ASSESSMENT:\n"
    report += f"   {compliance.get('overall_assessment', 'No assessment available')}\n\n"
    
    report += "="*80 + "\n"
    
    return report
