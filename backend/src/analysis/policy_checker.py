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
Ти — експерт з Facebook/Meta Ads Policy з глибоким знанням всіх рекламних політик платформи. Проаналізуй це відео максимально детально і перевір його на відповідність всім вимогам Meta для рекламного контенту.

**КОНТЕКСТ АНАЛІЗУ:**
- Це відео призначене для ПЛАТНОЇ реклами на Facebook/Instagram
- Застосовуються найсуворіші стандарти модерації
- Необхідна 100% відповідність Community Standards та Advertising Policies
- Аналізуй відео як людина-модератор Meta

---

**ЗАВДАННЯ:**

### 1. ДЕТАЛЬНИЙ ОПИС ВІДЕО (покадровий аналіз)

**Візуальний контент:**
- Опиши кожну сцену/кадр послідовно
- Що показано в кожній секунді відео?
- Які переходи між сценами?
- Якість зображення та освітлення
- Чи є будь-які приховані або неоднозначні елементи?

**Люди у відео:**
- Скільки людей, їх стать, приблизний вік
- Зовнішній вигляд (одяг, макіяж, зачіска)
- Чи відповідає одяг нормам пристойності? (немає надмірного оголення)
- Пози та мова тіла
- Вираз обличчя та емоції
- Взаємодія між людьми
- ⚠️ КРИТИЧНО: Чи виглядають люди як повнолітні (18+)? Якщо є сумніви - вкажи це

**Об'єкти, продукти, реквізит:**
- Детальний список всіх видимих предметів
- Продукти або послуги, що рекламуються
- Фонові об'єкти
- ⚠️ Чи є предмети, що можуть трактуватися як заборонені (імітація зброї, таблетки, алкоголь тощо)?

**Текст на екрані:**
- Весь текст точно (включно з помилками якщо є)
- Шрифт, розмір, колір
- Тривалість показу кожного тексту
- ⚠️ Перевір на заборонені твердження: "швидке схуднення", "чудодійний ефект", "гарантований результат", "схвалено FDA" тощо
- ⚠️ Чи є клікбейт або оманливі заголовки?
- ⚠️ Чи є граматичні помилки, що можуть вказувати на шахрайство?

**Аудіо:**
- Опис музики (жанр, настрій, темп)
- Голос за кадром (що говориться, інтонація)
- Звукові ефекти
- Чіткість та якість звуку

**Жести та дії:**
- Всі рухи та жести детально
- ⚠️ КРИТИЧНО: чи немає непристойних жестів (середній палець, неприйнятні рухи тазом, імітація сексуальних дій)
- Чи безпечні фізичні дії (немає небезпечних трюків без попереджень)?

**Загальний тон:**
- Емоційне забарвлення
- Цільова аудиторія
- Стиль подачі (серйозний, гумористичний, мотиваційний тощо)

---

### 2. БРЕНДИ, ТОРГОВІ МАРКИ ТА ІНТЕЛЕКТУАЛЬНА ВЛАСНІСТЬ

**Виявлені бренди:**
- Список всіх логотипів, назв компаній, торгових марок
- Тривалість та розмір показу кожного бренду
- Чи є це власний бренд рекламодавця чи сторонній?

**Перевірка використання:**
- ⚠️ Чи використовуються бренди META/Facebook/Instagram без дозволу?
- ⚠️ Чи є посилання на конкурентів (TikTok, Twitter/X, YouTube) з негативним контекстом?
- ⚠️ Чи використовуються celebritities/публічні особи без очевидного партнерства?
- ⚠️ Чи є логотипи відомих компаній (Apple, Nike, Coca-Cola тощо)?
- Чи може це трактуватися як фальшиве схвалення (fake endorsement)?

**Авторські права:**
- Можливі порушення авторських прав на зображення
- Використання стокових фото/відео (якщо впізнаєш)

---

### 3. ЗАБОРОНЕНИЙ ТА ОБМЕЖЕНИЙ КОНТЕНТ

**3.1. Непристойності та сексуальний контент:**
- ⚠️ Оголення (навіть часткове - оголені плечі, декольте, білизна)
- ⚠️ Сексуально натякаючі пози або рухи
- ⚠️ Акцент на частинах тіла (сідниці, груди, пах)
- ⚠️ Прозорий одяг або одяг що обтягує
- ⚠️ Камера фокусується на інтимних зонах
- ⚠️ Натяки на сексуальні послуги або знайомства для дорослих
- Рівень відповідності: повністю відповідає / потребує корекції / категорично заборонено

