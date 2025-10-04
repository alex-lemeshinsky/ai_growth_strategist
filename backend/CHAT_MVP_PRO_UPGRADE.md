# Chat MVP → Chat MVP Pro — Upgrade Guide

**Date:** 2025-10-04
**Status:** ✅ Implemented

## Зміни

### Що покращено:

#### 1. **Extended LLM Response Contract** (Backward Compatible)

**Ask Mode** тепер повертає:
```json
{
  "need_more_info": true,
  "question": "Коротке питання українською",
  "missing_fields": ["objective", "platform"],
  "updates": {"audience": "..."},

  // NEW FIELDS (опційні):
  "options": ["Instagram", "TikTok", "YouTube"],  // Quick-click choices
  "suggestions": [  // From competitor patterns or defaults
    {"text": "Problem-solution hook (3-5с)", "source": "patterns"},
    {"text": "Before/After трансформація", "source": "default"}
  ],
  "examples": ["Приклад 1", "Приклад 2"],  // Example answers
  "policy_hints": [  // Preflight policy warnings
    {"text": "💡 Підказка: before/after вимагає disclaimers", "type": "before_after"}
  ]
}
```

**Final Mode** тепер повертає:
```json
{
  "need_more_info": false,
  "final_prompt": "Детальний prompt...",
  "brief": { /* базові поля */ },

  // NEW FIELD (опційний):
  "creative_spec": {
    "hook": {"type": "problem-solution", "description": "..."},
    "structure": "hook-body-cta",
    "style": {"production": "UGC", "pacing": "dynamic"},
    "voiceover": ["VO line 1 (0-3s)", "VO line 2 (3-8s)", ...],
    "on_screen_text": ["Hook text", "Value prop", "CTA"],
    "cta_spec": {"text": "...", "timestamp": 12, "urgency": "high"}
  }
}
```

---

#### 2. **Patterns Integration** (Step-1 Context)

Якщо `task_id` передано при створенні сесії:

```python
POST /api/v1/chat-mvp/session
{
  "task_id": "uuid-from-step-1-analysis"
}
```

**Planner автоматично:**
- Витягує top hooks, structures, styles, CTAs з Step-1 аналізу
- Підмішує в prompt як `COMPETITOR PATTERNS`
- Пропонує suggestions із `source: "patterns"`

**Приклад:**
```
LLM: "Який hook використати?"
Options: ["Problem-solution", "Before/After", "Question"]
Suggestions: [
  {"text": "Проблема → швидке рішення (як у конкурента X)", "source": "patterns"},
  {"text": "До/Після трансформація (80% ефективність)", "source": "patterns"}
]
```

Без `task_id` → використовуються дефолтні best practices.

---

#### 3. **Creative Fields Collection**

Тепер збираються **3 додаткові поля** (опційно але рекомендовано):

- **hook** (string): Тип/опис хука (перші 3с)
- **structure** (string): Narrative structure (problem-solution, testimonial, etc.)
- **style** (string): Visual style (UGC, screencast, etc.)

**Флоу:**
1. Збирає 6 базових полів (product_offer, audience, objective, platform, duration, cta)
2. Якщо всі базові заповнені → переходить до creative fields
3. Коли все зібрано → повертає `creative_spec` у final mode

---

#### 4. **Policy Hints** (Preflight Warnings)

Автоматично детектує ризикові keywords і додає підказки:

**Ризики:**
- Health claims ("лікує", "виліковує")
- Before/After ("до і після", "результат за")
- Guarantees ("100% гарантія")
- Music rights ("популярна музика")
- Celebrities ("знаменитість")
- Alcohol/Tobacco

**Приклад:**
```
User: "Реклама таблеток, які виліковують головний біль"

Response:
{
  "question": "Для якої аудиторії ці таблетки?",
  "policy_hints": [
    {
      "text": "💡 Увага: уникай медичних claims без підтверджень (ризик відхилення модерацією)",
      "type": "health_claims"
    }
  ]
}
```

