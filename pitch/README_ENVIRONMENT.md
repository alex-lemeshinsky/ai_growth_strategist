# 🚀 Quick Environment Setup

## TL;DR - Швидкий старт

### Локально (localhost):
```bash
npm run dev  # Використає http://localhost:8000
```

### З ngrok:
```bash
# 1. Запустіть backend + ngrok
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000
ngrok http 8000

# 2. Налаштуйте презентацію (замініть на ваш ngrok URL):
./scripts/setup-ngrok.sh https://abc123.ngrok.io

# 3. Запустіть презентацію:
npm run dev
```

### Для Vercel:
1. Встановіть `NEXT_PUBLIC_API_BASE_URL` у Vercel dashboard
2. `vercel --prod`

---

## ⚡ Швидкі команди

```bash
# Локальна розробка
npm run dev

# Ngrok setup одной командой
./scripts/setup-ngrok.sh https://your-ngrok-url.ngrok.io

# Підготовка HTML файлів
npm run prepare-html

# Продакшен збірка
NEXT_PUBLIC_API_BASE_URL=https://your-domain.com npm run build
```

---

## 📱 Що працює

✅ **Динамічні URL** - больше ніяких хардкоджених localhost  
✅ **Ngrok support** - швидке налаштування для демо  
✅ **Vercel ready** - готовий для деплою  
✅ **Environment variables** - .env.local підтримка  
✅ **HTML injection** - автоматична заміна у статичних файлах  

---

## 🔧 Файли що змінилися

- `src/config/demoLinks.ts` - тепер використує environment змінні
- `public/chat-mvp-demo.html` - додана environment injection  
- `package.json` - нові скрипти для підготовки
- `scripts/prepare-html.js` - заміна плейсхолдерів у HTML
- `scripts/setup-ngrok.sh` - швидке налаштування ngrok

---

## 🆘 Проблеми?

**API не працює**: Перевірте `.env.local` файл  
**HTML не оновився**: Запустіть `npm run prepare-html`  
**Ngrok issues**: Використайте `./scripts/setup-ngrok.sh URL`

Детальна документація: [ENVIRONMENT_CONFIG.md](./ENVIRONMENT_CONFIG.md)