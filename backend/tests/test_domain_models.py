"""
Unit tests for domain models.
Tests business logic and model behavior without external dependencies.
"""

import pytest
from datetime import datetime

from src.domain.models import (
    FacebookAd, AdSearchQuery, AdSearchResult, AdSpendRange, 
    AdImpressionRange, AdActiveStatus, PublisherPlatform
)


class TestAdSpendRange:
    """Tests for AdSpendRange model"""
    
    def test_formatted_with_both_bounds(self):
        """Test formatted output when both bounds are present"""
        spend = AdSpendRange(lower_bound=100, upper_bound=500)
        assert spend.formatted == "100 - 500"
    
    def test_formatted_with_none_values(self):
        """Test formatted output when values are None"""
        spend = AdSpendRange(lower_bound=None, upper_bound=None)
        assert spend.formatted == "N/A"
    
    def test_formatted_with_partial_values(self):
        """Test formatted output with mixed None/int values"""
        spend = AdSpendRange(lower_bound=100, upper_bound=None)
        assert spend.formatted == "100 - 0"


class TestAdImpressionRange:
    """Tests for AdImpressionRange model"""
    
    def test_formatted_with_both_bounds(self):
        """Test formatted output with both bounds"""
        impressions = AdImpressionRange(lower_bound=1000, upper_bound=5000)
        assert impressions.formatted == "1,000 - 5,000"
    
    def test_formatted_with_none_values(self):
        """Test formatted output when values are None"""
        impressions = AdImpressionRange(lower_bound=None, upper_bound=None)
        assert impressions.formatted == "N/A"


class TestFacebookAd:
    """Tests for FacebookAd model"""
    
    def create_sample_ad(self) -> FacebookAd:
        """Create a sample ad for testing"""
        return FacebookAd(
            id="123456789",
            page_name="Test Page",
            page_id="987654321",
            ad_creative_bodies=["This is a test ad body", "Second body"],
            ad_creative_link_titles=["Test Title", "Second Title"],
            ad_creative_link_descriptions=["Test description", "Second description"],
            publisher_platforms=[PublisherPlatform.FACEBOOK, PublisherPlatform.INSTAGRAM],
            currency="USD",
            spend=AdSpendRange(100, 500),
            impressions=AdImpressionRange(1000, 5000)
        )
    
    def test_primary_properties(self):
        """Test primary text, title, description properties"""
        ad = self.create_sample_ad()
        
        assert ad.primary_text == "This is a test ad body"
        assert ad.primary_title == "Test Title"
        assert ad.primary_description == "Test description"
    
    def test_primary_properties_empty_lists(self):
        """Test primary properties when lists are empty"""
        ad = FacebookAd(id="123")
        
        assert ad.primary_text == ""
        assert ad.primary_title == ""
        assert ad.primary_description == ""
    
    def test_is_active_no_stop_time(self):
        """Test is_active when no stop time is set"""
        ad = FacebookAd(id="123", ad_delivery_stop_time=None)
        assert ad.is_active is True
    
    def test_is_active_with_future_stop_time(self):
        """Test is_active with future stop time"""
        future_time = datetime(2030, 1, 1)
        ad = FacebookAd(id="123", ad_delivery_stop_time=future_time)
        assert ad.is_active is True
    
    def test_is_active_with_past_stop_time(self):
        """Test is_active with past stop time"""
        past_time = datetime(2020, 1, 1)
        ad = FacebookAd(id="123", ad_delivery_stop_time=past_time)
        assert ad.is_active is False
    
    def test_formatted_platforms(self):
        """Test formatted platforms output"""
        ad = self.create_sample_ad()
        result = ad.formatted_platforms
        
        assert "📘 facebook" in result
        assert "📷 instagram" in result
    
    def test_formatted_platforms_empty(self):
        """Test formatted platforms when no platforms"""
        ad = FacebookAd(id="123")
        assert ad.formatted_platforms == "N/A"
    
    def test_platform_conversion_from_string(self):
        """Test automatic conversion from string to enum for platforms"""
        ad = FacebookAd(
            id="123",
            publisher_platforms=["facebook", "instagram"]  # strings
        )
        
        assert len(ad.publisher_platforms) == 2
        assert PublisherPlatform.FACEBOOK in ad.publisher_platforms
        assert PublisherPlatform.INSTAGRAM in ad.publisher_platforms


class TestAdSearchQuery:
    """Tests for AdSearchQuery model"""
    
    def test_default_values(self):
        """Test default values are set correctly"""
        query = AdSearchQuery(search_terms="fitness")
        
        assert query.search_terms == "fitness"
        assert query.ad_reached_countries == "US"
        assert query.limit == 20
        assert query.ad_active_status == AdActiveStatus.ALL
    
    def test_status_conversion_from_string(self):
        """Test automatic conversion from string to enum for status"""
        query = AdSearchQuery(
            search_terms="fitness",
            ad_active_status="ACTIVE"  # string
        )
        
        assert query.ad_active_status == AdActiveStatus.ACTIVE


class TestAdSearchResult:
    """Tests for AdSearchResult model"""
    
    def test_has_more_pages_true(self):
        """Test has_more_pages when next_page_url is present"""
        result = AdSearchResult(
            ads=[],
            total_count=0,
            next_page_url="https://example.com/next"
        )
        
        assert result.has_more_pages is True
    
    def test_has_more_pages_false(self):
        """Test has_more_pages when next_page_url is None"""
        result = AdSearchResult(
            ads=[],
            total_count=0,
            next_page_url=None
        )
        
        assert result.has_more_pages is False


class TestEnums:
    """Tests for enum classes"""
    
    def test_ad_active_status_values(self):
        """Test AdActiveStatus enum values"""
        assert AdActiveStatus.ALL.value == "ALL"
        assert AdActiveStatus.ACTIVE.value == "ACTIVE"
        assert AdActiveStatus.INACTIVE.value == "INACTIVE"
    
    def test_publisher_platform_values(self):
        """Test PublisherPlatform enum values"""
        assert PublisherPlatform.FACEBOOK.value == "facebook"
        assert PublisherPlatform.INSTAGRAM.value == "instagram"
        assert PublisherPlatform.MESSENGER.value == "messenger"
        assert PublisherPlatform.AUDIENCE_NETWORK.value == "audience_network"