---

#### 5. **Enhanced Final Prompt**

Генерує детальний blueprint замість generic prompt:

```
📋 КОНТЕКСТ:
• Продукт: ...
• Аудиторія: ...
• Мета: install
• Тривалість: 15с

🎬 КРЕАТИВНА КОНЦЕПЦІЯ:
• Hook: Problem-solution (0-3с)
• Структура: hook-body-cta
• Стиль: UGC, dynamic pacing

📝 ПОТРІБНО СТВОРИТИ:
1. HOOK (0-3с): опис
2. STRUCTURE: VO line 1, VO line 2...
3. ON-SCREEN TEXT: ["Hook", "Value prop", "CTA"]
4. CTA: text + timestamp + urgency

🎯 ФОКУС НА PERFORMANCE:
• Швидкий хук (перші 3с)
• Чіткий value prop
• Сильний CTA
```

---

## Architecture Changes

### New Files

1. **`src/services/patterns_extractor.py`**
   - `extract_patterns_summary(task_data)` → витягує patterns з Step-1
   - `format_patterns_for_prompt(patterns)` → форматує для LLM
   - `get_default_patterns()` → дефолтні якщо немає task_id

2. **`src/services/chat_planner_helpers.py`**
   - `detect_policy_risks(text, known_fields)` → детекція ризиків
   - `add_policy_hints_to_response(result, ...)` → додає hints
   - `generate_enhanced_final_prompt(brief, creative_spec)` → детальний prompt

### Updated Files

1. **`src/services/chat_planner.py`**
   - `plan_next_step()` тепер приймає `patterns: Optional[Dict]`
   - `_build_prompt()` підмішує patterns або defaults
   - Extended output schema (options/suggestions/examples)

2. **`src/api/chat_routes.py`**
   - `/message` завантажує patterns якщо є task_id
   - `_handle_ask_mode()` прокидає state.options/suggestions/examples/policy_hints
   - `_handle_final_mode()` генерує enhanced prompt з creative_spec

---

## Frontend Integration

### Backward Compatible

Старий фронт продовжить працювати — нові поля опційні.

### Enhanced UX (New Frontend)

#### 1. Render Options as Buttons

```javascript
if (response.state.options) {
  renderOptions(response.state.options); // Quick-click chips
}
```

#### 2. Show Suggestions from Patterns

```javascript
if (response.state.suggestions) {
  suggestions.forEach(s => {
    const badge = s.source === 'patterns' ? '🎯 З аналізу' : '💡 Best practice';
    renderSuggestion(s.text, badge);
  });
}
```

#### 3. Display Policy Hints

```javascript
if (response.state.policy_hints) {
  response.state.policy_hints.forEach(hint => {
    showWarning(hint.text, hint.type); // Yellow banner
  });
}
```

#### 4. Show Creative Spec in Final

```javascript
if (response.state.creative_spec) {
  const spec = response.state.creative_spec;

  // Display hook
  display(`Hook: ${spec.hook.description} (${spec.hook.type})`);

  // Display structure
  display(`Structure: ${spec.structure}`);

  // Display VO lines
  spec.voiceover.forEach(line => display(line));

  // Display CTA spec
  display(`CTA: "${spec.cta_spec.text}" at ${spec.cta_spec.timestamp}s`);
}
```

---

## Testing Examples

### 1. With task_id (Patterns)

```bash
# Create session with task_id
POST /session
{
  "task_id": "abc-123-from-step-1"
}

# First message
POST /message
{
  "session_id": "xyz",
  "message": "Хочу рекламувати додаток доставки"
}

# Response includes patterns:
{
  "question": "Який hook використати?",
  "options": ["Problem-solution", "Before/After", "Question"],
  "suggestions": [
    {"text": "Проблема → швидке рішення (3-5с)", "source": "patterns"},
    {"text": "Before/After трансформація", "source": "patterns"}
  ]
}
```

