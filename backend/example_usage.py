#!/usr/bin/env python3
"""
Example usage of the Facebook Ads Library Parser API.

This demonstrates how to use the API programmatically.
"""

import requests
import json
from typing import Optional


class AdsParserClient:
    """Simple client for the Ads Parser API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def parse_ads(
        self,
        url: str,
        max_results: int = 15,
        fetch_all_details: bool = True,
        output_filename: Optional[str] = None
    ) -> dict:
        """
        Parse ads from Facebook Ads Library URL.

        Args:
            url: Facebook Ads Library URL
            max_results: Maximum number of ads to extract
            fetch_all_details: Whether to fetch full creative details
            output_filename: Custom output filename

        Returns:
            API response dictionary
        """
        endpoint = f"{self.base_url}/api/v1/parse-ads"

        payload = {
            "url": url,
            "max_results": max_results,
            "fetch_all_details": fetch_all_details
        }

        if output_filename:
            payload["output_filename"] = output_filename

        response = requests.post(endpoint, json=payload)
        response.raise_for_status()

        return response.json()

    def health_check(self) -> dict:
        """Check if the API is healthy."""
        response = requests.get(f"{self.base_url}/api/v1/health")
        return response.json()


def main():
    """Example usage."""
    # Initialize client
    client = AdsParserClient()

    # Check if API is running
    print("Checking API health...")
    health = client.health_check()
    print(f"✓ API Status: {health['status']}")
    print()

    # Example: Parse ads from a Facebook page
    example_url = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&view_all_page_id=106691191787847"

    print(f"Parsing ads from URL...")
    print(f"URL: {example_url}")
    print()

    try:
        result = client.parse_ads(
            url=example_url,
            max_results=5,  # Get only 5 ads for this example
            fetch_all_details=True
        )

        if result["success"]:
            print(f"✓ Success! Extracted {result['ads_count']} ads")
            print(f"✓ Output file: {result['output_file']}")
            print()

            # Display details of the first ad
            if result["ads"] and len(result["ads"]) > 0:
                print("First ad details:")
                print("-" * 60)

                ad = result["ads"][0]

                print(f"Page Name: {ad.get('page_name')}")
                print(f"Ad ID: {ad.get('ad_archive_id')}")
                print(f"Display Format: {ad.get('display_format')}")
                print(f"Platforms: {', '.join(ad.get('publisher_platform', []))}")
                print(f"Active: {ad.get('is_active')}")
                print()

                body = ad.get('body')
                if body:
                    print(f"Body Text:")
                    print(f"  {body[:200]}...")
                    print()

                images = ad.get('image_urls', [])
                videos = ad.get('video_urls', [])
                print(f"Media:")
                print(f"  Images: {len(images)}")
                print(f"  Videos: {len(videos)}")
                print()

                if ad.get('start_date'):
                    print(f"Start Date: {ad.get('start_date')}")
                if ad.get('end_date'):
                    print(f"End Date: {ad.get('end_date')}")

                print("-" * 60)

                # Show summary statistics
                print()
                print("Summary Statistics:")
                total_images = sum(len(ad.get('image_urls', [])) for ad in result["ads"])
                total_videos = sum(len(ad.get('video_urls', [])) for ad in result["ads"])
                active_count = sum(1 for ad in result["ads"] if ad.get('is_active'))

                print(f"  Total ads: {result['ads_count']}")
                print(f"  Active ads: {active_count}")
                print(f"  Total images: {total_images}")
                print(f"  Total videos: {total_videos}")

        else:
            print(f"✗ Failed: {result.get('message')}")

    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        if e.response.text:
            print(f"  Details: {e.response.text}")
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API")
        print("  Make sure the server is running: python -m src.main")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
