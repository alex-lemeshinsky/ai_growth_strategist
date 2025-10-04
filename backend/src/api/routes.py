from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Query
from src.api.models import ParseAdsRequest, ParseAdsResponse, ErrorResponse
from src.db import MongoDB, Task, TaskStatus
from src.services.task_service import parse_ads_task, analyze_creatives_task
from src.utils.url_parser import URLParser
import logging
import uuid
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/parse-ads",
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def parse_ads(request: ParseAdsRequest, background_tasks: BackgroundTasks):
    """
    Parse Facebook Ads Library URL - returns task_id for tracking.
    Background task will extract ads and save to MongoDB.
    """
    try:
        # Validate URL
        if not URLParser.validate_url(request.url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Facebook Ads Library URL"
            )

        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Create task in MongoDB
        db = MongoDB.get_db()
        task = Task(
            task_id=task_id,
            url=request.url,
            status=TaskStatus.PENDING
        )
        await db.tasks.insert_one(task.model_dump())
        
        # Start background parsing (fire-and-forget)
        import asyncio
        asyncio.create_task(
            parse_ads_task(
                task_id=task_id,
                url=request.url,
                max_results=request.max_results
            )
        )
        
        logger.info(f"✅ Created task {task_id} for URL: {request.url}")
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Task created. Use GET /task/{task_id} to check status.",
            "status": TaskStatus.PENDING
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.post("/debug-parse")
async def debug_parse_ads(request: ParseAdsRequest):
    """
    Debug endpoint - returns raw Apify results without processing.
    """
    try:
        logger.info(f"Debug processing request for URL: {request.url}")

        # Initialize services
        apify_service = ApifyService()

        # Extract ads using Apify
        raw_ads = await apify_service.extract_ads_from_url(
            url=request.url,
            max_results=request.max_results,
            fetch_all_details=request.fetch_all_details
        )

        logger.info(f"Debug: Raw ads count: {len(raw_ads) if raw_ads else 0}")
        
        return {
            "success": True,
            "message": f"Raw extraction complete. Found {len(raw_ads) if raw_ads else 0} items",
            "raw_data": raw_ads,
            "data_types": [type(item).__name__ for item in raw_ads] if raw_ads else []
        }

    except Exception as e:
        logger.error(f"Debug error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/tasks")
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of tasks to return"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """
    List all tasks with pagination and optional status filter.
    """
    try:
        db = MongoDB.get_db()
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        
        # Get total count
        total = await db.tasks.count_documents(query)
        
        # Get tasks
        cursor = db.tasks.find(query).sort("created_at", -1).skip(skip).limit(limit)
        tasks = await cursor.to_list(length=limit)
        
        # Remove MongoDB _id field
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
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tasks: {str(e)}"
        )


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    """
    Get detailed information about a specific task.
    """
    try:
        db = MongoDB.get_db()
        
        task = await db.tasks.find_one({"task_id": task_id})
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        # Remove MongoDB _id field
        task.pop("_id", None)
        
        return {
            "success": True,
            "task": task
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task: {str(e)}"
        )


@router.post("/analyze-creatives/{task_id}")
async def analyze_creatives(task_id: str):
    """
    Start creative analysis for a parsed task.
    Only works if task status is PARSED and has ads to analyze.
    """
    try:
        db = MongoDB.get_db()
        
        # Get task
        task = await db.tasks.find_one({"task_id": task_id})
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        # Check if task is in PARSED status
        if task["status"] != TaskStatus.PARSED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Task must be in PARSED status. Current status: {task['status']}"
            )
        
        # Check if there are ads to analyze
        total_ads = task.get("total_ads", 0)
        if total_ads == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No ads found in this task to analyze"
            )
        
        # Check if analysis already exists
        if task.get("creatives_analyzed"):
            return {
                "success": False,
                "message": "Task already has analysis results. Analysis was already completed.",
                "task_id": task_id,
                "status": task["status"]
            }
        
        # Start analysis in background
        import asyncio
        asyncio.create_task(analyze_creatives_task(task_id))
        
        logger.info(f"✅ Started analysis for task {task_id} ({total_ads} ads)")
        
        return {
            "success": True,
            "message": f"Analysis started for {total_ads} ads. Check task status for progress.",
            "task_id": task_id,
            "total_ads": total_ads,
            "status": "analyzing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting analysis for task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start analysis: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Facebook Ads Parser API"
    }
