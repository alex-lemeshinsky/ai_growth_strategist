from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class URLParser:
    """Parse and validate Facebook Ads Library URLs."""

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if the URL is a valid Facebook Ads Library URL.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc in ['www.facebook.com', 'facebook.com'] and
                '/ads/library' in parsed.path
            )
        except Exception as e:
            logger.error(f"URL validation error: {str(e)}")
            return False

    @staticmethod
    def extract_parameters(url: str) -> Dict[str, Any]:
        """
        Extract parameters from Facebook Ads Library URL.

        Args:
            url: Facebook Ads Library URL

        Returns:
            Dictionary of extracted parameters
        """
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)

            # Convert single-item lists to single values
            extracted = {}
            for key, value in params.items():
                extracted[key] = value[0] if len(value) == 1 else value

            return {
                'active_status': extracted.get('active_status'),
                'ad_type': extracted.get('ad_type'),
                'country': extracted.get('country'),
                'is_targeted_country': extracted.get('is_targeted_country'),
                'media_type': extracted.get('media_type'),
                'search_type': extracted.get('search_type'),
                'view_all_page_id': extracted.get('view_all_page_id'),
                'q': extracted.get('q'),  # search query
                'page_ids': extracted.get('page_ids'),
            }
        except Exception as e:
            logger.error(f"Parameter extraction error: {str(e)}")
            return {}

    @staticmethod
    def get_page_id_from_url(url: str) -> Optional[str]:
        """
        Extract page ID from URL if present.

        Args:
            url: Facebook Ads Library URL

        Returns:
            Page ID or None
        """
        params = URLParser.extract_parameters(url)
        return params.get('view_all_page_id') or params.get('page_ids')
