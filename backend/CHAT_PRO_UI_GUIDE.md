# Chat MVP Pro - Enhanced UI Guide

**Date:** 2025-10-04
**File:** `/static/chat_pro.html`
**URL:** `http://localhost:8000/static/chat_pro.html`

## Overview

Enhanced тестовий frontend для Chat MVP Pro з повною підтримкою нових features:
- ✅ Options (quick-click buttons)
- ✅ Suggestions (з patterns або defaults)
- ✅ Policy hints (префлайт попередження)
- ✅ Creative spec display
- ✅ Session history & restore
- ✅ Sidebar з історією чатів

## Features

### 1. **Sidebar з історією чатів**

**Ліва панель показує:**
- Всі попередні сесії (sorted by updated_at desc)
- Для кожної сесії:
  - Назва (перше повідомлення або product_offer)
  - Дата/час останнього оновлення
  - Статус badge (active/final)
  - Completeness indicator

**Функції:**
- Кнопка "Новий чат" вгорі
- Клік на сесію → завантажує всю історію
- Active session підсвічена
- Auto-refresh після кожної відповіді

### 2. **Options (Quick-Click Buttons)**

Коли LLM повертає `state.options`:

```json
{
  "options": ["Instagram", "TikTok", "YouTube"]
}
```

**UI відображає:**
- Сині rounded chips під питанням
- Hover effect з lift
- Клік → автоматично вставляє в input і надсилає

**Use cases:**
- Platform selection
- Objective choice
- Duration selection
- Structure type
- Style type

### 3. **Suggestions (From Patterns)**

Коли LLM повертає `state.suggestions`:

```json
{
  "suggestions": [
    {"text": "Problem-solution hook", "source": "patterns"},
    {"text": "UGC style", "source": "default"}
  ]
}
```

**UI відображає:**
- Помаранчеві boxes під питанням
- Badge показує source:
  - 🎯 "З аналізу" для patterns
  - 💡 "Best practice" для defaults
- Клік → вставляє текст в input (не надсилає автоматично)

### 4. **Policy Hints**

Коли LLM повертає `state.policy_hints`:

```json
{
  "policy_hints": [
    {"text": "💡 Підказка: before/after вимагає disclaimers", "type": "before_after"}
  ]
}
```

**UI відображає:**
- Жовті warning boxes
- Іконка 💡
- Не блокують flow, просто інформують

**Тригери:**
- Health claims
- Before/After statements
- Guarantees
- Music mentions
- Celebrity names

### 5. **Creative Spec Display**

В final mode, коли є `state.creative_spec`:

```json
{
  "creative_spec": {
    "hook": {"type": "problem-solution", "description": "..."},
    "structure": "hook-body-cta",
    "style": {"production": "UGC", "pacing": "dynamic"},
    "voiceover": ["VO line 1", "VO line 2", "VO line 3"],
    "on_screen_text": ["Text 1", "Text 2"],
    "cta_spec": {"text": "...", "timestamp": 12, "urgency": "high"}
  }
}
```

**UI відображає:**
- Зелений блок після brief
- Секції для кожного компонента:
  - Hook (type + description)
  - Structure
  - Style (production + pacing)
  - Voiceover (numbered list)
  - On-screen text (numbered list)
  - CTA spec (text + timing + urgency)

### 6. **Session Management**

**API endpoint:** `GET /api/v1/chat-mvp/sessions`

**Функції:**
- Завантаження всіх сесій при старті
- Створення нової сесії
- Завантаження існуючої сесії з історією
- Auto-refresh після кожного message

**Session item показує:**
```
Додаток доставки їжі
4 жов 14:30        [final]
```

## UI Components

### Colors

**Primary:**
- Purple gradient: `#667eea → #764ba2`
- User messages: `#f093fb → #f5576c`

**Options:**
- Background: `#e3f2fd`
- Border/Text: `#1976d2`

**Suggestions:**
- Background: `#fff3e0`
- Border: `#ff9800`
- Badge patterns: `#4caf50`
- Badge default: `#ff9800`

**Policy Hints:**
- Background: `#fff3cd`
- Border: `#ffc107`
- Text: `#856404`

**Creative Spec:**
- Background: `#e8f5e9`
- Border: `#4caf50`
- Text: `#2e7d32`

### Layout

**Sidebar (280px):**
- Header з кнопкою "Новий чат"
- Scrollable sessions list
- Each session: title + meta + status

**Main chat:**
- Header з session info + completeness
- Progress bar
- Messages area (scrollable)
- Input area з send button

**Responsive:**
- На mobile (<1024px):
  - Sidebar стає horizontal вгорі
  - Max-height: 200px
  - Main chat full width

## Testing Scenarios

### 1. Test Options

