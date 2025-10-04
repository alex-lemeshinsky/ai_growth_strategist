#!/usr/bin/env python3
"""
Test script for full video analysis pipeline:
1. Parse ads from FB Ads Library
2. Analyze video creatives
3. Get aggregated results
"""
import httpx
import time
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"

def create_parse_task(url: str, max_results: int = 5) -> Optional[str]:
    """Create parsing task."""
    print(f"\n📤 Creating parse task for: {url}")
    
    response = httpx.post(
        f"{BASE_URL}/parse-ads",
        json={"url": url, "max_results": max_results},
        timeout=30.0
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return None
    
    data = response.json()
    task_id = data.get("task_id")
    print(f"✅ Task created: {task_id}")
    return task_id


def get_task_status(task_id: str) -> dict:
    """Get task status."""
    response = httpx.get(f"{BASE_URL}/task/{task_id}", timeout=30.0)
    if response.status_code != 200:
        print(f"❌ Error getting task: {response.text}")
        return {}
    return response.json().get("task", {})


def wait_for_parsing(task_id: str, timeout: int = 300) -> bool:
    """Wait for parsing to complete."""
    print(f"\n⏳ Waiting for parsing to complete...")
    
    start = time.time()
    while time.time() - start < timeout:
        task = get_task_status(task_id)
        status = task.get("status")
        
        print(f"   Status: {status}")
        
        if status == "parsed":
            print(f"✅ Parsing complete! Found {task.get('total_ads', 0)} ads")
            return True
        elif status == "failed":
            print(f"❌ Parsing failed: {task.get('error')}")
            return False
        
        time.sleep(5)
    
    print(f"❌ Timeout waiting for parsing")
    return False


def start_analysis(task_id: str) -> bool:
    """Start creative analysis."""
    print(f"\n📊 Starting analysis for task: {task_id}")
    
    response = httpx.post(f"{BASE_URL}/analyze-creatives/{task_id}", timeout=30.0)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return False
    
    data = response.json()
    print(f"✅ Analysis started: {data.get('message')}")
    return True


def wait_for_analysis(task_id: str, timeout: int = 600) -> bool:
    """Wait for analysis to complete."""
    print(f"\n⏳ Waiting for analysis to complete...")
    
    start = time.time()
    while time.time() - start < timeout:
        task = get_task_status(task_id)
        status = task.get("status")
        
        print(f"   Status: {status}")
        
        if status == "completed":
            print(f"✅ Analysis complete!")
            return True
        elif status == "failed":
            print(f"❌ Analysis failed: {task.get('error')}")
            return False
        
        time.sleep(10)
    
    print(f"❌ Timeout waiting for analysis")
    return False


def print_results(task_id: str):
    """Print analysis results."""
    task = get_task_status(task_id)
    
    print("\n" + "="*80)
    print("📊 ANALYSIS RESULTS")
    print("="*80)
    
    # Individual creatives
    creatives = task.get("creatives_analyzed", [])
    print(f"\n🎬 Analyzed {len(creatives)} creatives:")
    for i, creative in enumerate(creatives, 1):
        print(f"\n  {i}. {creative.get('page_name')} - {creative.get('ad_archive_id')}")
        print(f"     Summary: {creative.get('summary', 'N/A')[:100]}...")
        if creative.get('scores'):
            scores = creative['scores']
            print(f"     Scores: Hook={scores.get('hook_strength', 0):.2f}, "
                  f"CTA={scores.get('cta_clarity', 0):.2f}, "
                  f"Quality={scores.get('execution_quality', 0):.2f}")
    
    # Check for aggregation errors
    aggregation_error = task.get("aggregation_error")
    if aggregation_error:
        print(f"\n⚠️  Warning: Aggregation partially failed: {aggregation_error[:200]}")
    
    # Aggregated analysis
    aggregated = task.get("aggregated_analysis")
    if aggregated:
        print("\n" + "-"*80)
        print("📈 AGGREGATED INSIGHTS")
        print("-"*80)
        
        print(f"\n🎯 Core Idea: {aggregated.get('core_idea', 'N/A')}")
        print(f"🏷️  Theme: {aggregated.get('theme', 'N/A')}")
        print(f"💬 Message: {aggregated.get('message', 'N/A')}")
        
        if aggregated.get('pain_points'):
            print(f"\n😢 Pain Points:")
            for pain in aggregated['pain_points']:
                print(f"   - {pain}")
        
        if aggregated.get('hooks'):
            print(f"\n🎣 Popular Hooks:")
            for hook in aggregated['hooks']:
                print(f"   - {hook}")
        
        if aggregated.get('recommendations'):
            print(f"\n💡 Recommendations:")
            print(f"   {aggregated['recommendations']}")
        
        if aggregated.get('video_prompt'):
            print(f"\n🎥 Video Prompt (first 200 chars):")
            print(f"   {aggregated['video_prompt'][:200]}...")
    elif not aggregation_error:
        print("\n⚠️  No aggregated analysis available")
    
    print("\n" + "="*80)


def main():
    """Run full pipeline test."""
    # Example FB Ads Library URL
    url = input("\n🔗 Enter Facebook Ads Library URL: ").strip()
    if not url:
        print("❌ No URL provided")
        return
    
    max_results = int(input("📊 How many ads to analyze? (default: 5): ").strip() or "5")
    
    # Step 1: Parse ads
    task_id = create_parse_task(url, max_results)
    if not task_id:
        return
    
    # Step 2: Wait for parsing
    if not wait_for_parsing(task_id):
        return
    
    # Step 3: Start analysis
    if not start_analysis(task_id):
        return
    
    # Step 4: Wait for analysis
    if not wait_for_analysis(task_id):
        return
    
    # Step 5: Print results
    print_results(task_id)
    
    print(f"\n✅ Full pipeline completed!")
    print(f"📋 Task ID: {task_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