**3.2. Насильство та небезпечний контент:**
- ⚠️ Зброя (навіть іграшкова або історична)
- ⚠️ Насильство або погрози
- ⚠️ Кров, травми, медичні процедури
- ⚠️ Небезпечні трюки без попереджень
- ⚠️ Жорстоке поводження з тваринами
- ⚠️ Аварії, катастрофи, лиха

**3.3. Дискримінація та образливий контент:**
- ⚠️ Расові, етнічні стереотипи
- ⚠️ Дискримінація за статю, віком, релігією
- ⚠️ Образливі жарти або мемі
- ⚠️ Негативні асоціації з певними групами людей
- ⚠️ Body shaming або зневага до зовнішності
- ⚠️ Таргетинг на вразливі групи (вагітні, люди з хворобами, фінансові труднощі)

**3.4. Тютюн, алкоголь, наркотики:**
- ⚠️ КРИТИЧНО: Тютюнові вироби, вейпи, е-сигарети (ПОВНА ЗАБОРОНА)
- ⚠️ Алкоголь (вимагає обмежень за віком, не можна показувати вживання)
- ⚠️ Наркотики, аптечні препарати, CBD продукти
- ⚠️ Приналежність для вживання (бонги, трубки тощо)
- ⚠️ Натяки на зміну свідомості або "кайф"

**3.5. Азартні ігри та лотереї:**
- ⚠️ Казино, покер, ставки
- ⚠️ Лотереї або розіграші без правил
- ⚠️ Навички що імітують азартні ігри

**3.6. Фінансові послуги та криптовалюта:**
- ⚠️ Криптовалюта, ICO, NFT (вимагає попереднього дозволу)
- ⚠️ Бінарні опціони
- ⚠️ Обіцянки швидкого збагачення
- ⚠️ Схеми "швидких грошей"
- ⚠️ Кредити з високими відсотками без розкриття умов

---

### 4. МЕДИЧНІ ТА HEALTH-RELATED CLAIMS

**Продукти для здоров'я:**
- ⚠️ КРИТИЧНО: Зображення "До/Після" (ЗАБОРОНЕНО без спеціального дозволу)
- ⚠️ Нереалістичні результати схуднення
- ⚠️ Твердження про лікування хвороб
- ⚠️ Дієтичні добавки без дисклеймерів
- ⚠️ Фокус на проблемних зонах тіла
- ⚠️ Ліки, що відпускаються за рецептом
- ⚠️ Медичні пристрої без сертифікації
- ⚠️ Твердження схвалені FDA/MOH без доказів

**Психологічні маніпуляції:**
- ⚠️ Залякування ("у вас може бути рак")
- ⚠️ Викликання страху або паніки
- ⚠️ Самодіагностика серйозних захворювань
- ⚠️ Відмова від традиційної медицини

---

### 5. ОМАНЛИВІ ПРАКТИКИ

**Клікбейт та сенсації:**
- ⚠️ Неправдиві заголовки
- ⚠️ "Ви не повірите що сталося далі"
- ⚠️ Фейкові кнопки "play" або "close"
- ⚠️ Оманливі ескізи (thumbnails)

**Нереалістичні обіцянки:**
- ⚠️ "Схудни на 10 кг за тиждень"
- ⚠️ "Заробляй $10000 за день"
- ⚠️ "100% гарантія" без умов
- ⚠️ Фальшиві відгуки або статистика

**Шахрайство:**
- ⚠️ Фішинг або збір особистих даних
- ⚠️ Малварі або шкідливі програми
- ⚠️ Фальшиві знижки або дефіцит ("залишилось 2 товари")
- ⚠️ Підробка офіційних повідомлень

---

### 6. МУЗИКА ТА АУДІО АВТОРСЬКІ ПРАВА

**Перевірка музики:**
- Назва треку якщо впізнається
- ⚠️ КРИТИЧНО: Чи звучить як комерційна музика відомих виконавців?
- ⚠️ Чи є це популярна пісня (ймовірно захищена)?
- Безпечні варіанти: royalty-free музика, Facebook Sound Collection, ліцензована музика

**Аудіо контент:**
- ⚠️ Лайка, образливі слова
- ⚠️ Агресивні або образливі висловлювання
- ⚠️ Неправдива інформація голосом

---

### 7. NSFW (NOT SAFE FOR WORK) ФІЛЬТР

**Загальна безпечність:**
- Чи можна показувати на робочому місці?
- Чи підходить для сімейного перегляду?
- Чи безпечно для дітей 13+?

