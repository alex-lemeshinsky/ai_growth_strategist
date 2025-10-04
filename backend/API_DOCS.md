# AI Growth Strategist API Documentation

## 🚀 Overview

Backend API для аналізу відеокреативів конкурентів з Facebook Ads Library. Використовує Apify для парсингу та Gemini для мультимодального аналізу відео.

## 📋 Endpoints

### 1. Parse Ads from Facebook Ads Library

**Endpoint:** `POST /api/v1/parse-ads`

**Description:** Створює задачу для парсингу рекламних креативів з Facebook Ads Library.

**Request Body:**
```json
{
  "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&media_type=video&q=...",
  "max_results": 15,
  "fetch_all_details": true,
  "auto_analyze": true
}
```

**Parameters:**
- `url` (required): Facebook Ads Library URL
- `max_results` (default: 15): Maximum number of ads to extract (1-100)
- `fetch_all_details` (default: true): Fetch full creative details
- `auto_analyze` (default: true): **Automatically start video analysis after parsing**

**Response:**
```json
{
  "success": true,
  "task_id": "uuid-here",
  "message": "Task created. Use GET /task/{task_id} to check status.",
  "status": "pending"
}
```

**Status Flow:**
- With `auto_analyze=true` (default): `pending` → `parsing` → `parsed` → `analyzing` → `completed` / `failed`
- With `auto_analyze=false`: `pending` → `parsing` → `parsed` / `failed`

---

### 2. Get All Tasks

**Endpoint:** `GET /api/v1/tasks`

**Description:** Отримати список всіх задач з пагінацією.

**Query Parameters:**
- `skip` (int, default: 0) - Кількість задач для пропуску
- `limit` (int, default: 20, max: 100) - Максимум задач на сторінку
- `status` (string, optional) - Фільтр по статусу (`pending`, `parsing`, `parsed`, `analyzing`, `completed`, `failed`)

**Example:**
```bash
GET /api/v1/tasks?skip=0&limit=20&status=parsed
```

**Response:**
```json
{
  "success": true,
  "total": 42,
  "skip": 0,
  "limit": 20,
  "tasks": [
    {
      "task_id": "uuid-here",
      "url": "...",
      "status": "parsed",
      "page_name": "Brand Name",
      "page_id": "123456",
      "total_ads": 15,
      "creatives_file": "creatives/Brand_123456_20251004_143000.json",
      "created_at": "2025-10-04T14:30:00Z",
      "updated_at": "2025-10-04T14:35:00Z"
    }
  ]
}
```

---

### 3. Get Task Details

**Endpoint:** `GET /api/v1/task/{task_id}`

**Description:** Отримати детальну інформацію про конкретну задачу.

**Response:**
```json
{
  "success": true,
  "task": {
    "task_id": "uuid-here",
    "url": "...",
    "status": "completed",
    "page_name": "Brand Name",
    "total_ads": 5,
    "creatives_analyzed": [
      {
        "creative_id": "ad_archive_id",
        "page_name": "Brand",
        "hook": {
          "time_start_s": 0.0,
          "time_end_s": 3.0,
          "description": "...",
          "tactic": "bold claim",
          "strength": 0.8
        },
        "scores": {
          "hook_strength": 0.8,
          "cta_clarity": 0.9,
          "product_visibility": 0.7,
          "message_density": 0.6,
          "execution_quality": 0.8
        },
        "summary": "..."
      }
    ],
    "aggregated_analysis": {
      "pain_points": ["біль1", "біль2"],
      "concepts": ["концепт1", "концепт2"],
      "visual_trends": {
        "style": "UGC",
        "effects": ["jump cuts", "zooms"]
      },
      "hooks": ["хуи1", "хуи2"],
      "core_idea": "...",
      "theme": "...",
      "message": "...",
      "recommendations": "...",
      "video_prompt": "..."
    },
    "html_report": "<html>...</html>",
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

### 4. Analyze Creatives

**Endpoint:** `POST /api/v1/analyze-creatives/{task_id}`

**Description:** Запускає аналіз відеокреативів для задачі в статусі `parsed`.

**Validation:**
- Задача повинна існувати
- Статус повинен бути `parsed`
- Повинні бути знайдені креативи (`total_ads > 0`)
- Аналіз ще не виконаний

**Response:**
```json
{
  "success": true,
  "message": "Analysis started for 5 ads. Check task status for progress.",
  "task_id": "uuid-here",
  "total_ads": 5,
  "status": "analyzing"
}
```

**Status Flow:** `parsed` → `analyzing` → `completed` / `failed`

---

### 5. Health Check

**Endpoint:** `GET /api/v1/health`

**Description:** Перевірка стану API.

**Response:**
```json
{
  "status": "healthy",
  "service": "Facebook Ads Parser API"
}
```

---

## 🔄 Complete Pipeline Flow

### Step 1: Parse Ads
```bash
curl -X POST http://localhost:8000/api/v1/parse-ads \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/ads/library/?...",
    "max_results": 5
  }'

