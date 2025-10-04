"""
Domain models for Facebook Ads Library data.
These models represent business entities in a framework-agnostic way.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AdActiveStatus(Enum):
    """Facebook ad active status"""
    ALL = "ALL"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class PublisherPlatform(Enum):
    """Facebook publisher platforms"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    MESSENGER = "messenger"
    AUDIENCE_NETWORK = "audience_network"


@dataclass
class AdSpendRange:
    """Represents ad spend range"""
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None

    @property
    def formatted(self) -> str:
        """Format spend range for display"""
        if self.lower_bound is None and self.upper_bound is None:
            return "N/A"
        return f"{self.lower_bound or 0} - {self.upper_bound or 0}"


@dataclass
class AdImpressionRange:
    """Represents ad impression range"""
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None

    @property
    def formatted(self) -> str:
        """Format impression range for display"""
        if self.lower_bound is None and self.upper_bound is None:
            return "N/A"
        lower = f"{self.lower_bound:,}" if self.lower_bound else "0"
        upper = f"{self.upper_bound:,}" if self.upper_bound else "0"
        return f"{lower} - {upper}"


@dataclass
class FacebookAd:
    """Facebook ad from Ads Library business entity"""
    id: str
    page_name: Optional[str] = None
    page_id: Optional[str] = None
    ad_creation_time: Optional[datetime] = None
    ad_delivery_start_time: Optional[datetime] = None
    ad_delivery_stop_time: Optional[datetime] = None
    ad_snapshot_url: Optional[str] = None
    currency: Optional[str] = None
    
    # Creative content
    ad_creative_bodies: List[str] = field(default_factory=list)
    ad_creative_link_titles: List[str] = field(default_factory=list)
    ad_creative_link_descriptions: List[str] = field(default_factory=list)
    ad_creative_link_captions: List[str] = field(default_factory=list)
    
    # Platforms and metrics
    publisher_platforms: List[PublisherPlatform] = field(default_factory=list)
    impressions: Optional[AdImpressionRange] = None
    spend: Optional[AdSpendRange] = None

    def __post_init__(self):
        """Convert string platforms to enum if needed"""
        if self.publisher_platforms and isinstance(self.publisher_platforms[0], str):
            self.publisher_platforms = [
                PublisherPlatform(platform) for platform in self.publisher_platforms
            ]

    @property
    def is_active(self) -> bool:
        """Check if ad is currently active"""
        if self.ad_delivery_stop_time is None:
            return True
        return self.ad_delivery_stop_time > datetime.now()

    @property
    def primary_text(self) -> str:
        """Get primary ad text (first creative body)"""
        return self.ad_creative_bodies[0] if self.ad_creative_bodies else ""

    @property
    def primary_title(self) -> str:
        """Get primary ad title"""
        return self.ad_creative_link_titles[0] if self.ad_creative_link_titles else ""

    @property
    def primary_description(self) -> str:
        """Get primary ad description"""
        return self.ad_creative_link_descriptions[0] if self.ad_creative_link_descriptions else ""

    @property
    def platform_icons(self) -> Dict[PublisherPlatform, str]:
        """Get platform icons mapping"""
        return {
            PublisherPlatform.FACEBOOK: "📘",
            PublisherPlatform.INSTAGRAM: "📷",
            PublisherPlatform.MESSENGER: "💬",
            PublisherPlatform.AUDIENCE_NETWORK: "🌐"
        }

    @property
    def formatted_platforms(self) -> str:
        """Get formatted platform string with icons"""
        if not self.publisher_platforms:
            return "N/A"
        return " ".join([
            f"{self.platform_icons.get(platform, '▪️')} {platform.value}"
            for platform in self.publisher_platforms
        ])


@dataclass
class AdSearchQuery:
    """Search query for Facebook Ads Library"""
    search_terms: str
    ad_reached_countries: str = "US"
    limit: int = 20
    ad_active_status: AdActiveStatus = AdActiveStatus.ALL
    
    def __post_init__(self):
        """Convert string status to enum if needed"""
        if isinstance(self.ad_active_status, str):
            self.ad_active_status = AdActiveStatus(self.ad_active_status)


@dataclass
class AdSearchResult:
    """Result of ad search operation"""
    ads: List[FacebookAd]
    total_count: int
    next_page_url: Optional[str] = None
    
    @property
    def has_more_pages(self) -> bool:
        """Check if there are more pages available"""
        return self.next_page_url is not None