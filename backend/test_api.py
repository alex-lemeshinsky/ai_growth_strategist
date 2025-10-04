#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI implementation.
Run this after starting the server with: python -m src.main
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_parse_ads():
    """Test the parse ads endpoint."""
    print("Testing parse ads endpoint...")

    # Example URL from the development plan
    test_url = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=106691191787847"

    payload = {
        "url": test_url,
        "max_results": 5,  # Small number for testing
        "fetch_all_details": True
    }

    print(f"Request payload: {json.dumps(payload, indent=2)}")
    print("\nSending request...")

    response = requests.post(
        f"{API_URL}/api/v1/parse-ads",
        json=payload
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nSuccess! Extracted {result['ads_count']} ads")
        print(f"Output file: {result['output_file']}")

        # Print first ad details
        if result['ads'] and len(result['ads']) > 0:
            first_ad = result['ads'][0]
            print(f"\nFirst ad details:")
            print(f"  Page: {first_ad.get('page_name')}")
            print(f"  Body: {first_ad.get('body', 'N/A')[:100]}...")
            print(f"  Images: {len(first_ad.get('image_urls', []))} images")
            print(f"  Videos: {len(first_ad.get('video_urls', []))} videos")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Facebook Ads Library Parser API - Test Script\n")
    print("=" * 60)
    print()

    try:
        test_health_check()
        # Uncomment to test actual ad parsing (requires APIFY_API_KEY)
        # test_parse_ads()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running:")
        print("  python -m src.main")
    except Exception as e:
        print(f"Error: {e}")
