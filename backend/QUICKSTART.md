# Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies

```bash
cd backend
pip install -e .
```

### 2. Configure API Key

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Apify API key:
```env
APIFY_API_KEY=your_actual_apify_key_here
```

> Get your API key from: https://console.apify.com/account/integrations

### 3. Start the Server

```bash
python -m src.main
```

Server starts at: http://localhost:8000

## Test the API

### Option 1: Web Browser

Open the interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: cURL

```bash
curl -X POST "http://localhost:8000/api/v1/parse-ads" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&view_all_page_id=106691191787847",
    "max_results": 5
  }'
```

### Option 3: Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/parse-ads",
    json={
        "url": "https://www.facebook.com/ads/library/?view_all_page_id=106691191787847",
        "max_results": 5
    }
)

print(response.json())
```

### Option 4: Test Script

```bash
python test_api.py
```

## What Happens?

1. API receives Facebook Ads Library URL
2. Calls Apify actor to scrape ads
3. Processes and structures the data
4. Saves JSON file to `creatives/` directory
5. Returns structured response with ads data

## Output Files

Files are saved in `creatives/` directory:

```
creatives/
└── SHUBA_106691191787847_20231004_144532.json
```

Each file contains array of ad objects with:
- Creative content (text, images, videos)
- Publication dates
- Platform targeting
- Page information
- Call-to-action details

## Example Response

```json
{
  "success": true,
  "message": "Successfully extracted 5 ads",
  "ads_count": 5,
  "output_file": "creatives/SHUBA_106691191787847_20231004_144532.json",
  "ads": [
    {
      "ad_archive_id": "1278360484326626",
      "page_name": "SHUBA",
      "body": "3 головні ознаки, як вибрати справді якісний фарш",
      "image_urls": [
        "https://scontent.fmvd4-1.fna.fbcdn.net/..."
      ],
      "start_date": "2025-09-30T07:00:00",
      "publisher_platform": ["FACEBOOK", "INSTAGRAM"]
    }
  ]
}
```

## Troubleshooting

**Port already in use?**
```bash
# Use different port
API_PORT=8080 python -m src.main
```

**Missing API key?**
```bash
# Check .env file exists and has APIFY_API_KEY set
cat .env
```

**Import errors?**
```bash
# Reinstall dependencies
pip install -e . --force-reinstall
```

## Next Steps

- Read full documentation: [README.md](README.md)
- View implementation details: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- Check development plan: [docs/apify_ads_api_development_plan.md](docs/apify_ads_api_development_plan.md)

## Development Mode

Run with auto-reload on code changes:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, consider:
- Setting up nginx reverse proxy
- Using gunicorn with uvicorn workers
- Implementing rate limiting
- Adding authentication
- Setting up monitoring/logging