### 2. Without task_id (Defaults)

```bash
# Create session without task_id
POST /session
{}

# Same flow but suggestions from defaults:
{
  "suggestions": [
    {"text": "UGC style (найефективніший)", "source": "default"},
    {"text": "Screencast (для SaaS)", "source": "default"}
  ]
}
```

### 3. Policy Hints

```bash
POST /message
{
  "message": "Рекламую таблетки, які лікують все"
}

# Response:
{
  "question": "Для кого ці таблетки?",
  "policy_hints": [
    {
      "text": "💡 Увага: уникай медичних claims без підтверджень",
      "type": "health_claims"
    }
  ]
}
```

### 4. Final with Creative Spec

```bash
# After 6-8 turns...
{
  "type": "final",
  "brief": { /* базові поля */ },
  "creative_spec": {
    "hook": {
      "type": "problem-solution",
      "description": "Показати проблему затримки доставки → швидке рішення"
    },
    "structure": "hook-body-cta",
    "style": {"production": "UGC", "pacing": "dynamic"},
    "voiceover": [
      "Чекаєш їжу годинами? (0-3с)",
      "З нашим додатком — доставка за 15 хв! (3-8с)",
      "Завантажуй зараз і отримай знижку 20% (8-15с)"
    ],
    "on_screen_text": ["Проблема: повільна доставка", "Рішення: 15 хв", "CTA: -20%"],
    "cta_spec": {"text": "Завантажуй зараз", "timestamp": 12, "urgency": "high"}
  }
}
```

---

## Performance Impact

### Pros:
- ✅ Більш релевантні пропозиції (patterns from real ads)
- ✅ Швидший flow (quick-click options)
- ✅ Кращий final output (creative_spec → detailed blueprint)
- ✅ Менше policy rejects (preflight hints)

### Cons:
- ⚠️ +1 DB query для завантаження task (якщо є task_id)
- ⚠️ Трохи більший context для LLM (+200-500 tokens patterns)

**Optimization:** Cache patterns у Redis якщо потрібно.

---

## Migration Path

### Phase 1: Backend Only ✅
- Все працює backward compatible
- Фронт отримує нові поля але може їх ігнорувати

### Phase 2: Frontend Upgrade
- Додати рендер options як buttons
- Показувати suggestions з badges
- Display policy hints
- Показувати creative_spec у final

### Phase 3: Polish
- Analytics: track option clicks, suggestion usage
- A/B test: patterns vs defaults effectiveness
- Tune LLM temperature для кращих suggestions

---

## API Docs Update

Додано в `CHAT_MVP_DOCS.md`:

```markdown
## Enhanced Features (v2)

### Ask Response with Options
GET /message може повертати:
- options: Quick-click choices
- suggestions: From patterns or defaults
- examples: Example answers
- policy_hints: Preflight warnings

### Final Response with Creative Spec
- creative_spec: Detailed blueprint
- Enhanced final_prompt with structure
```

---

## Success Criteria

✅ **CP1:** Options/suggestions/examples в ask mode
✅ **CP2:** Patterns integration з task_id
✅ **CP3:** Policy hints + creative_spec
✅ **CP4:** Enhanced prompts

**Acceptance:**
- 3-6 turns до final (як раніше)
- Якщо task_id → хоча б 1-2 suggestions з `source: patterns`
- Policy hints з'являються при ризикових keywords
- Final mode повертає creative_spec якщо зібрані creative fields

---

## Next Steps

Для Production:
1. [ ] Add caching для patterns (Redis)
2. [ ] A/B test patterns vs defaults
3. [ ] Analytics на option clicks
4. [ ] Frontend upgrade для render options/suggestions
5. [ ] Streaming responses (SSE)
6. [ ] Voice input support
7. [ ] Multi-language (EN/UK)

---

**Готово! Chat MVP Pro активний і готовий до тестування.** 🚀
