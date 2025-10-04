# Facebook Ads Library Parser API

FastAPI-based service for extracting Facebook ads data using ApifyClient.

## Features

- Extract creative content, descriptions, publication dates, and metadata from Facebook Ads Library
- RESTful API endpoint for ad parsing
- Structured data models using Pydantic
- Automatic JSON file generation
- URL validation and parameter extraction

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── models.py          # Pydantic models
│   │   └── routes.py          # FastAPI routes
│   ├── services/
│   │   ├── apify_service.py   # Apify client wrapper
│   │   └── data_processor.py  # Data processing logic
│   ├── utils/
│   │   ├── url_parser.py      # URL parsing utilities
│   │   └── file_manager.py    # File operations
│   └── main.py                # FastAPI app entry point
├── creatives/                 # JSON output directory
└── pyproject.toml            # Dependencies
```

## Setup

You can use uv (recommended) or pip.

1. Install dependencies with uv:
```bash
uv sync
```

Or with pip:
```bash
pip install -e .
```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and add your Apify API key:
   ```bash
   cp .env.example .env
   ```

Edit `.env`:
```env
APIFY_API_KEY=your_apify_api_key_here
GOOGLE_API_KEY={{your_gemini_api_key}}
```

## Running the API

```bash
python -m src.main
```

Or with custom host/port:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Video Analysis Prototype 🎬

### Аналіз відео креативу з Gemini Vision

Gemini може аналізувати відео напряму і витягати:
- Хуки (перші 3 сек, тактика, сила)
- Візуальний стиль (UGC, screencast, ефекти, субтитри)
- Текст на екрані (OCR з таймкодами)
- Показ продукту (UI демо, ключові фічі)
- CTA (таймкоди, канали, сила)
- Болі/переваги з відео
- Аудіо/музика
- Покадровий сторіборд
- Оцінки якості

**Швидкий тест на кешованому відео:**
```bash
export GOOGLE_API_KEY={{YOUR_GEMINI_API_KEY}}
python demo_video_analysis.py
```

**Аналіз конкретного відео:**
```bash
python -m src.analysis.video_analyzer path/to/video.mp4 output.json
```

**Примітки:**
- Використовує Gemini 1.5 Flash за замовчуванням (можна змінити через GEMINI_MODEL)
- Відео завантажується в Gemini API (короткочасне зберігання)
- Результат — структурований JSON з усіма деталями
- Працює з будь-якими відео форматами, що підтримує Gemini

---

## MVP Creative Analysis (local JSON + Gemini)

Run the MVP analyzer on a local creatives JSON (no extra backend requests):

Simple (rule-based, no LLM):
```bash
python -m src.analysis.cli --input creatives/"Guru Apps_102120057962217_20251004_152910.json" --window 3:14 --top 3 --mode simple
```

Gemini (optional):
```bash
export GOOGLE_API_KEY={{YOUR_GEMINI_API_KEY}}
python -m src.analysis.cli --input creatives/"Guru Apps_102120057962217_20251004_152910.json" --window 3:14 --top 3 --mode gemini
# add --schema to request strict JSON shaping (may increase errors/token usage)
```

Notes:
- The tool caches videos into `backend/.cache/videos`.

Output: prints a JSON array of top N analyses and writes per-creative files into `backend/analysis/`.

Options:
- `--window A:B` active days window filter (default 3:14)
- `--top N` number of top creatives (default 3)
- `--mode simple|gemini` analysis engine (default simple)
- `--schema` enforce Gemini response schema (Gemini mode only)

## API Usage

### Parse Ads Endpoint

**POST** `/api/v1/parse-ads`

Extract ads from a Facebook Ads Library URL.

**Request Body:**
```json
{
  "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&view_all_page_id=106691191787847",
  "max_results": 15,
  "fetch_all_details": true,
  "output_filename": "my_ads"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully extracted 10 ads",
  "ads_count": 10,
  "output_file": "creatives/SHUBA_106691191787847_20231004_144532.json",
  "ads": [...]
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/api/v1/parse-ads" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&view_all_page_id=106691191787847",
    "max_results": 15
  }'
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/parse-ads",
    json={
        "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&view_all_page_id=106691191787847",
        "max_results": 15,
        "fetch_all_details": True
    }
)

result = response.json()
print(f"Extracted {result['ads_count']} ads")
print(f"Saved to: {result['output_file']}")
```

## Data Model

The API extracts and structures the following data:

- **Ad Identification:** archive_id, page_id, page_name
- **Creative Content:** title, body, caption, link_url
- **Media:** image_urls, video_urls, cards (for carousel ads)
- **Metadata:** start_date, end_date, publisher_platforms
- **Page Info:** page_categories, page_like_count
- **Call-to-Action:** cta_text, cta_type

## File Naming Convention

Output files are automatically named using the pattern:
```
{page_name}_{page_id}_{timestamp}.json
```

Example: `SHUBA_106691191787847_20231004_144532.json`

Custom filenames can be specified using the `output_filename` parameter.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APIFY_API_KEY` | Your Apify API key | Required |
| `APIFY_ACTOR_NAME` | Apify actor to use | `curious_coder/facebook-ads-library-scraper` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `DEFAULT_MAX_RESULTS` | Default max results | `15` |
| `OUTPUT_DIRECTORY` | Output directory | `creatives` |

## Development

### Running Tests

```bash
pytest
```

## Troubleshooting

**Issue:** "APIFY_API_KEY must be provided"
- **Solution:** Ensure `.env` file exists with `APIFY_API_KEY` set

**Issue:** "Invalid Facebook Ads Library URL"
- **Solution:** Verify the URL is from `facebook.com/ads/library/`

**Issue:** No ads returned
- **Solution:** Check if the page/search has active ads in the Ads Library