**Конкретні перевірки:**
- ⚠️ Оголення будь-якого рівня
- ⚠️ Інтимний або еротичний контент
- ⚠️ Шокуючі зображення (кров, травми, операції)
- ⚠️ Тривожний контент (жахи, насильство)
- ⚠️ Контент для дорослих (навіть натяки)

---

### 8. ПОЛІТИКА ОСОБИСТИХ АТРИБУТІВ

**Таргетинг на особисті характеристики:**
- ⚠️ ЗАБОРОНЕНО: "Ти товстий? Купи цей продукт"
- ⚠️ ЗАБОРОНЕНО: "Для людей з діабетом"
- ⚠️ ЗАБОРОНЕНО: "Самотні? Знайди пару"
- ⚠️ ЗАБОРОНЕНО: Звертання до фінансового стану
- ⚠️ ЗАБОРОНЕНО: Натяки на медичний стан
- ⚠️ ЗАБОРОНЕНО: Таргетинг на релігію, расу

---

### 9. ТЕХНІЧНА ЯКІСТЬ ТА USER EXPERIENCE

**Якість відео:**
- Роздільна здатність (мінімум 720p рекомендовано)
- ⚠️ Чи не занадто розмите або низької якості?
- ⚠️ Чи немає блимаючих ефектів (епілепсія-небезпечно)?
- ⚠️ Чи не призводить до дискомфорту при перегляді?

**Текст у відео:**
- ⚠️ Facebook рекомендує менше 20% тексту від площі
- Чіткість та читабельність тексту
- Контраст та розмір шрифту

---

### 10. ДОДАТКОВІ РИЗИКИ ТА EDGE CASES

**Специфічні заборони:**
- ⚠️ Контент пов'язаний з COVID-19 (вимагає перевірки фактів)
- ⚠️ Політична реклама (вимагає верифікації)
- ⚠️ Соціальні питання (можуть вимагати disclaimers)
- ⚠️ Продукти для дорослих (навіть легальні можуть бути заборонені)
- ⚠️ Контент про вагітність та батьківство (обмеження)
- ⚠️ Пси/коти в контексті продажу тварин

**Культурна чутливість:**
- ⚠️ Релігійні символи або обряди
- ⚠️ Національні або культурні стереотипи
- ⚠️ Святкування що можуть образити

---

