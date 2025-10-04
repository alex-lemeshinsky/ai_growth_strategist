# Video Policy Compliance API Documentation

## 🎯 Overview

API для перевірки відеокреативів на відповідність рекламним політикам платформ (Facebook/Meta). Використовує Gemini для мультимодального аналізу відео.

---

## 📋 Endpoints

### 1. Check Video Policy (via URL)

**Endpoint:** `POST /api/v1/policy/check-video-url`

**Description:** Перевірка відео на відповідність політиці Facebook Ads за URL.

**Request Body:**
```json
{
  "video_url": "https://example.com/video.mp4",
  "platform": "facebook"
}
```

**Response:**
```json
{
  "success": true,
  "platform": "facebook",
  "result": {
    "video_description": {
      "visual_content": "детальний опис",
      "people": "опис людей",
      "objects_products": ["продукт1", "продукт2"],
      "on_screen_text": ["текст1"],
      "audio_description": "опис аудіо",
      "gestures_actions": ["жест1"],
      "overall_tone": "настрій"
    },
    "brands_trademarks": {
      "detected_brands": ["Brand1"],
      "trademark_issues": "опис проблем",
      "brand_usage_ok": true
    },
    "prohibited_content": {
      "inappropriate_gestures": false,
      "violence_weapons": false,
      "discriminatory_content": false,
      "sexual_content": false,
      "drugs_alcohol_tobacco": false,
      "details": ""
    },
    "audio_copyright": {
      "copyrighted_music": false,
      "offensive_language": false,
      "audio_issues": ""
    },
    "nsfw_check": {
      "safe_for_work": true,
      "nudity": false,
      "shocking_content": false,
      "nsfw_reasons": ""
    },
    "facebook_policy_violations": [
      {
        "category": "Medical Claims",
        "severity": "high",
        "description": "нереалістичні обіцянки схуднення",
        "timestamp_seconds": 5.2,
        "recommendation": "видалити твердження або додати дисклеймер"
      }
    ],
    "compliance_summary": {
      "will_pass_moderation": false,
      "confidence": 0.85,
      "risk_level": "high",
      "overall_assessment": "загальна оцінка"
    },
    "feedback": {
      "main_issues": ["проблема1", "проблема2"],
      "required_changes": ["зміна1", "зміна2"],
      "recommendations": ["рекомендація1"],
      "alternative_approaches": ["підхід1"]
    },
    "metadata": {
      "video_path": "/tmp/video.mp4",
      "platform": "facebook",
      "model": "models/gemini-2.0-flash",
      "analyzed_at": "2025-10-04 15:30:00"
    }
  },
  "text_report": "📋 FACEBOOK ADS POLICY CHECK REPORT\n..."
}
```

---

### 2. Check Video Policy (via Upload)

**Endpoint:** `POST /api/v1/policy/check-video-upload`

**Description:** Перевірка відео на відповідність політиці Facebook Ads через завантаження файлу.

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `video` (file): Відеофайл (mp4, mov, etc.)
  - `platform` (string, optional): Платформа (default: "facebook")

**Response:** Same as check-video-url