# Response: {"task_id": "abc-123", "status": "pending"}
```

### Step 2: Monitor Parsing
```bash
# Check status every 5 seconds
curl http://localhost:8000/api/v1/task/abc-123

# Wait for status: "parsed"
```

### Step 3: Start Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze-creatives/abc-123

# Response: {"success": true, "status": "analyzing"}
```

### Step 4: Monitor Analysis
```bash
# Check status every 10 seconds
curl http://localhost:8000/api/v1/task/abc-123

# Wait for status: "completed"
```

### Step 5: Get Results
```bash
curl http://localhost:8000/api/v1/task/abc-123 | jq '.task.aggregated_analysis'
```

---

## 🧪 Testing

### Automated Test Script

```bash
# Run full pipeline test
python test_full_pipeline.py
```

Скрипт автоматично:
1. Створює задачу парсингу
2. Чекає завершення парсингу
3. Запускає аналіз
4. Чекає завершення аналізу
5. Виводить результати

### Manual Testing with cURL

```bash
# 1. Create parse task
TASK_ID=$(curl -X POST http://localhost:8000/api/v1/parse-ads \
  -H "Content-Type: application/json" \
  -d '{"url": "YOUR_URL", "max_results": 5}' | jq -r '.task_id')

echo "Task ID: $TASK_ID"

# 2. Wait and check status
watch -n 5 "curl -s http://localhost:8000/api/v1/task/$TASK_ID | jq '.task.status'"

# 3. Start analysis (when status is "parsed")
curl -X POST http://localhost:8000/api/v1/analyze-creatives/$TASK_ID

# 4. Get final results
curl http://localhost:8000/api/v1/task/$TASK_ID | jq '.task.aggregated_analysis'
```

---

## 🔧 Environment Variables

```bash
# Required
APIFY_API_KEY=your_apify_key
GOOGLE_API_KEY=your_google_ai_studio_key

# Optional
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=ai_growth_strategist
GEMINI_MODEL=models/gemini-2.0-flash
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📊 Task Statuses

| Status | Description |
|--------|-------------|
| `pending` | Задача створена, очікує обробки |
| `parsing` | Парсинг FB Ads Library в процесі |
| `parsed` | Парсинг завершено, готово до аналізу |
| `analyzing` | Аналіз відео в процесі |
| `completed` | Аналіз завершено успішно |
| `failed` | Помилка при виконанні |

---

## 🎬 Video Analysis Details

Для кожного відеокреативу аналізується:

- **Hook (0-3s):** Тактика, сила, опис
- **Візуальний стиль:** UGC/screencast/motion graphics, ефекти, субтитри
- **Текст на екрані:** OCR з таймкодами
- **Показ продукту:** Тип, таймкоди, ключові фічі
- **CTA:** Текст, таймкод, канал (on-screen/voice)
- **Болі/Value Props:** З таймкодами
- **Музика/Звук:** Настрій, закадровий голос, звукові ефекти
- **Сторіборд:** Покадровий розбір сцен
- **Оцінки (0-1):** Hook strength, CTA clarity, Product visibility, Message density, Execution quality

---

## 🚀 Quick Start

1. **Start server:**
```bash
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Test pipeline:**
```bash
python test_full_pipeline.py
```

3. **View docs:**
```
http://localhost:8000/docs
```

---

## 📝 Notes

- Apify actor може працювати 2-5 хвилин залежно від кількості ads
- Gemini аналіз відео займає ~30-60 секунд на креатив
- Відео кешується в `.cache/videos/` для повторного використання
- Результати зберігаються в MongoDB + JSON файли в `creatives/`
