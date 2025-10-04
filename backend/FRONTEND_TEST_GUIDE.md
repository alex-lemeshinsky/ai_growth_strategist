# Chat MVP - Frontend Test Guide

## Швидкий старт

### 1. Запустити backend

```bash
cd backend
uvicorn src.main:app --reload
```

### 2. Відкрити тестовий UI

Відкрий в браузері:
```
http://localhost:8000/static/chat_test.html
```

Або через головну сторінку:
```
http://localhost:8000/
```
(там є лінк `chat_test_ui`)

## Що тестувати

### Happy Path (3-6 повідомлень)

**Приклад діалогу:**

1. **User:** "Хочу зробити відео про додаток доставки їжі"
   - **AI:** "Супер! Для якої аудиторії цей додаток?"
   - **Completeness:** ~17%

2. **User:** "Для зайнятих людей 25-40 років у великих містах"
   - **AI:** "Яка мета реклами - встановлення, покупка чи щось інше?"
   - **Completeness:** ~33%

3. **User:** "Встановлення додатку"
   - **AI:** "На якій платформі показувати - TikTok, Instagram чи YouTube?"
   - **Completeness:** ~50%

4. **User:** "Instagram Reels"
   - **AI:** "Яка тривалість відео - 6, 9, 15 чи 30 секунд?"
   - **Completeness:** ~67%

5. **User:** "15 секунд"
   - **AI:** "І останнє - який буде call-to-action?"
   - **Completeness:** ~83%

6. **User:** "Завантажуй зараз і отримай знижку 20%"
   - **AI:** "✅ Готово! Ось твій бриф..."
   - **Completeness:** 100%
   - Показується фінальний бриф + кнопка "Відправити на генерацію"

### Інші тестові сценарії

**Швидкий старт (2 повідомлення):**
```
User: "Відео 15 секунд для Instagram Reels про доставку їжі для молодих професіоналів.
       Мета - завантаження додатка. CTA: Спробуй зараз безкоштовно"
AI: "✅ Готово!" (якщо LLM правильно витягне всі поля)
```

**Поступовий збір:**
```
User: "Хочу рекламу"
AI: "Що саме ти хочеш рекламувати?"
User: "Фітнес-додаток"
AI: "Для кого цей додаток?"
...і так далі
```

## Features UI

### ✅ Реалізовано

1. **Real-time chat** з гарною анімацією
2. **Progress bar** (0-100%) вгорі
3. **Completeness badge** показує прогрес відсотками
4. **Typing indicator** (три крапки) під час відповіді AI
5. **User/Assistant avatars** (👤/🤖)
6. **Timestamps** для кожного повідомлення
7. **Final brief display** з усіма полями
8. **Submit button** для відправки готового брифа
9. **Error handling** з показом помилок
10. **Auto-scroll** до останнього повідомлення
11. **Responsive design** (працює на мобільних)

### Візуальні стани

**Progress Bar:**
- 0-20%: червоний
- 20-50%: помаранчевий
- 50-80%: жовтий
- 80-100%: зелений

**Final Brief Card:**
- Жовтий background (`#fff3cd`)
- Всі поля брифа в структурованому вигляді
- Промпт у monospace шрифті
- Зелена кнопка submit

## Debugging

### Перевірити session в консолі

```javascript
// В Developer Tools Console
console.log('Session ID:', sessionId);
console.log('Current Brief:', currentBrief);
console.log('Current Prompt:', currentPrompt);
```

### Перевірити network requests

1. Відкрий Developer Tools (F12)
2. Таб "Network"
3. Фільтр: XHR
4. Дивись запити до `/api/v1/chat-mvp/`

### Перевірити MongoDB

```javascript
// В MongoDB Compass або mongosh
use ai_growth_strategist

// Дивись сесії
db.chat_sessions.find().pretty()

// Дивись повідомлення
db.chat_messages.find().sort({ts: -1}).limit(20).pretty()
```

## Можливі пробломи

### "Failed to create session"

**Причина:** Backend не запущений або MongoDB не підключена

**Рішення:**
```bash
# Перевір чи запущений backend
curl http://localhost:8000/

# Перевір MongoDB
mongosh
> show dbs
> use ai_growth_strategist
> db.chat_sessions.countDocuments()
```

### "LLM processing failed"

**Причина:** `GOOGLE_API_KEY` не встановлений або невірний

**Рішення:**
```bash
# Перевір .env
cat .env | grep GOOGLE_API_KEY

# Якщо немає, додай:
echo "GOOGLE_API_KEY=your-key-here" >> .env

# Перезапусти backend
```

### CORS errors

**Причина:** Frontend працює не на localhost:8000

**Рішення:** Відкрий через `http://localhost:8000/static/chat_test.html`, а не через file://

## API Endpoints (для ручного тестування)

### 1. Create Session

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/session \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 2. Send Message

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "Хочу рекламувати додаток"
  }'
```

### 3. Get Session State

```bash
curl http://localhost:8000/api/v1/chat-mvp/session/YOUR_SESSION_ID
```

### 4. Submit Brief

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/submit \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "final_prompt": "...",
    "brief": {...}
  }'
```

## UX Details

### Анімації

- **Slide in:** Нові повідомлення з'являються з плавною анімацією
- **Typing dots:** Пульсують під час очікування відповіді
- **Progress bar:** Плавний перехід при зміні прогресу
- **Button hover:** Підняття кнопки при наведенні

### Кольори

- **Primary:** `#667eea` (фіолетовий)
- **Secondary:** `#764ba2` (темно-фіолетовий)
- **User messages:** Градієнт `#f093fb → #f5576c` (рожевий)
- **Success:** `#10b981` (зелений)
- **Warning:** `#ffc107` (жовтий)
- **Error:** `#ef4444` (червоний)

### Типографія

- **Font:** System UI (Apple/Google default)
- **Message text:** 14px
- **Headers:** 20px bold
- **Time:** 11px, напівпрозорий

## Mobile Support

UI адаптивний для мобільних:
- Повідомлення займають до 85% ширини на маленьких екранах
- Inputs збільшені для зручності
- Viewport налаштований для mobile
- Touch-friendly buttons

## Наступні кроки

Для production frontend можна додати:
- [ ] Voice input (Web Speech API)
- [ ] Markdown підтримка в повідомленнях
- [ ] Копіювання промпта в clipboard
- [ ] Експорт брифа як JSON/PDF
- [ ] Історія попередніх сесій
- [ ] Редагування попередніх відповідей
- [ ] Темна тема
- [ ] Локалізація (EN/UK)

---

**Готово! Тестуй на http://localhost:8000/static/chat_test.html** 🚀