```
User: "Хочу зробити відео"
AI: "Для якої платформи?"
Options: [Instagram] [TikTok] [YouTube]

→ Клікни на "Instagram"
→ Автоматично надсилає "Instagram"
```

### 2. Test Suggestions from Patterns

**Prerequisite:** Create session з task_id

```javascript
POST /api/v1/chat-mvp/session
{
  "task_id": "uuid-from-step-1"
}
```

```
User: "Хочу рекламувати додаток"
AI: "Який hook використати?"
Suggestions:
  💡 Problem-solution hook (3-5с) 🎯 З аналізу
  💡 Before/After трансформація 💡 Best practice

→ Клікни на suggestion
→ Текст вставляється в input
→ Натисни Send
```

### 3. Test Policy Hints

```
User: "Реклама таблеток, які лікують головний біль"
AI: "Для якої аудиторії?"
Policy Hints:
  💡 Увага: уникай медичних claims без підтверджень (ризик відхилення)

→ Hint показується але не блокує
→ Можна продовжувати діалог
```

### 4. Test Creative Spec

**Complete full flow (6-8 turns):**

```
1. Product: додаток доставки
2. Audience: молоді професіонали
3. Objective: install
4. Platform: Instagram
5. Duration: 15s
6. CTA: Завантажуй зараз
7. Hook: problem-solution
8. Structure: hook-body-cta
9. Style: UGC

→ Final response shows creative spec:
  ✅ Hook section
  ✅ Structure
  ✅ Style (UGC + dynamic)
  ✅ Voiceover lines (3-4)
  ✅ On-screen text
  ✅ CTA spec
```

### 5. Test Session History

```
1. Створи 3 різні чати
2. Кожен доведи до різних стадій (pending/active/final)
3. Закрий браузер
4. Відкрий знову /static/chat_pro.html
5. Sidebar показує всі 3 сесії
6. Клік на будь-яку → завантажує історію
7. Можна продовжити діалог
```

## API Integration

### Enhanced Response Example

**Ask Mode:**
```json
{
  "type": "ask",
  "reply": "Для якої платформи відео?",
  "missing_fields": ["platform", "duration_s"],
  "state": {
    "known": {"product_offer": "додаток доставки", "audience": "..."},
    "completeness": 0.5,
    "options": ["Instagram", "TikTok", "YouTube"],
    "suggestions": [
      {"text": "Instagram Reels (15s)", "source": "patterns"},
      {"text": "TikTok (9-15s)", "source": "default"}
    ],
    "examples": ["Instagram", "TikTok для Gen Z"],
    "policy_hints": []
  }
}
```

**Final Mode:**
```json
{
  "type": "final",
  "final_prompt": "Детальний prompt...",
  "brief": {
    "product_offer": "...",
    "audience": "...",
    "objective": "install",
    "platform": "instagram",
    "format": "reels",
    "duration_s": 15,
    "cta": "..."
  },
  "state": {
    "completeness": 1.0,
    "creative_spec": {
      "hook": {"type": "problem-solution", "description": "Показати проблему повільної доставки"},
      "structure": "hook-body-cta",
      "style": {"production": "UGC", "pacing": "dynamic"},
      "voiceover": [
        "Чекаєш їжу годинами? (0-3с)",
        "З нашим додатком — 15 хв! (3-10с)",
        "Завантажуй зараз (10-15с)"
      ],
      "on_screen_text": ["Проблема: повільно", "Рішення: 15 хв", "CTA"],
      "cta_spec": {"text": "Завантажуй", "timestamp": 12, "urgency": "high"}
    }
  }
}
```

## Browser Compatibility

**Tested:**
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile Safari (iOS 15+)
- ✅ Chrome Mobile (Android)

**Required features:**
- Fetch API
- ES6 (arrow functions, template literals)
- CSS Grid/Flexbox
- CSS animations

## Performance

**Optimizations:**
- Sessions list cached locally
- Lazy load messages (scroll pagination можна додати)
- Debounce для typing indicator
- Auto-scroll only for new messages

**Limits:**
- Max 100 messages per session (scroll if more)
- Max 20 sessions in sidebar (pagination можна додати)

## Future Enhancements

1. **Streaming responses** (SSE)
2. **Voice input** (Web Speech API)
3. **Copy prompt to clipboard** (one-click)
4. **Export brief as JSON/PDF**
5. **Dark mode toggle**
6. **Search sessions** (by product/date)
7. **Delete sessions**
8. **Edit previous messages**
9. **Fork conversation** (branch from any point)
10. **Share session** (read-only link)

---

## Quick Start

```bash
# 1. Start backend
cd backend
uvicorn src.main:app --reload

# 2. Open browser
http://localhost:8000/static/chat_pro.html

# 3. Click "Новий чат"
# 4. Start conversation!
```

**Готово! Тестуй всі нові features.** 🚀
