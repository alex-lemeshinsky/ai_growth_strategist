# Chat-based Creative Brief (Step-2) — Work Plan and Technical Design

Date: 2025-10-04
Owner: Backend (FastAPI) + n8n (generation pipeline)
Status: Draft for review

Executive summary
- Goal: Add a guided “chat + quiz” that collects all inputs needed to generate high-quality video creatives, with idea suggestions and policy-aware guardrails.
- Output: A finalized VideoGenerationBrief JSON payload ready for Step-2 (n8n) generation pipeline.
- Value: Higher-quality briefs, fewer iterations, safer-by-design content (lower ban risk), faster time-to-ready-to-generate.

Scope
- In-scope: Conversation engine, checklist-driven questioning, dynamic branching, idea suggestions from patterns, policy prechecks, final brief generation, API endpoints, persistence.
- Out-of-scope (owned by other dev): Actual video assembly (n8n pipeline, ffmpeg), hosting of final assets.

User stories
- As a marketer, I want the system to ask me only the necessary questions for my use-case (platform, category, objective) so I don’t waste time.
- As a marketer, I want the system to propose hooks/concepts based on real winning patterns so I can choose quickly.
- As a marketer, I want the system to flag risk areas early (policy) and propose safe alternatives so I avoid bans.
- As a marketer, I want a clear final brief (JSON + human-readable) that can be passed to generation and saved for future runs.

Conversational UX (quiz + ideas)
- Entry: One kickoff prompt initiates a guided session. The system evaluates what is known and asks only missing items.
- Checklist taxonomy (core fields):
  - Product/Offer, Audience (demographic/psychographic), Objective (install/lead/purchase), Platform & Placement (TikTok/IG/YouTube), Format & Aspect (9:16/1:1/16:9), Length (6/9/15/30s), Core value props, Pain points, CTA, Brand voice/tone, Visual style references, Assets (logo, app screens, UGC, disclaimers), Regions/languages, Budget/velocity (optional), Special constraints (regulated: health/finance), Music preferences/licensing.
- Dynamic branching:
  - If platform=IG Reels/TikTok → tighten length, CTA display norms, text safe areas.
  - If regulated category (health/finance/crypto) → add compliance questions (claims, disclaimers).
  - If minors/family content → extra safety and COPPA-like constraints.
  - If music requested → ask licensing source and fallback to royalty-free library.
- Idea suggestions:
  - Pull top 3–5 pattern-driven concepts from Step-1 analysis (hooks/story arcs/visual styles) and offer as selectable starting points.
- Readiness gate:
  - Compute Brief Completeness Score (0–1). If < 0.8, automatically ask only missing/high-impact questions.
  - When >= 0.8, offer “Finalize brief” with explicit summary confirmation.

Data model (core)
- CreativeBriefV1 (final payload to n8n):
  - meta: session_id, created_at, user_id (optional)
  - context: product, offer, audience, objective, platform, placement, locales
  - format: aspect_ratio, target_duration_s, safe_text_margins
  - messaging: pains[], value_props[], brand_voice, mandatory_phrases[], prohibited_phrases[]
  - creative_strategy: hook_choice, narrative_arc, visual_style, pacing, color_palette, typography
  - script: scenes[] with timecodes, voiceover lines, on_screen_text items, cta spec (text, timecodes)
  - assets: logo_url, references[], screen_recordings[], broll[], music_pref, license_source
  - policy_constraints: must_not_show[], must_not_claim[], required_disclaimers[], celebrity_restrictions
  - generation_hints: variants_count, variation_axes (hook/cta/style/length), seed
- Session/Chat persistence:
  - ChatSession: session_id, status (active/ready/finalized), completeness_score, last_missing_fields[]
  - ChatMessage: session_id, role (user/assistant), content, ts
  - ChecklistState: session_id, fields map with values and confidence

API design (FastAPI)
- POST /api/v1/chat/session
  - body: { task_id?: string, seed?: int }
  - returns: { session_id }
