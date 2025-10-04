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
        
        # Generate HTML report
        html_report = generate_policy_html_report(result, video_url, platform)
        
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


def generate_policy_html_report(result: dict, video_url: str, platform: str) -> str:
    """
    Generate HTML report for policy check results.
    """
    compliance = result.get("compliance_summary", {})
    will_pass = compliance.get("will_pass_moderation", False)
    risk_level = compliance.get("risk_level", "unknown")
    confidence = compliance.get("confidence", 0)
    
    status_emoji = "✅" if will_pass else "❌"
    status_text = "PASS" if will_pass else "FAIL"
    status_color = "#10b981" if will_pass else "#ef4444"
    
    risk_colors = {
        "low": "#10b981",
        "medium": "#f59e0b",
        "high": "#ef4444"
    }
    risk_color = risk_colors.get(risk_level, "#6b7280")
    
    html = f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Policy Check Report - {platform.upper()}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        
        .status-banner {{
            background: {status_color};
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 15px 25px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid {risk_color};
        }}
        
        .metric-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }}
        
        .section {{
            margin: 30px 0;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .violation {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }}
        
        .violation-header {{
            font-weight: bold;
            color: #dc2626;
            margin-bottom: 5px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-critical {{ background: #fee2e2; color: #dc2626; }}
        .badge-high {{ background: #fed7aa; color: #ea580c; }}
        .badge-medium {{ background: #fef3c7; color: #d97706; }}
        .badge-low {{ background: #dbeafe; color: #2563eb; }}
        
        .video-container {{
            margin: 20px 0;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        video {{
            width: 100%;
            max-height: 500px;
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Policy Compliance Check</h1>
            <p><strong>Platform:</strong> {platform.upper()}</p>
            <p><strong>Checked:</strong> {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        </div>
        
        <div class="status-banner">
            {status_emoji} MODERATION STATUS: {status_text}
        </div>
        
        <div class="content">
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Risk Level</div>
                    <div class="metric-value" style="color: {risk_color}">{risk_level.upper()}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{confidence:.0%}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Violations</div>
                    <div class="metric-value">{len(result.get('facebook_policy_violations', []))}</div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">🎥 Video</h2>
                <div class="video-container">
                    <video controls preload="metadata">
                        <source src="{video_url}" type="video/mp4">
                        Your browser does not support video.
                    </video>
                </div>
            </div>
"""
    
    # Violations
    violations = result.get("facebook_policy_violations", [])
    if violations:
        html += """
            <div class="section">
                <h2 class="section-title">⛔ Policy Violations</h2>
"""
        for v in violations:
            severity = v.get("severity", "unknown")
            badge_class = f"badge-{severity}"
            
            html += f"""
                <div class="violation">
                    <div class="violation-header">
                        <span class="badge {badge_class}">{severity}</span>
                        {v.get('category', 'Unknown')}
                    </div>
                    <p><strong>Issue:</strong> {v.get('description', 'No description')}</p>
                    {f'<p><strong>Timestamp:</strong> {v["timestamp_seconds"]}s</p>' if v.get('timestamp_seconds') else ''}
                    {f'<p><strong>💡 Recommendation:</strong> {v["recommendation"]}</p>' if v.get('recommendation') else ''}
                </div>
"""
        html += "            </div>\n"
    
    # Feedback
    feedback = result.get("feedback", {})
    if feedback.get("main_issues") or feedback.get("recommendations"):
        html += """
            <div class="section">
                <h2 class="section-title">💡 Feedback & Recommendations</h2>
"""
        
        if feedback.get("main_issues"):
            html += "                <h3>Main Issues:</h3>\n                <ul>\n"
            for issue in feedback["main_issues"]:
                html += f"                    <li>{issue}</li>\n"
            html += "                </ul>\n"
        
        if feedback.get("recommendations"):
            html += "                <h3>Recommendations:</h3>\n                <ul>\n"
            for rec in feedback["recommendations"]:
                html += f"                    <li>{rec}</li>\n"
            html += "                </ul>\n"
        
        html += "            </div>\n"
    
    # Overall assessment
    html += f"""
            <div class="section">
                <h2 class="section-title">📝 Overall Assessment</h2>
                <p>{compliance.get('overall_assessment', 'No assessment available')}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html
