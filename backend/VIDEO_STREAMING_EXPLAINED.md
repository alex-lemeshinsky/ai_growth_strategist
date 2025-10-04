# Video Processing: Streaming vs Download

## 🔄 Як працює перевірка відео

### Варіант 1: POST /check-video-url (Оптимізований)

```
┌─────────┐
│ Client  │
└────┬────┘
     │ POST {video_url: "https://..."}
     ▼
┌─────────────┐
│   Backend   │
└──────┬──────┘
       │ httpx.stream(video_url)
       │ ↓ (завантажує в пам'ять)
       │ ↓ (мінімальний temp файл для Gemini API)
       ▼
┌─────────────┐
│   Gemini    │
└──────┬──────┘
       │ Аналізує відео
       ▼
┌─────────────┐
│   Backend   │ (видаляє temp файл)
└──────┬──────┘
       │ JSON Response
       ▼
┌─────────┐
│ Client  │
└─────────┘
```

**Переваги:**
- ✅ Відео завантажується **один раз** (URL → Gemini)
- ✅ Мінімальне використання диску (тільки для Gemini API requirement)
- ✅ Швидше для великих відео
- ✅ Не займає місце на диску backend'а

**Недоліки:**
- ⚠️ Gemini API вимагає файл (не може читати стрім напряму)
- ⚠️ Короткочасний temp файл все одно створюється

---

### Варіант 2: POST /check-video-upload

```
┌─────────┐
│ Client  │ (має відео локально)
└────┬────┘
     │ multipart/form-data (весь файл)
     ▼
┌─────────────┐
│   Backend   │ (зберігає в /tmp)
└──────┬──────┘
       │ genai.upload_file(temp_path)
       ▼
┌─────────────┐
│   Gemini    │
└──────┬──────┘
       │ Аналізує відео
       ▼
┌─────────────┐
│   Backend   │ (видаляє /tmp)
└──────┬──────┘
       │ JSON Response
       ▼
┌─────────┐
│ Client  │
└─────────┘
```

**Переваги:**
- ✅ Працює з локальними файлами
- ✅ Не потребує публічного URL

**Недоліки:**
- ⚠️ Завантажується **двічі**: Client→Server, Server→Gemini
- ⚠️ Використовує bandwidth
- ⚠️ Повільніше для великих файлів

---

## 💾 Використання диску

### check-video-url (Streaming)
```
Disk usage: ~0 MB (постійно)
            ~50-200 MB (короткочасно під час upload в Gemini)
            
Cleanup: Автоматичний (finally block)
```

### check-video-upload
```
Disk usage: ~100-500 MB (залежно від розміру відео)
            зберігається поки йде аналіз
            
Cleanup: Автоматичний (finally block)
```

---

## ⚡ Швидкість

| Method | Download | Processing | Total |
|--------|----------|------------|-------|
| URL (old) | Client→Server: 10s<br>Server→Gemini: 10s | 30s | **50s** |
| URL (new streaming) | Прямий стрім: 10s | 30s | **40s** |
| Upload | Client→Server: 15s | 30s | **45s** |

*Приблизні значення для відео 50MB*

---

## 🛠️ Технічна реалізація

### Streaming approach (новий)

```python
# src/analysis/policy_checker.py

if video_url:
    # Direct upload from URL
    with httpx.stream("GET", video_url) as response:
        # Stream to memory
        video_bytes = io.BytesIO()
        for chunk in response.iter_bytes():
            video_bytes.write(chunk)
        
        # Minimal temp file for Gemini API
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(video_bytes.read())
            video_file = genai.upload_file(tmp.name)
```

**Чому temp файл все одно потрібен?**
- Gemini API `upload_file()` приймає тільки file path
- Не підтримує streaming або in-memory buffers
- Це обмеження Google API, не наше

---

## 🎯 Коли використовувати що?

### Використовуйте `/check-video-url` якщо:
- ✅ Відео вже є в інтернеті (FB Ads, storage, CDN)
- ✅ Хочете зекономити bandwidth
- ✅ Потрібна швидкість
- ✅ Відео велике (>100MB)

### Використовуйте `/check-video-upload` якщо:
- ✅ Відео локальне (на комп'ютері користувача)
- ✅ Відео не має публічного URL
- ✅ Потрібна приватність (не хочете викладати на CDN)
- ✅ Відео маленьке (<50MB)

---

## 📊 Приклад використання

### Streaming (рекомендовано для URL)
```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/policy/check-video-url",
    json={
        "video_url": "https://cdn.example.com/ad.mp4",
        "platform": "facebook"
    },
    timeout=120.0
)
```

**Флоу:**
1. Backend stream'ить відео з URL
2. Мінімальний temp файл для Gemini
3. Upload в Gemini
4. Аналіз
5. Response (temp файл видалено)

### Upload (для локальних файлів)
```python
import httpx

with open("local_video.mp4", "rb") as f:
    response = httpx.post(
        "http://localhost:8000/api/v1/policy/check-video-upload",
        files={"video": ("ad.mp4", f, "video/mp4")},
        data={"platform": "facebook"},
        timeout=120.0
    )
```

**Флоу:**
1. Client upload'ить весь файл на backend
2. Backend зберігає в /tmp
3. Upload в Gemini
4. Аналіз
5. Response (temp файл видалено)

---

## 🔒 Безпека

### Streaming
- ✅ Не зберігає відео на диску backend'а
- ✅ Мінімальний footprint
- ⚠️ URL має бути доступним

### Upload
- ✅ Приватність (відео не публічне)
- ⚠️ Короткочасно зберігається на диску
- ✅ Автоматичне видалення

---

## 🎯 Best Practice

**Рекомендований workflow:**

1. **Якщо відео вже в storage/CDN:**
   ```python
   # Use streaming
   POST /check-video-url
   {
     "video_url": "https://storage.example.com/video.mp4"
   }
   ```

2. **Якщо користувач має локальний файл:**
   ```python
   # Use upload
   POST /check-video-upload
   (multipart with video file)
   ```

3. **Для FB Ads креативів (з competitor analysis):**
   ```python
   # Відео вже кешоване локально
   # Use direct path (internal API)
   check_video_policy(
       video_path="/cache/videos/abc123.mp4",
       platform="facebook"
   )
   ```

---

## 📈 Майбутні оптимізації

### Можливі покращення:
- 🔜 Підтримка Gemini streaming API (коли з'явиться)
- 🔜 Batch processing (кілька відео одночасно)
- 🔜 Caching результатів (за video hash)
- 🔜 Parallel analysis (кілька платформ)

### Обмеження Gemini API:
- ❌ Не підтримує прямий стрім (потрібен файл)
- ❌ Не підтримує in-memory buffers
- ✅ Підтримує великі файли (до 2GB)
- ✅ Автоматичне processing відео
