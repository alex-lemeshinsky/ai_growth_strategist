# Chat MVP — API Documentation

**Version:** 1.0.0
**Base Path:** `/api/v1/chat-mvp`
**Date:** 2025-10-04

## Overview

Chat MVP provides a conversational interface for collecting creative brief information through AI-powered clarifying questions. The system guides users through 3-6 message turns to gather all required fields, then returns a complete brief with a generation prompt.

## Architecture

```
User → Frontend → POST /session → Backend → MongoDB (chat_sessions)
                ↓
         POST /message → ChatPlanner (Gemini 2.0) → Ask/Final Mode
                ↓
         GET /session/{id} → Message history + state
                ↓
         POST /submit → n8n webhook (stub in MVP)
```

## Required Brief Fields

All fields must be collected before brief is considered complete:

- **product_offer** (string): Product/service/offer to promote
- **audience** (string): Target audience description
- **objective** (enum): `install | lead | purchase | signup | traffic`
- **platform** (enum): `tiktok | instagram | youtube`
- **duration_s** (integer): `6 | 9 | 15 | 30` seconds
- **cta** (string): Call-to-action text

## Endpoints

### POST /session

Create a new chat session for brief collection.

**Request:**
```json
{
  "task_id": "optional-uuid-from-step-1"
}
```

**Response (200):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-10-04T12:00:00Z"
}
```

**Notes:**
- `task_id` is optional; used to link with Step-1 analysis for context (future feature)
- Session automatically sends initial greeting message

---

### POST /message

Send user message and receive AI response.

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Хочу рекламувати додаток для доставки їжі"
}
```

**Response Types:**

#### Ask Mode (202 Accepted)
When more information is needed:

```json
{
  "type": "ask",
  "reply": "Супер! А для якої аудиторії цей додаток?",
  "missing_fields": ["audience", "objective", "platform", "duration_s", "cta"],
  "state": {
    "known": {
      "product_offer": "додаток для доставки їжі",
      "audience": null,
      "objective": null,
      "platform": null,
      "format": null,
      "aspect_ratio": "9:16",
      "duration_s": null,
      "cta": null
    },
    "completeness": 0.17
  }
}
```

#### Final Mode (200 OK)
When all required fields are collected:

```json
{
  "type": "final",
  "final_prompt": "Створи сценарій 15с вертикального перформанс-відео для instagram/reels...",
  "brief": {
    "product_offer": "додаток для доставки їжі",
    "audience": "зайняті професіонали 25-40 років у великих містах",
    "objective": "install",
    "platform": "instagram",
    "format": "reels",
    "aspect_ratio": "9:16",
    "duration_s": 15,
    "cta": "Завантажуй зараз і отримай знижку 20%"
  },
  "state": {
    "completeness": 1.0
  }
}
```

**Error Responses:**

- **404 Not Found**: Session not found
- **400 Bad Request**: Session already finalized or invalid message
- **500 Internal Server Error**: LLM processing error

---

### GET /session/{session_id}

Get session state with full message history.

**Response (200):**
```json
{
  "messages": [
    {
      "role": "assistant",
      "text": "Привіт! Я допоможу тобі створити бриф...",
      "ts": "2025-10-04T12:00:00Z"
    },
    {
      "role": "user",
      "text": "Хочу рекламувати додаток для доставки їжі",
      "ts": "2025-10-04T12:00:15Z"
    }
  ],
  "state": {
    "known": {
      "product_offer": "додаток для доставки їжі",
      "audience": null,
      ...
    },
    "completeness": 0.17,
    "missing_fields": ["audience", "objective", "platform", "duration_s", "cta"],
    "status": "active"
  }
}
```

**Error Responses:**

- **404 Not Found**: Session not found

---

### POST /submit

Submit finalized brief for processing.

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "final_prompt": "Створи сценарій...",
  "brief": {
    "product_offer": "...",
    "audience": "...",
    "objective": "install",
    "platform": "instagram",
    "format": "reels",
    "aspect_ratio": "9:16",
    "duration_s": 15,
    "cta": "..."
  }
}
```

**Response (200):**
```json
{
  "submitted": true,
  "handler": "queued",
  "job_id": "abc-123-def-456"
}
```

**Notes:**
- MVP version returns `"handler": "queued"` without real processing
- Production version will forward to n8n webhook
- Session must be in FINAL status to submit

**Error Responses:**

- **404 Not Found**: Session not found
- **400 Bad Request**: Session not finalized yet

---

## LLM Planner Logic

The `ChatPlanner` service uses Gemini 2.0 Flash with structured JSON output.

### System Prompt (Simplified)

```
You are a creative producer helping to collect information for a performance video brief.

Ask concise, friendly questions in Ukrainian to gather these required fields:
- product_offer, audience, objective, platform, duration_s, cta

