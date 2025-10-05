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
                max_results=request.max_results,
                auto_analyze=request.auto_analyze
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
    Debug endpoint - returns raw Apify results with filtering statistics.
    """
    try:
        logger.info(f"Debug processing request for URL: {request.url}")

        # Initialize services  
        from src.services.apify_service import ApifyService
        apify_service = ApifyService()

        # Extract ads using Apify
        raw_ads = await apify_service.extract_ads_from_url(
            url=request.url,
            max_results=request.max_results,
            fetch_all_details=request.fetch_all_details
        )

        # Analyze media types
        media_stats = {
            "total": len(raw_ads),
            "video_ads": 0,
            "image_ads": 0,
            "carousel_ads": 0,
            "other_ads": 0
        }
        
        sample_ads = []
        
        for ad in raw_ads[:5]:  # Show first 5 for debugging
            snapshot = ad.get('snapshot', {})
            
            # Check media type
            has_video = False
            has_images = False
            
            # Check for videos
            if snapshot.get('videos') and len(snapshot.get('videos', [])) > 0:
                has_video = True
            
            # Check cards for video/images
            cards = snapshot.get('cards', [])
            for card in cards:
                if card.get('video_hd_url') or card.get('video_sd_url'):
                    has_video = True
                if card.get('original_image_url') or card.get('resized_image_url'):
                    has_images = True
            
            # Categorize
            if has_video:
                media_stats["video_ads"] += 1
                media_type = "video"
            elif len(cards) > 1:
                media_stats["carousel_ads"] += 1
                media_type = "carousel"
            elif has_images:
                media_stats["image_ads"] += 1
                media_type = "image"
            else:
                media_stats["other_ads"] += 1
                media_type = "other"
            
            sample_ads.append({
                "ad_archive_id": ad.get('ad_archive_id'),
                "media_type": media_type,
                "has_video": has_video,
                "cards_count": len(cards),
                "videos_count": len(snapshot.get('videos', []))
            })

        logger.info(f"Debug: Media stats: {media_stats}")
        
        return {
            "success": True,
            "message": f"Extraction complete. Found {len(raw_ads)} items",
            "media_stats": media_stats,
            "sample_ads": sample_ads,
            "requested_max": request.max_results
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
