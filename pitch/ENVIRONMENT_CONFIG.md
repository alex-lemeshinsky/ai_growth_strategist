# 🌍 Environment Configuration Guide

Тепер презентація підтримує змінні середовища для налаштування API URL. Це дозволяє легко переключатися між різними серверами без редагування коду.

## 🚀 Швидкий старт

### 1. Локальна розробка (за замовчанням):
```bash
# Використовує http://localhost:8000
npm run dev
```

### 2. З ngrok тунелем:
```bash
# 1. Створіть .env.local файл:
echo "NEXT_PUBLIC_API_BASE_URL=https://your-ngrok-id.ngrok.io" > .env.local

# 2. Запустіть презентацію:
npm run dev:ngrok
```

### 3. Для продакшена:
```bash
# 1. Встановіть змінну для продакшен сервера:
export NEXT_PUBLIC_API_BASE_URL=https://your-production-domain.com

# 2. Зібліть проект:
npm run build:production

# 3. Запустіть:
npm run start
```

---

## 📝 Конфігурація

### Environment Files

1. **`.env.local`** - для локальної розробки:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

2. **`.env.ngrok`** - для ngrok тунелів:
```bash
NEXT_PUBLIC_API_BASE_URL=https://abc123.ngrok.io
```

3. **`.env.production`** - для продакшена:
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.your-domain.com
```

### Priority Order
1. Environment variables (найвищий пріоритет)
2. `.env.local` файл
3. `http://localhost:8000` (fallback)

---

## 🔧 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Локальна розробка з localhost:8000 |
| `npm run dev:ngrok` | Розробка з підготовкою HTML для ngrok |
| `npm run build` | Збірка з підготовкою HTML |
| `npm run build:production` | Продакшен збірка |
| `npm run prepare-html` | Підготовка HTML файлів з environment змінними |

---

## 🌐 Ngrok Setup Example

### 1. Запустіть backend:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Запустіть ngrok:
```bash
ngrok http 8000
```

### 3. Скопіюйте ngrok URL і створіть .env.local:
```bash
# Замініть на ваш ngrok URL
echo "NEXT_PUBLIC_API_BASE_URL=https://abc123-def456.ngrok.io" > .env.local
```

### 4. Запустіть презентацію:
```bash
npm run dev:ngrok
```

---

## 📦 Deployment на Vercel

### 1. Налаштуйте environment variables у Vercel:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com
```

### 2. Додайте у vercel.json:
```json
{
  "env": {
    "NEXT_PUBLIC_API_BASE_URL": "@api-base-url"
  }
}
```

### 3. Deploy:
```bash
vercel --prod
```

---

## 🔍 Що змінилося

### До:
- Хардкоджений `http://localhost:8000` у всіх файлах
- Потрібно було вручну міняти URL для різних серверів

### Після:
- ✅ Динамічний API URL з environment змінних
- ✅ Підтримка множинних середовищ
- ✅ Автоматична заміна у HTML файлах
- ✅ Готовність до деплою на Vercel/Netlify

### Файли що оновилися:
- `src/config/demoLinks.ts` - додав getApiBaseUrl()
- `public/chat-mvp-demo.html` - додав environment injection
- `package.json` - нові скрипти
- `scripts/prepare-html.js` - скрипт заміни плейсхолдерів

---

## 🆘 Troubleshooting

### Проблема: API не працює після зміни URL
```bash
# Перевірте чи правильний URL:
echo $NEXT_PUBLIC_API_BASE_URL

# Перезапустіть сервер:
npm run dev:ngrok
```

### Проблема: HTML файл не оновився
```bash
# Запустіть prepare-html окремо:
npm run prepare-html
```

### Проблема: Environment змінні не підхоплюються
```bash
# Перевірте .env.local файл:
cat .env.local

# Переконайтесь що змінна починається з NEXT_PUBLIC_:
grep NEXT_PUBLIC .env.local
```

---

## 💡 Best Practices

1. **Ніколи не коммітьте .env.local** з реальними URL
2. **Використовуйте .env.example** як шаблон
3. **Тестуйте** кожне середовище перед деплоем
4. **Документуйте** всі environment змінні для команди