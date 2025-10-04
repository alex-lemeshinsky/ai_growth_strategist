# Chat MVP — Technical Specification (Vibecoding Simplified)

Date: 2025-10-04
Owner: Backend (FastAPI) + Frontend (Flutter) + n8n (generation handler)
Status: Draft for implementation

Goal
Build a minimal chat-based flow that:
- lets the user converse from the frontend
- collects essential brief fields via LLM clarifying questions
- when sufficient info is gathered, returns a final generation prompt + compact brief JSON
- user can then submit that final payload via a separate input to a handler (stub or n8n webhook)

Non-goals (MVP)
- No streaming tokens (can add later)
- No complex branching or vertical presets (keep required fields minimal)
- No video assembly (handled by n8n outside this scope)

1) Minimal Checklist (required fields)
- product_offer (string)
- audience (string)
- objective (enum: install | lead | purchase | signup | traffic)
- platform (enum: tiktok | instagram | youtube)
- format (enum: reels | shorts | tiktok | feed) and/or aspect_ratio (9:16 default)
- duration_s (enum: 6 | 9 | 15 | 30)
- cta (string)

Readiness: brief is considered ready when at least product_offer, audience, objective, platform, duration_s, cta are present.

2) API Contract (Backend)
Base path: /api/v1/chat-mvp

- POST /session
  - Body: { task_id?: string }
  - Return: { session_id: string, created_at: string }
  - Purpose: Creates a new chat session. Optionally ties to an existing Step-1 task for patterns (future usage).

- POST /message
  - Body: { session_id: string, message: string }
  - Return (two modes):
    - Ask mode (need more info):
      {
        "type": "ask",
        "reply": "Уточнення/запитання до користувача",
        "missing_fields": ["objective", "platform"],
        "state": {
          "known": { ...partial fields... },
          "completeness": 0.65
        }
      }
    - Final mode (ready):
      {
        "type": "final",
        "final_prompt": "...готовий промпт для генератора...",
        "brief": {
          "product_offer": "...",
          "audience": "...",
          "objective": "install",
          "platform": "instagram",
          "format": "reels",
          "aspect_ratio": "9:16",
          "duration_s": 15,
          "cta": "Download now"
        },
        "state": { "completeness": 1.0 }
      }
  - Purpose: Accept user message, update state, call LLM planner, return either next question or final deliverable.

- GET /session/{session_id}
  - Return: { messages: [{role, text, ts}], state: { known, completeness, missing_fields } }
  - Purpose: Debug/restore state in frontend.

- POST /submit
  - Body: { session_id: string, final_prompt: string, brief: object }
  - Return: { submitted: true, handler: "queued", job_id?: string }
  - Purpose: Stub for forwarding to n8n (or simply persisting). For MVP, return queued without real dispatch.

3) Data Models (MongoDB)
- chat_sessions
  { session_id, created_at, updated_at, status: "active|final", known: {product_offer?, audience?, objective?, platform?, format?, aspect_ratio?, duration_s?, cta?}, completeness: number }

- chat_messages
  { session_id, role: "user|assistant", text, ts }

Note: MVP doesn’t require indexes beyond session_id; add TTL/indexes later if needed.

4) LLM Planner (Simplified)
Model: Gemini 2.0 (same as stack), response_mime_type=application/json

System prompt (high level):
- You are a creative producer. Your job is to collect only the minimal info needed to create a small creative brief for a short performance video (reels/shorts/tiktok). Ask concise questions. If all required fields are known, output final mode.

Required output JSON schema:
- Ask mode:
  {
    "need_more_info": true,
    "question": "...",
    "missing_fields": ["objective", "platform"],
    "updates": { "objective": "install" } // optional if answer inferred
  }
- Final mode:
  {
    "need_more_info": false,
    "final_prompt": "...",
    "brief": { ...fields... }
  }

Backend logic:
- Merge known fields from session with any new updates LLM proposed.
- If missing fields remain → return type=ask with question.
- If complete → compose final_prompt template (LLM’s or backend’s) and return type=final.

5) Minimal Final Prompt Template (if LLM doesn’t supply one)
Use backend fallback when LLM final_prompt missing:

"""
Create a 15s vertical performance ad script for {platform}/{format}.
Context:
- Product/Offer: {product_offer}
- Audience: {audience}
- Objective: {objective}
- Duration: {duration_s}s
- CTA: {cta}
Deliver:
- Shot list for 3–4 scenes with timecodes
- Voiceover lines
- On-screen text lines
- Hook (0–3s) and placement of CTA
"""

6) Frontend Contract (minimal)
- Create session on mount or user action; store session_id.
- Send user messages to /message and render reply content.
- When response.type=="final" show final_prompt + brief JSON and provide a separate button to POST /submit.
- Optionally show completeness% in UI.

7) Error Handling
- 400: invalid session_id or empty message → { error }
- 500: LLM error → return generic apology and ask to retry (no crash)
- Timeouts: 20–30s LLM timeout, then apology message.

8) Security/Config
- Use existing GOOGLE_API_KEY via env.
- Rate-limit (basic): per session max 60 requests/hour (optional MVP).
- Log only non-sensitive text. No secrets in logs.

9) Acceptance Criteria (MVP)
- Happy path: 3–6 message turns result in final prompt + brief (>= 5 required fields populated).
- Invalid inputs handled without 5xx in most cases.
- Frontend can: create session → chat → receive clarifying question(s) → receive final → submit payload via /submit.

10) Checkpoints & Timeline
- CP1 (0.5–1d): Endpoints /session, /message (echo mode w/o LLM), persistence working.
- CP2 (0.5–1d): Integrate LLM planner (ask/final JSON), minimum checklist enforcement.
- CP3 (0.5d): Final prompt fallback + /submit stub.
- CP4 (0.5d): Frontend wiring, manual E2E test.

11) Test Cases (examples)
- Case A: User starts with “Потрібно відео для застосунку медитації” → LLM asks for objective & platform → user replies → LLM asks for CTA → user replies → final prompt returned.
- Case B: User provides full context in one message → immediate final.
- Case C: Missing_fields loop never ends → after 3 asks, backend chooses default duration_s=15, format per platform.

12) Future (out of MVP)
- Streaming, multiple-choice options, patterns-based suggestions, quick pre-policy, submit to n8n with job_id, session TTL, auth.