Rules:
1. Ask ONE question at a time
2. Be concise and friendly
3. Extract info from answers and update known fields
4. When ALL required fields filled → switch to final mode
5. Infer defaults when possible (e.g., "Instagram Reels" → platform=instagram, format=reels)
```

### Output Schema

**Ask Mode:**
```json
{
  "need_more_info": true,
  "question": "Запитання українською",
  "missing_fields": ["objective", "platform"],
  "updates": {
    "audience": "зайняті професіонали 25-40"
  }
}
```

**Final Mode:**
```json
{
  "need_more_info": false,
  "final_prompt": "Детальний промпт українською...",
  "brief": { ...all fields... }
}
```

---

## Data Models

### MongoDB Collections

#### `chat_sessions`
```javascript
{
  session_id: String (UUID),
  task_id: String? (optional link to Step-1),
  status: "active" | "final",
  known: {
    product_offer: String?,
    audience: String?,
    objective: "install|lead|purchase|signup|traffic"?,
    platform: "tiktok|instagram|youtube"?,
    format: "reels|shorts|tiktok|feed"?,
    aspect_ratio: "9:16",
    duration_s: Number?,
    cta: String?
  },
  completeness: Number (0.0-1.0),
  missing_fields: [String],
  created_at: DateTime,
  updated_at: DateTime
}
```

#### `chat_messages`
```javascript
{
  session_id: String (UUID),
  role: "user" | "assistant",
  text: String,
  ts: DateTime
}
```

---

## Example Flow

### 1. Create Session

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/session \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "session_id": "abc-123",
  "created_at": "2025-10-04T12:00:00Z"
}
```

### 2. First Message

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "message": "Хочу зробити відео для Instagram Reels про додаток доставки"
  }'
```

**Response:**
```json
{
  "type": "ask",
  "reply": "Чудово! Для якої аудиторії цей додаток?",
  "missing_fields": ["audience", "objective", "duration_s", "cta"],
  "state": {
    "known": {
      "product_offer": "додаток доставки",
      "platform": "instagram",
      "format": "reels"
    },
    "completeness": 0.33
  }
}
```

### 3. Continue Conversation...

(3-6 more turns collecting audience, objective, duration, CTA)

### 4. Final Response

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "message": "15 секунд буде достатньо"
  }'
```

**Response:**
```json
{
  "type": "final",
  "final_prompt": "Створи сценарій 15с вертикального відео для Instagram Reels...",
  "brief": {
    "product_offer": "додаток доставки їжі",
    "audience": "зайняті професіонали 25-40",
    "objective": "install",
    "platform": "instagram",
    "format": "reels",
    "aspect_ratio": "9:16",
    "duration_s": 15,
    "cta": "Завантажуй зараз"
  },
  "state": {
    "completeness": 1.0
  }
}
```

### 5. Submit Brief

```bash
curl -X POST http://localhost:8000/api/v1/chat-mvp/submit \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "final_prompt": "...",
    "brief": {...}
  }'
```

**Response:**
```json
{
  "submitted": true,
  "handler": "queued",
  "job_id": "xyz-789"
}
```

---

## Error Handling

### LLM Errors

If Gemini fails to respond or returns invalid JSON:
- Returns friendly error message to user
- Logs detailed error for debugging
- Suggests user to retry or rephrase

### Timeout

- LLM requests have 30s timeout
- Returns apology message on timeout
- User can retry same message

### Rate Limiting (Future)

- MVP has no rate limiting
- Production should add: 60 requests/hour per session

---

## Security Considerations

1. **API Key**: `GOOGLE_API_KEY` must be in environment
2. **Input Validation**: Messages limited to 2000 chars
3. **Session Validation**: All endpoints verify session exists
4. **No Sensitive Data**: Logs exclude user content (only metadata)
5. **CORS**: Configured for development (`allow_origins=*`), restrict in production

---

## Frontend Integration

### React/Flutter Example

```javascript
// 1. Create session
const { session_id } = await POST('/api/v1/chat-mvp/session', {});

// 2. Send message
const response = await POST('/api/v1/chat-mvp/message', {
  session_id,
  message: userInput
});

if (response.type === 'ask') {
  // Show next question
  setAssistantMessage(response.reply);
  setCompleteness(response.state.completeness);
} else if (response.type === 'final') {
  // Show final brief + submit button
  setFinalPrompt(response.final_prompt);
  setBrief(response.brief);
}

// 3. Submit when ready
await POST('/api/v1/chat-mvp/submit', {
  session_id,
  final_prompt,
  brief
});
```

---

## Testing

### Manual Testing

```bash
# Start server
uvicorn src.main:app --reload

# Test endpoints
curl http://localhost:8000/api/v1/chat-mvp/session
curl http://localhost:8000/api/v1/chat-mvp/message
curl http://localhost:8000/api/v1/chat-mvp/submit
```

### Swagger UI

Visit: `http://localhost:8000/docs`

All endpoints available for interactive testing.

---

## Future Enhancements

- [ ] Streaming token responses (SSE)
- [ ] Link with Step-1 task context
- [ ] Real n8n webhook integration
- [ ] Rate limiting per session
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Brief templates for different verticals

---

## Support

For issues or questions, contact backend team or check:
- `/docs` - Swagger API docs
- `/redoc` - ReDoc API docs
- MongoDB logs for debugging session state
