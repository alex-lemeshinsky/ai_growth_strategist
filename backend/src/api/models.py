from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class AdCard(BaseModel):
    """Represents a single creative card in an ad."""
    body: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    link_url: Optional[str] = None
    link_description: Optional[str] = None
    cta_text: Optional[str] = None
    cta_type: Optional[str] = None
    original_image_url: Optional[str] = None
    resized_image_url: Optional[str] = None
    video_hd_url: Optional[str] = None
    video_sd_url: Optional[str] = None
    video_preview_image_url: Optional[str] = None


class AdCreative(BaseModel):
    """Structured ad creative data model."""
    ad_archive_id: str
    ad_id: Optional[str] = None
    page_id: str
    page_name: str
    page_profile_uri: Optional[str] = None
    page_profile_picture_url: Optional[str] = None
    page_categories: List[str] = Field(default_factory=list)
    page_like_count: Optional[int] = None

    # Creative content
    body: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    link_url: Optional[str] = None
    link_description: Optional[str] = None
    cta_text: Optional[str] = None
    cta_type: Optional[str] = None
    display_format: Optional[str] = None

    # Media
    cards: List[AdCard] = Field(default_factory=list)
    image_urls: List[str] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)

    # Dates and platforms
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_date_formatted: Optional[str] = None
    end_date_formatted: Optional[str] = None
    publisher_platform: List[str] = Field(default_factory=list)

    # Status
    is_active: bool = False
    categories: List[str] = Field(default_factory=list)

    # URLs
    ad_library_url: str
    url: Optional[str] = None

    # Additional metadata
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    total: Optional[int] = None
    ads_count: Optional[int] = None
    collation_count: Optional[int] = None


class ParseAdsRequest(BaseModel):
    """Request model for parsing ads."""
    url: str = Field(..., description="Facebook Ads Library URL")
    max_results: int = Field(default=5, ge=1, le=100, description="Maximum number of ads to extract")
    fetch_all_details: bool = Field(default=True, description="Whether to fetch full creative details")
    auto_analyze: bool = Field(default=True, description="Automatically start video analysis after parsing")
    output_filename: Optional[str] = Field(default=None, description="Custom output filename (without extension)")


class ParseAdsResponse(BaseModel):
    """Response model for parsing ads."""
    success: bool
    message: str
    ads_count: int
    output_file: Optional[str] = None
    ads: Optional[List[AdCreative]] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None
