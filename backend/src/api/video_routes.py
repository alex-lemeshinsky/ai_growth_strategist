"""
Video streaming endpoints for cached videos.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse, Response
from pathlib import Path
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter()

# Cache directory
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache" / "videos"


@router.get("/stream/{video_hash}")
async def stream_video(video_hash: str, range: Optional[str] = None):
    """
    Stream video file from cache.
    Supports HTTP Range requests for seeking.
    
    Args:
        video_hash: Video file hash (filename without extension)
        range: HTTP Range header for partial content
    """
    try:
        # Find video file
        video_path = CACHE_DIR / f"{video_hash}.mp4"
        
        if not video_path.exists():
            # Try other extensions
            for ext in [".mov", ".avi", ".webm"]:
                alt_path = CACHE_DIR / f"{video_hash}{ext}"
                if alt_path.exists():
                    video_path = alt_path
                    break
        
        if not video_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video not found: {video_hash}"
            )
        
        file_size = video_path.stat().st_size
        
        # Parse Range header if present
        start = 0
        end = file_size - 1
        
        if range:
            # Parse "bytes=start-end"
            range_str = range.replace("bytes=", "")
            range_parts = range_str.split("-")
            
            if range_parts[0]:
                start = int(range_parts[0])
            if len(range_parts) > 1 and range_parts[1]:
                end = int(range_parts[1])
        
        # Read video chunk
        def iter_file():
            with open(video_path, "rb") as f:
                f.seek(start)
                remaining = end - start + 1
                chunk_size = 1024 * 1024  # 1MB chunks
                
                while remaining > 0:
                    chunk = f.read(min(chunk_size, remaining))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
        
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
        }
        
        # If range requested, return 206 Partial Content
        if range:
            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            headers["Content-Length"] = str(end - start + 1)
            
            return StreamingResponse(
                iter_file(),
                status_code=206,
                headers=headers,
                media_type="video/mp4"
            )
        
        # Full content
        headers["Content-Length"] = str(file_size)
        
        return StreamingResponse(
            iter_file(),
            headers=headers,
            media_type="video/mp4"
        )
        
    except Exception as e:
        logger.error(f"Error streaming video {video_hash}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stream video: {str(e)}"
        )


@router.get("/proxy")
async def proxy_video(url: str):
    """
    Proxy video from external URL.
    Useful for videos that require authentication or have CORS issues.
    
    Args:
        url: External video URL to proxy
    """
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            return Response(
                content=response.content,
                media_type="video/mp4",
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(len(response.content))
                }
            )
            
    except httpx.HTTPError as e:
        logger.error(f"Error proxying video from {url}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch video: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error proxying video: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to proxy video: {str(e)}"
        )


@router.head("/stream/{video_hash}")
async def video_head(video_hash: str):
    """
    HEAD request for video metadata.
    Used by video players to check file size before streaming.
    """
    try:
        video_path = CACHE_DIR / f"{video_hash}.mp4"
        
        if not video_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video not found: {video_hash}"
            )
        
        file_size = video_path.stat().st_size
        
        return Response(
            headers={
                "Accept-Ranges": "bytes",
                "Content-Type": "video/mp4",
                "Content-Length": str(file_size)
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting video metadata {video_hash}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get video metadata: {str(e)}"
        )
