"""
API routes for video policy compliance checking with task tracking.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import tempfile
import os
import uuid
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from src.db import MongoDB, PolicyTask, PolicyCheckStatus

logger = logging.getLogger(__name__)

router = APIRouter()


class CreatePolicyCheckRequest(BaseModel):
    """Request to create policy check task."""
    video_url: Optional[str] = Field(None, description="URL to video file")
    platform: str = Field(default="facebook", description="Platform policy to check")


@router.post("/check", summary="Create policy check task")
async def create_policy_check(request: CreatePolicyCheckRequest):
    """
    Create a new policy check task.
    Returns task_id for tracking progress.
    """
    try:
        if not request.video_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="video_url is required"
            )
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Create task in MongoDB
        db = MongoDB.get_db()
        task = PolicyTask(
            task_id=task_id,
            video_url=request.video_url,
            platform=request.platform,
            status=PolicyCheckStatus.PENDING
        )
        await db.policy_tasks.insert_one(task.model_dump())
        
        # Start background check
        asyncio.create_task(
            policy_check_task(
                task_id=task_id,
                video_url=request.video_url,
                platform=request.platform
            )
        )
        
        logger.info(f"✅ Created policy check task {task_id}")
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Policy check started. Use GET /policy/task/{task_id} to check status.",
            "status": PolicyCheckStatus.PENDING
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating policy check task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create policy check task: {str(e)}"
        )


@router.get("/task/{task_id}", summary="Get policy check task status")
async def get_policy_task(task_id: str):
    """
    Get policy check task details and results.
    """
    try:
        db = MongoDB.get_db()
        
        task = await db.policy_tasks.find_one({"task_id": task_id})
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Policy task {task_id} not found"
            )
        
        # Remove MongoDB _id
        task.pop("_id", None)
        
        return {
            "success": True,
            "task": task
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting policy task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get policy task: {str(e)}"
        )


@router.get("/tasks", summary="List all policy check tasks")
async def list_policy_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    platform: Optional[str] = Query(None)
):
    """
    List all policy check tasks with pagination.
    """
    try:
        db = MongoDB.get_db()
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        if platform:
            query["platform"] = platform
        
        # Get total count
        total = await db.policy_tasks.count_documents(query)
        
        # Get tasks
        cursor = db.policy_tasks.find(query).sort("created_at", -1).skip(skip).limit(limit)
        tasks = await cursor.to_list(length=limit)
        
        # Remove MongoDB _id
        for task in tasks:
            task.pop("_id", None)
        
        return {
            "success": True,
            "total": total,
            "skip": skip,
            "limit": limit,
            "tasks": tasks
        }
        
    except Exception as e:
        logger.error(f"Error listing policy tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list policy tasks: {str(e)}"
        )


@router.get("/supported-platforms")
async def get_supported_platforms():
    """Get list of supported platforms."""
    return {
        "success": True,
        "platforms": [
            {
                "id": "facebook",
                "name": "Facebook/Meta Ads",
                "description": "Check compliance with Facebook and Instagram advertising policies"
            }
        ]
    }


async def policy_check_task(task_id: str, video_url: str, platform: str):
    """
    Background task for policy checking.
    """
    from src.analysis.policy_checker import check_video_policy, format_policy_report
    from src.utils.policy_html_report import generate_comprehensive_policy_html
    
    db = MongoDB.get_db()
    
    try:
        # Update status to CHECKING
        await db.policy_tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": PolicyCheckStatus.CHECKING,
                "updated_at": datetime.utcnow()
            }}
        )
        
        logger.info(f"🔍 Starting policy check for task {task_id}")
        
        # Run policy check in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                check_video_policy,
                None,  # video_path
                platform,
                None,  # model_name
                video_url  # video_url
            )
        
        # Generate comprehensive HTML report with all new fields
        html_report = generate_comprehensive_policy_html(result, video_url, platform)
        
        # Extract key metrics
        compliance = result.get("compliance_summary", {})
        violations = result.get("facebook_policy_violations", [])
        
        # Update task with results
        await db.policy_tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": PolicyCheckStatus.COMPLETED,
                "policy_result": result,
                "html_report": html_report,
                "will_pass_moderation": compliance.get("will_pass_moderation", False),
                "risk_level": compliance.get("risk_level", "unknown"),
                "violations_count": len(violations),
                "updated_at": datetime.utcnow()
            }}
        )
        
        logger.info(f"✅ Policy check completed for task {task_id}")
        
    except Exception as e:
        logger.error(f"❌ Policy check failed for task {task_id}: {e}")
        await db.policy_tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "status": PolicyCheckStatus.FAILED,
                "error": str(e),
                "updated_at": datetime.utcnow()
            }}
        )

