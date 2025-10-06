# 🔄 HTML Report Regeneration Scripts

Тепер у вас є два скрипти для перегенерації HTML звітів:

## 📋 Доступні скрипти

### 1. **Basic Script** - `regenerate_html_reports.py` 
Простий і надійний скрипт для базової регенерації.

### 2. **Enhanced Script** - `regenerate_html_enhanced.py` ✨
Розширений скрипт з додатковими можливостями.

---

## 🚀 Швидкий старт

### Подивитись що буде перегенеровано (DRY RUN):
```bash
# Basic version
python regenerate_html_reports.py --dry-run --limit 5

# Enhanced version  
python regenerate_html_enhanced.py --dry-run --limit 5
```

### Перегенерувати останні 10 тасків:
```bash
# Basic version
python regenerate_html_reports.py --limit 10

# Enhanced version
python regenerate_html_enhanced.py --limit 10
```

---

## 📊 Порівняння скриптів

| Feature | Basic Script | Enhanced Script |
|---------|-------------|-----------------|
| Базова регенерація | ✅ | ✅ |
| Dry-run режим | ✅ | ✅ |
| Ліміт кількості | ✅ | ✅ |
| Конкретні task IDs | ❌ | ✅ |
| Фільтр за датою | ❌ | ✅ |
| Force режим | ❌ | ✅ |
| Валідація даних | ❌ | ✅ |
| Batch processing | ❌ | ✅ |
| Детальна статистика | ❌ | ✅ |

---

## 🎯 Enhanced Script - Детальні можливості

### Основні опції:
```bash
--limit 10           # Кількість тасків (за замовчанням всі)
--dry-run           # Показати що буде зроблено, не виконувати
--force             # Перегенерувати навіть якщо HTML вже є
```

### Фільтрація:
```bash
--task-ids UUID1 UUID2 UUID3    # Конкретні task ID
--since-days 7                  # Тільки таски за останні 7 днів  
--only-missing                  # Тільки таски без HTML звітів
```

### Обробка:
```bash
--batch-size 5      # Кількість тасків одночасно (за замовчанням 5)
--no-validate       # Пропустити валідацію
```

---

## 📝 Приклади використання

### 1. Перегенерувати конкретні таски:
```bash
python regenerate_html_enhanced.py \
  --task-ids 177e59a6-c960-4b31-9740-231b91be231f f9da824c-44b2-42c0-a8b1-c4d0a44bcc94 \
  --force
```

### 2. Перегенерувати тільки таски без HTML (за останній тиждень):
```bash
python regenerate_html_enhanced.py \
  --only-missing \
  --since-days 7 \
  --limit 20
```

### 3. Force перегенерація останніх 5 тасків:
```bash
python regenerate_html_enhanced.py \
  --force \
  --limit 5 \
  --batch-size 2
```

### 4. Dry run для всіх тасків за останні 3 дні:
```bash
python regenerate_html_enhanced.py \
  --dry-run \
  --since-days 3
```

---

## 🎨 Що покращується при регенерації

✅ **Відео інтеграція:**
- Правильні посилання на стрім відео
- Відображення оригінальних URL відео
- Кешовані відео через API endpoint

✅ **Чат інтеграція:** 
- Task ID для створення чат сесій
- Кнопки "💬 Створити чат"

✅ **Візуальний дизайн:**
- Покращена верстка та стилізація
- Responsive дизайн для мобільних
- Кращі кольори та іконки

✅ **Функціональність:**
- Source URL в заголовку звіту
- Покращена обробка помилок
- Fallback опції для відео

---

## 🔍 Моніторинг та логи

Скрипти виводять детальну інформацію:

```
🚀 Starting enhanced HTML report regeneration
📋 Found 5 tasks to process:
  1. task-id - Page Name (3 creatives) [HTML: ✓]
  2. ...
🔄 Processing batch 1/2 (3 tasks)
📊 Progress: 3/5 tasks processed
🏁 HTML report regeneration completed!
📊 Results:
   ✅ Successfully regenerated: 3
   ⏭️ Skipped (already had HTML): 1  
   ❌ Failed: 1
```

---

## 🆘 Troubleshooting

### Помилка підключення до MongoDB:
```bash
# Перевірте що backend запущений або .env файл правильний
ls -la .env
cat .env | grep MONGO
```

### Таск не знайдено:
```bash
# Перевірте що task_id правильний
python regenerate_html_enhanced.py --dry-run --task-ids YOUR_TASK_ID
```

### Помилка валідації:
```bash
# Використайте --force щоб пропустити валідацію
python regenerate_html_enhanced.py --task-ids YOUR_TASK_ID --force --no-validate
```

---

## 💡 Рекомендації

### Для щоденного використання:
```bash
# Перегенерувати тільки нові таски без HTML
python regenerate_html_enhanced.py --only-missing --limit 10
```

### Для оновлення після змін в коді:
```bash
# Force регенерація останніх тасків
python regenerate_html_enhanced.py --force --limit 5
```

### Для дебагу конкретного таску:
```bash
# Dry run + конкретний task
python regenerate_html_enhanced.py --dry-run --task-ids YOUR_TASK_ID
```

---

## 🎯 Коли використовувати який скрипт

**Basic Script** - коли потрібно:
- Швидко перегенерувати останні N тасків
- Простий і надійний процес  
- Мінімальний вивід інформації

**Enhanced Script** - коли потрібно:
- Точний контроль над тим, що регенерується
- Детальна статистика та моніторинг
- Валідація та перевірка даних
- Batch processing великої кількості тасків
- Фільтрація за різними критеріями