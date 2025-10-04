from fastapi import APIRouter, HTTPException, status
from src.api.models import ParseAdsRequest, ParseAdsResponse, ErrorResponse
from src.services.apify_service import ApifyService
from src.services.data_processor import DataProcessor
from src.utils.url_parser import URLParser
from src.utils.file_manager import FileManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/parse-ads",
    response_model=ParseAdsResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def parse_ads(request: ParseAdsRequest):
    """
    Parse Facebook Ads Library URL and extract ad creatives.

    Args:
        request: ParseAdsRequest containing URL and options

    Returns:
        ParseAdsResponse with extracted ads data and file location
    """
    try:
        # Validate URL
        if not URLParser.validate_url(request.url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Facebook Ads Library URL"
            )

        logger.info(f"Processing request for URL: {request.url}")

        # Initialize services
        apify_service = ApifyService()
        file_manager = FileManager()

        # Extract ads using Apify
        raw_ads = await apify_service.extract_ads_from_url(
            url=request.url,
            max_results=request.max_results,
            fetch_all_details=request.fetch_all_details
        )

        if not raw_ads:
            return ParseAdsResponse(
                success=True,
                message="No ads found for the given URL",
                ads_count=0,
                ads=[]
            )

        logger.info(f"Successfully extracted {len(raw_ads)} ads")
        
        # For now, let's save raw data to JSON file in creatives directory
        import json
        import os
        from datetime import datetime
        
        # Create creatives directory if it doesn't exist
        os.makedirs("creatives", exist_ok=True)
        
        # Get page info from first ad
        page_name = "unknown"
        page_id = "unknown"
        if raw_ads and isinstance(raw_ads[0], dict):
            page_name = raw_ads[0].get('page_name', 'unknown')
            page_id = raw_ads[0].get('page_id', 'unknown')
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{page_name}_{page_id}_{timestamp}.json"
        filepath = f"creatives/{filename}"
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "extraction_metadata": {
                    "url": request.url,
                    "extracted_at": datetime.now().isoformat(),
                    "total_ads": len(raw_ads),
                    "page_name": page_name,
                    "page_id": page_id
                },
                "ads": raw_ads
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(raw_ads)} ads to {filepath}")
        
        return {
            "success": True,
            "message": f"Successfully extracted {len(raw_ads)} ads",
            "ads_count": len(raw_ads),
            "output_file": filepath,
            "page_name": page_name,
            "page_id": page_id,
            "ads_sample": raw_ads[:2] if raw_ads else []  # Return first 2 ads as sample
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing ads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process ads: {str(e)}"
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


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Facebook Ads Parser API"
    }