- POST /api/v1/chat/message
  - body: { session_id, message }
  - returns: { reply, state: { completeness_score, missing_fields } }
- GET /api/v1/chat/session/{session_id}
  - returns: { transcript, checklist_state, suggestions }
- POST /api/v1/chat/session/{session_id}/finalize
  - body: { confirm: true }
  - returns: { brief: CreativeBriefV1, brief_human_summary, policy_precheck_summary }
- POST /api/v1/generate (owned by n8n webhook)
  - body: { brief: CreativeBriefV1 }
  - returns: { job_id } (n8n handles assembly)
- Optional: WS /api/v1/chat/stream for token streaming.

LLM strategy
- Model: Google Gemini 2.0 (flash/pro) to stay consistent with current stack.
- Structured outputs: response_mime_type=application/json for internal “Planner” tool.
- Roles:
  - Planner: Decides next question or action based on missing fields and risk profile. Output schema {next_action, questions[], suggestions[], updates_to_checklist}.
  - Copywriter: Turns agreed strategy into VO lines and on-screen text.
  - Policy Advisor: Runs pre-policy pass (heuristic) and annotates constraints for brief.
- Guardrails:
  - Deterministic JSON schema validation (pydantic) for every LLM output.
  - Refusal policy for unsafe categories. Early detection routes to human-in-the-loop if needed.

Integrations
- Step-1 (patterns):
  - Endpoint to fetch top patterns for the given vertical/platform from existing task_id or global DB (future).
  - Suggestions merged into “suggestions” field for Planner to present multiple-choice options.
- Step-3 (policy):
  - Pre-policy quick check (LLM heuristic) while chatting.
  - After finalize: auto-run full policy_checker on draft script (optional) and include risks in brief_human_summary.
- Step-2 (n8n):
  - Submit CreativeBriefV1 via webhook. Expect job_id and store it in session.

Checklist and scoring
- Each field has weight by impact on generation quality (e.g., Objective, Platform, Hook, Assets > minor preferences).
- Completeness Score = weighted coverage × confidence.
- Gate at 0.8 to unlock finalize.
- If under threshold, Planner returns max 2 focused questions at a time to reduce fatigue.

Prompt design (high level)
- System: “You are a Performance Creative Producer that asks the minimum questions needed to produce a high-performing, policy-safe creative brief. Use the checklist, reference patterns, and pre-policy rules. Keep questions short, offer examples, and propose options when useful.”
- Planner output JSON (contract):
  { "next_action": "ask|suggest|finalize", "questions": [{id, text, options?}], "suggestions": [{type, text, rationale}], "updates": { field: value }, "missing_fields": [..], "completeness": 0.0 }
- Copywriter prompt: Generates script scenes, VO, on-screen text per decided strategy (language/locales, durations, timing alignment, CTA placement).
- Policy advisor prompt: Highlights risky phrases and proposes safe alternatives inline.

Persistence and models (MongoDB + Pydantic)
- Collections: chat_sessions, chat_messages, chat_checklists, chat_briefs.
- Indexes: session_id, updated_at; for patterns: platform+vertical (future).

Security and compliance
- No secrets in logs. PII minimal. Optional redaction of raw uploads.
- For health/finance: inject mandatory constraints and disclaimers.
- Music/logo use: default to royalty-free unless explicit proof provided.

Readiness criteria (acceptance)
- Chat asks no more than 6–10 turns for a typical case to reach 0.8+ completeness.
- Final brief passes policy precheck with no critical blockers.
- Brief JSON validates against CreativeBriefV1 schema and renders in a human summary.
- n8n can consume brief and produce at least one playable MP4 per variant spec.

Delivery plan (2–3 weeks)
- Wk1
  - Backend: session models, endpoints (/chat/session, /chat/message), LLM Planner prototype.
  - Checklist weights + completeness scoring. Persist state to Mongo.
  - Integrate Step-1 suggestions (from last task_id) in /chat/message responses.
