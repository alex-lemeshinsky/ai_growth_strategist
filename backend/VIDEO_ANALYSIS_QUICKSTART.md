# 🎬 Прототип аналізу відео креативів

## Що це робить?

Gemini 1.5 Flash/Pro може аналізувати відео напряму і витягати:

✅ **Хуки** (0-3 сек): тактика, сила, опис  
✅ **Візуальний стиль**: UGC/screencast/motion graphics, ефекти, субтитри  
✅ **Текст на екрані**: OCR з точними таймкодами  
✅ **Показ продукту**: UI demo, ключові фічі, таймкоди  
✅ **CTA**: де з'являється, текст, канали (voice/on-screen/both)  
✅ **Болі/переваги**: що показують у відео  
✅ **Аудіо/музика**: настрій, закадровий голос, звукові ефекти  
✅ **Покадровий сторіборд**: що бачимо і чуємо по сценах  
✅ **Оцінки якості**: hook strength, CTA clarity, product visibility, etc.

## Швидкий старт

### 1. Переконайтеся, що є кешовані відео

```bash
ls -lah .cache/videos/
# У вас є: c76cda2a3490430d.mp4, ec73bdcaa703315d.mp4
```

Якщо немає — запустіть MVP pipeline спочатку:
```bash
uv run python -m src.analysis.cli --input creatives/"Guru Apps_*.json" --mode simple
```

### 2. Встановіть GOOGLE_API_KEY

```bash
export GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Запустіть демо

```bash
python demo_video_analysis.py
```

Це проаналізує перше кешоване відео і покаже:
- Hook (тактика, сила, опис)
- Візуальний стиль (тип, ефекти, субтитри)
- CTA (таймкоди, текст, канали)
- Показ продукту (тип, таймкоди, фічі)
- Оцінки якості
- Резюме

Результат збережеться у `analysis/video_analysis_<hash>.json`

## Аналіз конкретного відео

```bash
python -m src.analysis.video_analyzer path/to/video.mp4 output.json
```

## Приклади використання

### Приклад 1: Batch аналіз усіх відео

```bash
python example_video_analysis.py 2
```

Проаналізує всі відео з `.cache/videos/` і збереже у `analysis/video_analyses/`

### Приклад 2: Порівняння хуків

```bash
python example_video_analysis.py 3
```

Витягне хуки з перших 3 відео і відсортує за силою.

### Приклад 3: Витягти весь текст на екрані

```bash
python example_video_analysis.py 4
```

### Приклад 4: Отримати покадровий сторіборд

```bash
python example_video_analysis.py 5
```

## Формат результату

```json
{
  "hook": {
    "time_start_s": 0.0,
    "time_end_s": 3.0,
    "description": "детальний опис",
    "tactic": "pattern_interrupt / bold_claim / question / demo / problem",
    "strength": 0.8
  },
  "visual_style": {
    "style": "UGC / screencast / motion_graphics / real_footage",
    "effects": ["jump_cuts", "zooms", "transitions"],
    "has_captions": true,
    "caption_style": "bold white text with black outline",
    "color_mood": "bright and energetic"
  },
  "on_screen_text": [
    {"timecode_s": 1.5, "text": "Low Storage?"},
    {"timecode_s": 3.0, "text": "Fix It NOW!"}
  ],
  "product_showcase": {
    "type": "UI demo",
    "timecodes_s": [2.0, 5.5, 10.0],
    "key_features": ["cleanup", "file manager", "battery saver"],
    "clarity_score": 0.8
  },
  "cta": [
    {
      "timecode_s": 12.0,
      "text": "Download Now",
      "channel": "on-screen",
      "strength": 0.9
    }
  ],
  "pains": [
    {"text": "Low storage space", "timecode_s": 1.0}
  ],
  "value_props": [
    {"text": "Free up space in few taps", "timecode_s": 3.5}
  ],
  "audio": {
    "has_voiceover": false,
    "music_mood": "energetic",
    "sound_effects": true
  },
  "storyboard": [
    {
      "scene": 1,
      "time_start_s": 0.0,
      "time_end_s": 3.0,
      "what_we_see": "Phone screen showing low storage warning",
      "what_we_hear": "Upbeat electronic music"
    }
  ],
  "scores": {
    "hook_strength": 0.8,
    "cta_clarity": 0.9,
    "product_visibility": 0.7,
    "message_density": 0.6,
    "execution_quality": 0.8
  },
  "summary": "Strong hook with problem-solution approach. Clear UI demo with multiple CTAs."
}
```

## Інтеграція з MVP pipeline

Щоб додати аналіз відео в основний пайплайн:

```python
from src.analysis.video_analyzer import analyze_video_file

# У mvp_pipeline.py після кешування відео:
if cached_path:
    video_analysis = analyze_video_file(
        cached_path,
        meta={
            "creative_id": ad.ad_archive_id,
            "page_name": ad.page_name,
            "platforms": vf.publisher_platform
        }
    )
    # Використовуй video_analysis для скорингу і ранжування
```

## Примітки

- **Модель за замовчуванням**: `gemini-1.5-flash` (можна змінити через `GEMINI_MODEL`)
- **Розмір відео**: підтримує відео до ~2GB (обмеження Gemini API)
- **Тривалість обробки**: ~10-30 сек на відео залежно від довжини
- **Вартість**: ~$0.00001-0.0001 за відео (Gemini Flash дешевий)
- **Точність**: висока для текстів/UI, середня для складних візуальних ефектів
- **Мови**: розуміє текст на різних мовах (EN/UK/FR/DE/IT/AR/etc)

## Що далі?

1. ✅ **Базовий аналіз відео** — готово (цей прототип)
2. 🔄 **Інтеграція в MVP pipeline** — додати video_analysis до run_mvp()
3. 🔄 **Покращити скоринг** — використати video_analysis для ранжування
4. 📊 **Аналітика по топам** — порівняння хуків/CTA/стилів
5. 🎯 **Рекомендації** — на основі аналізу топових креативів

## Troubleshooting

**Помилка: "GOOGLE_API_KEY is not set"**
```bash
export GOOGLE_API_KEY=your_key_here
```

**Помилка: "Video file not found"**
- Спочатку запустіть MVP pipeline для кешування відео
- Або вкажіть правильний шлях до відео

**Відео занадто довге**
- Gemini Flash підтримує відео до ~1 години
- Для довших — обріжте або використайте Gemini Pro

**JSON parse error**
- Спробуйте без `response_mime_type` (видалити з generation_config)
- Або зменшіть температуру до 0.1
