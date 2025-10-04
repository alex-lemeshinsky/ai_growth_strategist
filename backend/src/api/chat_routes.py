"""
API routes for Chat MVP - conversational brief collection.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import uuid
from datetime import datetime

from src.db import MongoDB
from src.db.models import (
    ChatSession,
    ChatMessage,
    ChatSessionStatus,
    BriefState
)
from src.services.chat_planner import (
    ChatPlanner,
    calculate_completeness,
    get_missing_fields,
    is_brief_complete
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize planner (singleton)
planner = ChatPlanner()


# ============================================================================
# Request/Response Models
# ============================================================================

class CreateSessionRequest(BaseModel):
    """Request to create new chat session."""
    task_id: Optional[str] = Field(None, description="Optional task_id to link with Step-1 analysis")


class CreateSessionResponse(BaseModel):
    """Response with new session details."""
    session_id: str
    created_at: str


class SendMessageRequest(BaseModel):
    """Request to send message in session."""
    session_id: str
    message: str = Field(..., min_length=1, max_length=2000)


class AskResponse(BaseModel):
    """Response when more info is needed."""
    type: str = "ask"
    reply: str
    missing_fields: List[str]
    state: Dict[str, Any]


class FinalResponse(BaseModel):
    """Response when brief is complete."""
    type: str = "final"
    final_prompt: str
    brief: Dict[str, Any]
    state: Dict[str, Any]


class MessageHistoryItem(BaseModel):
    """Single message in history."""
    role: str
    text: str
    ts: str


class SessionStateResponse(BaseModel):
    """Session state with history."""
    messages: List[MessageHistoryItem]
    state: Dict[str, Any]


class SubmitRequest(BaseModel):
    """Request to submit final brief."""
    session_id: str
    final_prompt: str
    brief: Dict[str, Any]


class SubmitResponse(BaseModel):
    """Response after submission."""
    submitted: bool
    handler: str
    job_id: Optional[str] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/session", response_model=CreateSessionResponse, summary="Create new chat session")
async def create_session(request: CreateSessionRequest):
    """
    Create a new chat session for brief collection.

    Optionally link to existing Step-1 task for context.
    """
    try:
        session_id = str(uuid.uuid4())

        # Create session
        session = ChatSession(
            session_id=session_id,
            task_id=request.task_id,
            status=ChatSessionStatus.ACTIVE,
            known=BriefState(),
            completeness=0.0,
            missing_fields=get_missing_fields({})
        )

        # Save to DB
        db = MongoDB.get_db()
        await db.chat_sessions.insert_one(session.model_dump())

        # Send initial greeting
        greeting = ChatMessage(
            session_id=session_id,
            role="assistant",
            text="Привіт! Я допоможу тобі створити бриф для перформанс-відео. Давай почнемо: що ти хочеш рекламувати?"
        )
        await db.chat_messages.insert_one(greeting.model_dump())

        logger.info(f"✅ Created chat session: {session_id}")

        return CreateSessionResponse(
            session_id=session_id,
            created_at=session.created_at.isoformat()
        )

    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.post("/message", summary="Send message and get response")
async def send_message(request: SendMessageRequest):
    """
    Send user message and get AI response.

    Returns either:
    - Ask mode: Next clarifying question
    - Final mode: Complete brief with generation prompt
    """
    try:
        db = MongoDB.get_db()

        # Get session
        session_data = await db.chat_sessions.find_one({"session_id": request.session_id})
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {request.session_id} not found"
            )

        session_data.pop("_id", None)
        session = ChatSession(**session_data)

        # Check if already finalized
        if session.status == ChatSessionStatus.FINAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session already finalized. Create a new session to start over."
            )

        # Save user message
        user_msg = ChatMessage(
            session_id=request.session_id,
            role="user",
            text=request.message
        )
        await db.chat_messages.insert_one(user_msg.model_dump())

        # Get conversation history
        history_cursor = db.chat_messages.find({"session_id": request.session_id}).sort("ts", 1)
        history_docs = await history_cursor.to_list(length=100)
        conversation_history = [
            {"role": msg["role"], "text": msg["text"]}
            for msg in history_docs
        ]

        # Get patterns from task if available
        patterns = None
        if session.task_id:
            task = await db.tasks.find_one({"task_id": session.task_id})
            if task:
                from src.services.patterns_extractor import extract_patterns_summary
                patterns = extract_patterns_summary(task)
                logger.info(f"✅ Loaded patterns from task {session.task_id}")

        # Call LLM planner
        logger.info(f"🤖 Planning next step for session {request.session_id}")
        try:
            plan_result = planner.plan_next_step(
                user_message=request.message,
                known_fields=session.known.model_dump(),
                conversation_history=conversation_history,
                patterns=patterns
            )
        except Exception as e:
            logger.error(f"LLM planner error: {e}")
            # Return friendly error
            error_msg = ChatMessage(
                session_id=request.session_id,
                role="assistant",
                text="Вибачте, виникла технічна помилка. Будь ласка, спробуйте ще раз або переформулюйте питання."
            )
            await db.chat_messages.insert_one(error_msg.model_dump())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM processing failed. Please try again."
            )

        # Process result
        if plan_result.get("need_more_info"):
            # ASK MODE: More info needed
            return await _handle_ask_mode(request.session_id, session, plan_result, db)
        else:
            # FINAL MODE: Brief complete
            return await _handle_final_mode(request.session_id, session, plan_result, db)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


async def _handle_ask_mode(
    session_id: str,
    session: ChatSession,
    plan_result: Dict[str, Any],
    db
) -> AskResponse:
    """Handle ask mode: save state and return question with options/suggestions."""

    question = plan_result.get("question", "Розкажи більше про твій продукт")
    updates = plan_result.get("updates", {})
    missing_fields = plan_result.get("missing_fields", [])

    # Extract new fields from LLM response
    options = plan_result.get("options", [])
    suggestions = plan_result.get("suggestions", [])
    examples = plan_result.get("examples", [])
    policy_hints = plan_result.get("policy_hints", [])

    # Update known fields
    known_dict = session.known.model_dump()
    known_dict.update(updates)

    # Calculate completeness
    completeness = calculate_completeness(known_dict)

    # Update session
    await db.chat_sessions.update_one(
        {"session_id": session_id},
        {"$set": {
            "known": known_dict,
            "completeness": completeness,
            "missing_fields": missing_fields,
            "updated_at": datetime.utcnow()
        }}
    )

    # Save assistant response
    assistant_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        text=question
    )
    await db.chat_messages.insert_one(assistant_msg.model_dump())

    logger.info(f"📝 Ask mode: completeness={completeness:.0%}, missing={len(missing_fields)}, options={len(options)}, suggestions={len(suggestions)}")

    # Build enhanced state
    state = {
        "known": known_dict,
        "completeness": completeness
    }

    # Add optional fields if present
    if options:
        state["options"] = options
    if suggestions:
        state["suggestions"] = suggestions
    if examples:
        state["examples"] = examples
    if policy_hints:
        state["policy_hints"] = policy_hints

    return AskResponse(
        type="ask",
        reply=question,
        missing_fields=missing_fields,
        state=state
    )


async def _handle_final_mode(
    session_id: str,
    session: ChatSession,
    plan_result: Dict[str, Any],
    db
) -> FinalResponse:
    """Handle final mode: save brief and return prompt with creative_spec."""

    brief = plan_result.get("brief", {})
    creative_spec = plan_result.get("creative_spec")
    final_prompt = plan_result.get("final_prompt")

    # Generate enhanced prompt if not provided or if we have creative_spec
    if not final_prompt or creative_spec:
        from src.services.chat_planner_helpers import generate_enhanced_final_prompt
        final_prompt = generate_enhanced_final_prompt(brief, creative_spec)

    # Update session to FINAL
    await db.chat_sessions.update_one(
        {"session_id": session_id},
        {"$set": {
            "status": ChatSessionStatus.FINAL,
            "known": brief,
            "completeness": 1.0,
            "missing_fields": [],
            "updated_at": datetime.utcnow()
        }}
    )

    # Save assistant response
    summary_text = "✅ Чудово! Я зібрав всю необхідну інформацію."
    if creative_spec:
        summary_text += " Створив детальний креативний blueprint з hook, структурою та стилем."

    assistant_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        text=summary_text
    )
    await db.chat_messages.insert_one(assistant_msg.model_dump())

    logger.info(f"✅ Final mode: brief complete for session {session_id}, creative_spec={bool(creative_spec)}")

    # Build response state
    state = {"completeness": 1.0}
    if creative_spec:
        state["creative_spec"] = creative_spec

    return FinalResponse(
        type="final",
        final_prompt=final_prompt,
        brief=brief,
        state=state
    )


@router.get("/session/{session_id}", response_model=SessionStateResponse, summary="Get session state")
async def get_session_state(session_id: str):
    """
    Get session state with message history.

    Useful for debugging or restoring state in frontend.
    """
    try:
        db = MongoDB.get_db()

        # Get session
        session_data = await db.chat_sessions.find_one({"session_id": session_id})
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )

        session_data.pop("_id", None)
        session = ChatSession(**session_data)

        # Get messages
        messages_cursor = db.chat_messages.find({"session_id": session_id}).sort("ts", 1)
        messages_docs = await messages_cursor.to_list(length=1000)

        messages = [
            MessageHistoryItem(
                role=msg["role"],
                text=msg["text"],
                ts=msg["ts"].isoformat()
            )
            for msg in messages_docs
        ]

        return SessionStateResponse(
            messages=messages,
            state={
                "known": session.known.model_dump(),
                "completeness": session.completeness,
                "missing_fields": session.missing_fields,
                "status": session.status
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session state: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session: {str(e)}"
        )


@router.get("/sessions", summary="List all chat sessions")
async def list_sessions(
    skip: int = 0,
    limit: int = 20
):
    """
    List all chat sessions with pagination.
    """
    try:
        db = MongoDB.get_db()

        # Get total count
        total = await db.chat_sessions.count_documents({})

        # Get sessions sorted by updated_at desc
        cursor = db.chat_sessions.find({}).sort("updated_at", -1).skip(skip).limit(limit)
        sessions = await cursor.to_list(length=limit)

        # Remove MongoDB _id
        for session in sessions:
            session.pop("_id", None)

        return {
            "success": True,
            "total": total,
            "skip": skip,
            "limit": limit,
            "sessions": sessions
        }

    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.post("/submit", response_model=SubmitResponse, summary="Submit final brief")
async def submit_brief(request: SubmitRequest):
    """
    Submit final brief for processing.

    For MVP, this is a stub that returns "queued".
    In production, this would forward to n8n webhook.
    """
    try:
        db = MongoDB.get_db()

        # Verify session exists and is finalized
        session_data = await db.chat_sessions.find_one({"session_id": request.session_id})
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {request.session_id} not found"
            )

        session = ChatSession(**{k: v for k, v in session_data.items() if k != "_id"})

        if session.status != ChatSessionStatus.FINAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot submit: session is not finalized. Continue the conversation first."
            )

        # TODO: Forward to n8n webhook
        # For now, just log and return queued
        logger.info(f"📤 Brief submitted for session {request.session_id}")
        logger.info(f"Brief: {request.brief}")
        logger.info(f"Prompt: {request.final_prompt[:200]}...")

        # Generate job_id for tracking
        job_id = str(uuid.uuid4())

        return SubmitResponse(
            submitted=True,
            handler="queued",
            job_id=job_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting brief: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit brief: {str(e)}"
        )