**ФОРМАТ ВІДПОВІДІ (JSON):**
```json
{
  "video_description": {
    "duration_seconds": 0,
    "scene_by_scene": [
      {
        "timestamp": "0:00-0:05",
        "description": "детальний опис сцени",
        "key_elements": ["елемент1", "елемент2"]
      }
    ],
    "visual_content": "повний опис візуального контенту",
    "people": {
      "count": 0,
      "descriptions": ["опис особи 1", "опис особи 2"],
      "age_appropriateness": "всі виглядають 18+ / є сумніви / неможливо визначити",
      "clothing_appropriateness": "відповідає стандартам / потенційні проблеми",
      "actions_and_gestures": ["дія1", "дія2"]
    },
    "objects_products": {
      "main_product": "назва продукту",
      "visible_items": ["item1", "item2"],
      "potentially_problematic": ["проблемний об'єкт якщо є"]
    },
    "on_screen_text": {
      "all_text": ["текст1", "текст2"],
      "claims_made": ["твердження1", "твердження2"],
      "text_to_image_ratio": "приблизно X%"
    },
    "audio_description": {
      "music": "опис музики",
      "music_copyright_risk": "low/medium/high",
      "voiceover": "що говориться",
      "sound_effects": ["ефект1", "ефект2"],
      "language_appropriateness": "чиста мова / є ризики"
    },
    "overall_tone": "детальний опис тону та настрою"
  },

  "brands_trademarks": {
    "detected_brands": [
      {
        "brand_name": "назва бренду",
        "type": "logo/text/product",
        "duration_seconds": 2.5,
        "usage_type": "власний/сторонній/невідомо",
        "potential_issue": true/false
      }
    ],
    "meta_platforms_mentioned": false,
    "competitor_platforms_mentioned": false,
    "celebrity_endorsement": {
      "present": false,
      "details": "деталі якщо присутні"
    },
    "trademark_issues": "опис проблем або 'немає проблем'",
    "brand_usage_ok": true/false,
    "copyright_concerns": "опис занепокоєнь"
  },

  "prohibited_content": {
    "adult_content": {
      "nudity": false,
      "sexually_suggestive": false,
      "focus_on_body_parts": false,
      "revealing_clothing": false,
      "sexual_innuendo": false,
      "details": "деталі якщо щось виявлено"
    },
    "violence_weapons": {
      "weapons_present": false,
      "violence_depicted": false,
      "blood_gore": false,
      "dangerous_activities": false,
      "details": "деталі"
    },
    "discriminatory_content": {
      "racial_stereotypes": false,
      "gender_discrimination": false,
      "age_discrimination": false,
      "religious_insensitivity": false,
      "body_shaming": false,
      "details": "деталі"
    },
    "substances": {
      "tobacco": false,
      "alcohol": false,
      "drugs": false,
      "paraphernalia": false,
      "details": "деталі та тип якщо виявлено"
    },
    "shocking_content": {
      "graphic_imagery": false,
      "disturbing_content": false,
      "fear_inducing": false,
      "details": "деталі"
    }
  },

  "health_medical_claims": {
    "before_after_imagery": false,
    "weight_loss_claims": false,
    "disease_treatment_claims": false,
    "unrealistic_results": false,
    "body_focused_negative": false,
    "prescription_drugs": false,
    "medical_devices": false,
    "fda_claims": false,
    "fear_based_health_messaging": false,
    "specific_issues": [
      {
        "type": "тип проблеми",
        "description": "опис",
        "severity": "low/medium/high/critical"
      }
    ]
  },

  "deceptive_practices": {
    "clickbait": false,
    "misleading_headlines": false,
    "fake_buttons": false,
    "unrealistic_promises": false,
    "fake_scarcity": false,
    "false_testimonials": false,
    "phishing_indicators": false,
    "details": "деталі оманливих практик"
  },

  "personal_attributes_targeting": {
    "targets_health_conditions": false,
    "targets_financial_status": false,
    "targets_personal_hardships": false,
    "implies_knowledge_of_user": false,
    "examples": ["приклади якщо є"]
  },

  "audio_copyright": {
    "copyrighted_music_detected": false,
    "music_recognition": "назва треку якщо впізнано / royalty-free / невідомо",
    "copyright_risk_level": "low/medium/high",
    "offensive_language": false,
    "audio_issues": "деталі проблем"
  },

  "nsfw_check": {
    "safe_for_work": true/false,
    "family_friendly": true/false,
    "age_appropriate_13plus": true/false,
    "specific_concerns": ["concern1", "concern2"],
    "nsfw_reasons": "детальні причини якщо не safe"
  },

  "technical_quality": {
    "resolution_adequate": true/false,
    "text_overlay_percentage": "приблизно X%",
    "flashing_effects": false,
    "viewing_comfort": "комфортно / можливий дискомфорт",
    "accessibility_concerns": "проблеми доступності"
  },

  "facebook_policy_violations": [
    {
      "violation_id": 1,
      "category": "точна назва категорії Meta Policy",
      "policy_section": "назва розділу політики",
      "severity": "low/medium/high/critical",
      "description": "детальний опис порушення",
      "timestamp_seconds": 5.2,
      "specific_frame_description": "що саме на цьому кадрі",
      "why_its_violation": "чому це порушення політики",
      "recommendation": "конкретні кроки для виправлення",
      "alternative_approach": "альтернативний підхід"
    }
  ],

  "compliance_summary": {
    "will_pass_moderation": true/false,
    "confidence_level": 0.95,
    "risk_level": "low/medium/high/critical",
    "approval_probability": "0-100%",
    "overall_assessment": "детальна загальна оцінка (2-3 речення)",
    "critical_blockers": ["блокер1 якщо є"],
    "medium_risks": ["ризик1 якщо є"],
    "low_risks": ["ризик1 якщо є"]
  },

  "feedback": {
    "main_issues": [
      {
        "issue": "проблема",
        "impact": "критичний/високий/середній/низький",
        "must_fix": true/false
      }
    ],
    "required_changes": [
      {
        "change": "що змінити",
        "priority": "критичний/високий/середній",
        "how_to_fix": "як саме виправити"
      }
    ],
    "recommendations": [
      "детальна рекомендація 1",
      "детальна рекомендація 2"
    ],
    "alternative_approaches": [
      "альтернативний підхід 1 з поясненням чому він кращий",
      "альтернативний підхід 2"
    ],
    "best_practices": [
      "best practice 1",
      "best practice 2"
    ]
  },

  "action_items": {
    "immediate_blockers": ["що треба виправити негайно"],
    "recommended_improvements": ["що покращить шанси схвалення"],
    "optional_enhancements": ["що зробить рекламу ще кращою"],
    "resubmission_readiness": "готово до публікації / потребує змін / категорично не готово"
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