**Example (curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/policy/check-video-upload" \
  -F "video=@/path/to/video.mp4" \
  -F "platform=facebook"
```

---

### 3. Get Supported Platforms

**Endpoint:** `GET /api/v1/policy/supported-platforms`

**Description:** Отримати список підтримуваних платформ.

**Response:**
```json
{
  "success": true,
  "platforms": [
    {
      "id": "facebook",
      "name": "Facebook/Meta Ads",
      "description": "Check compliance with Facebook and Instagram advertising policies"
    }
  ]
}
```

---

## 🔍 What Gets Checked

### 1. **Video Description**
- Візуальний контент (кадр за кадром)
- Люди (вигляд, одяг, поведінка)
- Об'єкти та продукти
- Текст на екрані (OCR)
- Аудіо (музика, голос, звуки)
- Жести та дії

### 2. **Brands & Trademarks**
- Виявлені логотипи та бренди
- Несанкціоноване використання торгових марок
- Посилання на компанії

### 3. **Prohibited Content**
- ❌ Непристойні жести
- ❌ Насильство та зброя
- ❌ Дискримінація
- ❌ Сексуальний контент
- ❌ Тютюн, алкоголь, наркотики

### 4. **Audio & Copyright**
- Захищена авторськими правами музика
- Образливі слова
- Невідповідність аудіо та візуалу

### 5. **NSFW Filter**
- Безпечність для перегляду на роботі
- Оголення
- Шокуючий контент

### 6. **Facebook Policy Violations**
- Заборонений контент
- Оманливі практики
- Дискримінація
- Нереалістичні обіцянки
- Медичні твердження без підтвердження
- "До/після" без дисклеймерів
- Залякування
- Фейкові новини

---

## 📊 Severity Levels

| Level | Description |
|-------|-------------|
| `low` | Незначне порушення, легко виправити |
| `medium` | Помірне порушення, потребує уваги |
| `high` | Серйозне порушення, висока ймовірність відхилення |
| `critical` | Критичне порушення, гарантоване відхилення |

---

## 🚦 Risk Levels

| Level | Will Pass? | Action Required |
|-------|------------|-----------------|
| `low` | ✅ Likely | Мінімальні зміни (опційно) |
| `medium` | ⚠️ Maybe | Рекомендовані виправлення |
| `high` | ❌ Unlikely | Обов'язкові зміни |

---

## 💡 Usage Examples

### Python (httpx)
```python
import httpx

# Check video by URL
response = httpx.post(
    "http://localhost:8000/api/v1/policy/check-video-url",
    json={
        "video_url": "https://example.com/ad.mp4",
        "platform": "facebook"
    },
    timeout=120.0
)

result = response.json()

# Check if will pass
will_pass = result["result"]["compliance_summary"]["will_pass_moderation"]
print(f"Will pass moderation: {will_pass}")

# Print violations
for v in result["result"]["facebook_policy_violations"]:
    print(f"[{v['severity']}] {v['category']}: {v['description']}")
```

### JavaScript (fetch)
```javascript
// Check video by URL
const response = await fetch('/api/v1/policy/check-video-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_url: 'https://example.com/ad.mp4',
    platform: 'facebook'
  })
});

const data = await response.json();

if (data.result.compliance_summary.will_pass_moderation) {
  console.log('✅ Video will likely pass');
} else {
  console.log('❌ Video will likely fail');
  console.log('Issues:', data.result.feedback.main_issues);
}
```

### cURL
```bash
# Check by URL
curl -X POST "http://localhost:8000/api/v1/policy/check-video-url" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://example.com/ad.mp4", "platform": "facebook"}'

# Upload file
curl -X POST "http://localhost:8000/api/v1/policy/check-video-upload" \
  -F "video=@my_ad.mp4" \
  -F "platform=facebook"
```

---

## 🧪 Testing

### Interactive Test Script
```bash
# Run interactive test
python test_policy_check.py

# Choose:
# 1. Check video by URL
# 2. Upload video file
```

### Test Flow
1. Вибрати метод (URL або файл)
2. Надати video URL або шлях до файлу
3. Отримати детальний звіт
4. Переглянути JSON з повними результатами

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_google_ai_studio_key

# Optional
GEMINI_MODEL=models/gemini-2.0-flash
```

---

## 📝 Response Fields Explained

### `compliance_summary`
- `will_pass_moderation` (bool): Чи пройде модерацію?
- `confidence` (float 0-1): Впевненість в оцінці
- `risk_level` (string): Рівень ризику (low/medium/high)
- `overall_assessment` (string): Загальний висновок

### `facebook_policy_violations`
Array of violation objects:
- `category` (string): Категорія порушення
- `severity` (string): Рівень серйозності
- `description` (string): Детальний опис
- `timestamp_seconds` (float): Таймкод порушення
- `recommendation` (string): Як виправити

### `feedback`
- `main_issues` (array): Основні проблеми
- `required_changes` (array): Обов'язкові зміни
- `recommendations` (array): Рекомендації
- `alternative_approaches` (array): Альтернативні підходи

---

## 🎯 Best Practices

1. **Перевіряйте ранньо**: Перевіряйте креативи до запуску кампанії
2. **Зверніть увагу на severity**: Виправляйте спочатку critical/high
3. **Читайте recommendations**: Gemini дає конкретні поради
4. **Зберігайте результати**: JSON містить детальну інформацію
5. **Перевіряйте після змін**: Повторно перевірте після виправлень

---

## ⚠️ Limitations

- Підтримується тільки Facebook/Meta (поки що)
- AI аналіз не є офіційною модерацією Facebook
- Результати є рекомендаціями, не гарантіями
- Деякі нюанси політики можуть бути пропущені

---

## 🔮 Future Features

- ✅ Facebook/Meta Ads Policy
- 🔜 Google Ads Policy
- 🔜 TikTok Ads Policy
- 🔜 Batch processing (multiple videos)
- 🔜 Historical tracking
- 🔜 A/B testing recommendations
