#!/usr/bin/env python3
"""
Direct test of Apify integration - matches analyze.py approach
"""

import os
import sys
from apify_client import ApifyClient
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path so we can import our services
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_apify_direct():
    """Test Apify directly like analyze.py does"""
    
    started = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=106691191787847"
    
    APIFY_API_KEY = os.environ.get('APIFY_API_KEY')
    ACTOR_NAME = "curious_coder/facebook-ads-library-scraper"
    RESULTS_LIMIT = 15

    if not APIFY_API_KEY:
        print("❌ APIFY_API_KEY not found in environment")
        return

    client = ApifyClient(APIFY_API_KEY)

    run_input = {
        "urls": [
            {"url": started}
        ],
        "maxResults": RESULTS_LIMIT,
        "fetchAllDetails": True,
    }

    print(f"🚀 Starting Apify test...")
    print(f"URL: {started}")
    print(f"Actor: {ACTOR_NAME}")

    try:
        run = client.actor(ACTOR_NAME).call(run_input=run_input)
        print("✅ Actor finished. Getting data...")
        print(f"Dataset ID: {run['defaultDatasetId']}")
        print(f"Run details: {run}")

        # Try to get dataset info
        try:
            dataset = client.dataset(run["defaultDatasetId"])
            dataset_info = dataset.get()
            print(f"📊 Dataset info: {dataset_info}")
        except Exception as e:
            print(f"⚠️  Could not get dataset info: {e}")

        # Get items
        results = []
        item_count = 0
        
        print("🔍 Iterating through items...")
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            item_count += 1
            print(f"📝 Item {item_count}: {type(item)}")
            
            if isinstance(item, dict):
                print(f"   Keys: {list(item.keys()) if item else 'empty dict'}")
                if 'page_name' in item:
                    print(f"   Page: {item.get('page_name')}")
                if 'ad_archive_id' in item:
                    print(f"   Ad ID: {item.get('ad_archive_id')}")
            else:
                print(f"   Value (first 200 chars): {str(item)[:200]}")
            
            results.append(item)
            
            # Limit for testing
            if item_count >= 3:
                print(f"   ... limiting to first 3 items for testing")
                break

        print(f"✅ Total items found: {len(results)}")
        
        if results:
            print("📄 Saving first result to test_result.json")
            with open('test_result.json', 'w', encoding='utf-8') as f:
                json.dump(results[0], f, indent=2, ensure_ascii=False)
                
            print("🎯 First result summary:")
            first_result = results[0]
            if isinstance(first_result, dict):
                print(f"   Type: {type(first_result)}")
                print(f"   Keys: {list(first_result.keys())}")
                if 'page_name' in first_result:
                    print(f"   Page Name: {first_result.get('page_name')}")
                if 'ad_archive_id' in first_result:
                    print(f"   Ad Archive ID: {first_result.get('ad_archive_id')}")
        else:
            print("❌ No results found")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_apify_direct()