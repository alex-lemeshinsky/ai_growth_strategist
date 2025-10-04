"""
API routes for video policy compliance checking.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
import tempfile
import os
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.analysis.policy_checker import check_video_policy, format_policy_report

logger = logging.getLogger(__name__)

router = APIRouter()


class PolicyCheckRequest(BaseModel):
    """Request model for policy check via URL."""
    video_url: str = Field(..., description="URL to video file")
    platform: str = Field(default="facebook", description="Platform policy to check (facebook)")


class PolicyCheckResponse(BaseModel):
    """Response model for policy check."""
    success: bool
    platform: str
    result: dict
    text_report: Optional[str] = None


@router.post(
    "/check-video-url",
    response_model=PolicyCheckResponse,
    summary="Check video policy compliance via URL"
)
async def check_video_from_url(request: PolicyCheckRequest):
    """
    Check video compliance with platform advertising policy using video URL.
    
    The video will be downloaded temporarily and analyzed.
    """
    try:
        logger.info(f"Policy check requested for URL: {request.video_url}")
        
        # Check policy directly from URL (streaming - no local storage)
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                check_video_policy,
                None,  # video_path
                request.platform,
                None,  # model_name
                request.video_url  # video_url for direct streaming
            )
        
        # Generate text report
        text_report = format_policy_report(result)
        
        logger.info(f"Policy check complete. Pass: {result.get('compliance_summary', {}).get('will_pass_moderation', False)}")
        
        return PolicyCheckResponse(
            success=True,
            platform=request.platform,
            result=result,
            text_report=text_report
        )
    
    except httpx.HTTPError as e:
        logger.error(f"Error downloading video: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download video: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error checking video policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check video policy: {str(e)}"
        )


@router.post(
    "/check-video-upload",
    response_model=PolicyCheckResponse,
    summary="Check video policy compliance via file upload"
)
async def check_video_from_upload(
    video: UploadFile = File(..., description="Video file to check"),
    platform: str = Form(default="facebook", description="Platform policy (facebook)")
):
    """
    Check video compliance with platform advertising policy using uploaded file.
    
    Upload a video file and get compliance check results.
    """
    try:
        logger.info(f"Policy check requested for uploaded file: {video.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(suffix=Path(video.filename or "video.mp4").suffix, delete=False) as tmp_file:
            temp_path = tmp_file.name
            
            try:
                # Write uploaded content
                content = await video.read()
                tmp_file.write(content)
                tmp_file.flush()
                
                logger.info(f"File saved to: {temp_path}")
                
                # Check policy in thread pool
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(
                        executor,
                        check_video_policy,
                        temp_path,
                        platform
                    )
                
                # Generate text report
                text_report = format_policy_report(result)
                
                logger.info(f"Policy check complete. Pass: {result.get('compliance_summary', {}).get('will_pass_moderation', False)}")
                
                return PolicyCheckResponse(
                    success=True,
                    platform=platform,
                    result=result,
                    text_report=text_report
                )
                
            finally:
                # Cleanup temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
    
    except Exception as e:
        logger.error(f"Error checking video policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check video policy: {str(e)}"
        )


@router.get(
    "/supported-platforms",
    summary="Get list of supported platforms"
)
async def get_supported_platforms():
    """
    Get list of supported advertising platforms for policy checking.
    """
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
