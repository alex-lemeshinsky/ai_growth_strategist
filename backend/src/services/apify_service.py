import os
from typing import List, Dict, Any, Optional
from apify_client import ApifyClient
import logging

logger = logging.getLogger(__name__)


class ApifyService:
    """Service for interacting with Apify Facebook Ads Library scraper."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apify service.

        Args:
            api_key: Apify API key. If not provided, reads from APIFY_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get('APIFY_API_KEY')
        if not self.api_key:
            raise ValueError("APIFY_API_KEY must be provided or set as environment variable")

        self.client = ApifyClient(self.api_key)
        self.actor_name = os.environ.get('APIFY_ACTOR_NAME', 'curious_coder/facebook-ads-library-scraper')

    async def extract_ads_from_url(
        self,
        url: str,
        max_results: int = 15,
        fetch_all_details: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Extract ads from Facebook Ads Library URL using Apify.

        Args:
            url: Facebook Ads Library URL
            max_results: Maximum number of ads to extract
            fetch_all_details: Whether to fetch full creative details

        Returns:
            List of ad data dictionaries

        Raises:
            Exception: If the Apify actor run fails
        """
        run_input = {
            "urls": [{"url": url}],
            "maxResults": max_results,
            "fetchAllDetails": fetch_all_details,
        }

        logger.info(f"Starting Apify actor for URL: {url}")

        try:
            # Run the actor and wait for it to finish
            run = self.client.actor(self.actor_name).call(run_input=run_input)

            logger.info(f"Actor completed. Dataset ID: {run['defaultDatasetId']}")

            # Fetch the results from the dataset - simple approach like analyze.py
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)

            logger.info(f"Extracted {len(results)} ads")
            return results

        except Exception as e:
            logger.error(f"Error running Apify actor: {str(e)}")
            raise Exception(f"Failed to extract ads: {str(e)}")