- Wk2
  - Copywriter module to assemble scenes, VO, on-screen text. Policy advisor precheck.
  - Finalize endpoint building CreativeBriefV1. Human summary renderer.
  - n8n webhook contract agreed; smoke test end-to-end with mock assets.
- Wk3
  - UX polish: streaming, batching questions, multiple-choice shortcuts.
  - Quality passes: unit tests for schema, e2e for chat→brief, latency/safety tests.
  - Docs: API reference, operator playbook, example briefs.

Open questions
- Vertical presets: do we ship category templates (e.g., gaming, wellness, fintech)?
- Asset library: do we provide stock/UGC pools or rely on user uploads only?
- Localization: do we enforce language consistency (VO vs on-screen vs policy)?
- KPI proxy: do we include a simple heuristic score to prioritize variants?

Appendix A — CreativeBriefV1 example (truncated)
```json path=null start=null
{
  "meta": {"session_id": "sess_123", "created_at": "2025-10-04T20:00:00Z"},
  "context": {
    "product": "Meditation App",
    "offer": "30-day free trial",
    "audience": {"segment": "Women 25-40, urban, stressed"},
    "objective": "install",
    "platform": "instagram",
    "placement": "reels",
    "locales": ["uk-UA"]
  },
  "format": {"aspect_ratio": "9:16", "target_duration_s": 15, "safe_text_margins": "platform_default"},
  "messaging": {
    "pains": ["work stress", "no time to relax"],
    "value_props": ["5 minutes to calm", "personalized sessions"],
    "brand_voice": "friendly, supportive",
    "mandatory_phrases": [],
    "prohibited_phrases": ["cure", "guaranteed"]
  },
  "creative_strategy": {
    "hook_choice": "Problem → Solution",
    "narrative_arc": "intrigue→problem→solution→desired_result",
    "visual_style": "UGC",
    "pacing": "fast",
    "color_palette": "warm",
    "typography": "platform_default"
  },
  "script": {
    "scenes": [
      {"t": [0,3], "see": "Stressed at desk", "hear": "gentle music"},
      {"t": [3,10], "see": "App demo", "hear": "VO explains benefits"},
      {"t": [10,15], "see": "Smiling user", "hear": "CTA"}
    ],
    "voiceover": [
      {"t": [0,3], "text": "Втомилась від постійного стресу?"},
      {"t": [3,10], "text": "Спробуй 5-хвилинні практики"},
      {"t": [10,15], "text": "Завантажуй зараз — безкоштовно 30 днів"}
    ],
    "on_screen_text": [
      {"t": 1.0, "text": "Втомлена?"}, {"t": 12.0, "text": "Завантажуй зараз"}
    ],
    "cta": {"text": "Download now", "t": 12.0}
  },
  "assets": {
    "logo_url": "https://cdn/logo.png",
    "references": ["task:123/hook:problem-solution"],
    "screen_recordings": ["s3://app-demo-uk.mp4"],
    "broll": [],
    "music_pref": "uplifting",
    "license_source": "royalty_free"
  },
  "policy_constraints": {
    "must_not_show": ["before/after bodies"],
    "must_not_claim": ["guaranteed cure"],
    "required_disclaimers": [],
    "celebrity_restrictions": true
  },
  "generation_hints": {"variants_count": 3, "variation_axes": ["hook", "cta"]}
}
```

Appendix B — Planner JSON (example)
```json path=null start=null
{
  "next_action": "ask",
  "questions": [
    {"id": "objective", "text": "Яка мета кампанії? (інстали, ліди, продажі)", "options": ["install", "lead", "purchase"]},
    {"id": "platform", "text": "Де показувати креатив?", "options": ["tiktok", "instagram", "youtube"]}
  ],
  "suggestions": [
    {"type": "hook", "text": "Проблема→Рішення на 0-3с", "rationale": "перформить у ніші wellness"}
  ],
  "updates": {},
  "missing_fields": ["audience.segment", "assets.logo"],
  "completeness": 0.62
}
```
