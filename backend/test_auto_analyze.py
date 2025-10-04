#!/usr/bin/env python3
"""
Test auto-analyze flow: одне API request → парсинг → аналіз → HTML звіт.
"""
import httpx
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_auto_analyze():
    """Test complete auto-analyze flow."""
    
    # Get URL from user
    url = input("\n🔗 Enter Facebook Ads Library URL: ").strip()
    if not url:
        print("❌ No URL provided")
        return
    
    max_results = int(input("📊 How many ads to analyze? (default: 5): ").strip() or "5")
    
    # Create task with auto_analyze=True
    print(f"\n📤 Creating task with auto-analyze enabled...")
    
    response = httpx.post(
        f"{BASE_URL}/parse-ads",
        json={
            "url": url,
            "max_results": max_results,
            "auto_analyze": True  # This will auto-trigger analysis!
        },
        timeout=30.0
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return
    
    data = response.json()
    task_id = data.get("task_id")
    print(f"✅ Task created: {task_id}")
    print("⏳ Waiting for auto-analysis to complete...\n")
    
    # Wait for completion
    start = time.time()
    while time.time() - start < 900:  # 15 min timeout
        time.sleep(10)
        
        # Check status
        status_response = httpx.get(f"{BASE_URL}/task/{task_id}", timeout=30.0)
        if status_response.status_code != 200:
            print(f"❌ Error getting task: {status_response.text}")
            return
        
        task = status_response.json().get("task", {})
        status = task.get("status")
        
        print(f"   Status: {status}")
        
        if status == "completed":
            print(f"\n✅ Analysis complete!")
            print_results(task)
            return
        elif status == "failed":
            print(f"\n❌ Task failed: {task.get('error')}")
            return
    
    print("\n❌ Timeout waiting for analysis")


def print_results(task: dict):
    """Print analysis results."""
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    
    # Stats
    total_ads = task.get("total_ads", 0)
    analyzed = len(task.get("creatives_analyzed", []))
    print(f"\n📈 Processed: {analyzed}/{total_ads} creatives")
    
    # Aggregated insights
    aggregated = task.get("aggregated_analysis")
    if aggregated:
        print(f"\n🎯 Core Idea: {aggregated.get('core_idea', 'N/A')}")
        print(f"🏷️  Theme: {aggregated.get('theme', 'N/A')}")
        
        if aggregated.get("video_prompt"):
            print(f"\n🎥 Video Prompt (first 200 chars):")
            print(f"   {aggregated['video_prompt'][:200]}...")
    
    # HTML report
    html_report = task.get("html_report")
    if html_report:
        print(f"\n📄 HTML Report: {len(html_report)} characters")
        
        # Save to file
        filename = f"report_{task.get('task_id', 'unknown')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        print(f"✅ Saved HTML report to: {filename}")
        print(f"🌐 Open in browser: file://{filename}")
    else:
        print("\n⚠️  No HTML report generated")
    
    # Warnings
    if task.get("aggregation_error"):
        print(f"\n⚠️  Aggregation warning: {task['aggregation_error'][:100]}...")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        test_auto_analyze()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
