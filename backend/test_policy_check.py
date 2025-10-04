#!/usr/bin/env python3
"""
Test video policy checking.
"""
import httpx
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/policy"


def test_policy_check_url():
    """Test policy check with video URL."""
    
    video_url = input("\n🔗 Enter video URL to check: ").strip()
    if not video_url:
        print("❌ No URL provided")
        return
    
    print(f"\n📤 Sending policy check request...")
    print(f"   Platform: Facebook")
    print(f"   URL: {video_url}\n")
    
    try:
        response = httpx.post(
            f"{BASE_URL}/check-video-url",
            json={
                "video_url": video_url,
                "platform": "facebook"
            },
            timeout=120.0
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return
        
        data = response.json()
        
        # Print text report
        if data.get("text_report"):
            print(data["text_report"])
        
        # Save full JSON result
        result_file = "policy_check_result.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(data["result"], f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full results saved to: {result_file}")
        
        # Quick summary
        compliance = data["result"].get("compliance_summary", {})
        will_pass = compliance.get("will_pass_moderation", False)
        
        if will_pass:
            print("\n✅ RESULT: Video WILL LIKELY PASS moderation")
        else:
            print("\n❌ RESULT: Video WILL LIKELY FAIL moderation")
            
            violations = data["result"].get("facebook_policy_violations", [])
            if violations:
                print(f"\n⛔ Found {len(violations)} policy violations")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_policy_check_file():
    """Test policy check with video file upload."""
    
    video_path = input("\n📁 Enter path to video file: ").strip()
    if not video_path:
        print("❌ No path provided")
        return
    
    video_path = Path(video_path)
    if not video_path.exists():
        print(f"❌ File not found: {video_path}")
        return
    
    print(f"\n📤 Uploading video for policy check...")
    print(f"   Platform: Facebook")
    print(f"   File: {video_path.name}\n")
    
    try:
        with open(video_path, "rb") as f:
            files = {"video": (video_path.name, f, "video/mp4")}
            data = {"platform": "facebook"}
            
            response = httpx.post(
                f"{BASE_URL}/check-video-upload",
                files=files,
                data=data,
                timeout=120.0
            )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return
        
        result = response.json()
        
        # Print text report
        if result.get("text_report"):
            print(result["text_report"])
        
        # Save full JSON result
        result_file = "policy_check_result.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result["result"], f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full results saved to: {result_file}")
        
        # Quick summary
        compliance = result["result"].get("compliance_summary", {})
        will_pass = compliance.get("will_pass_moderation", False)
        
        if will_pass:
            print("\n✅ RESULT: Video WILL LIKELY PASS moderation")
        else:
            print("\n❌ RESULT: Video WILL LIKELY FAIL moderation")
            
            violations = result["result"].get("facebook_policy_violations", [])
            if violations:
                print(f"\n⛔ Found {len(violations)} policy violations")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main menu."""
    print("\n" + "="*60)
    print("🔍 VIDEO POLICY COMPLIANCE CHECKER")
    print("="*60)
    
    print("\nChoose input method:")
    print("1. Check video by URL")
    print("2. Upload video file")
    print("3. Exit")
    
    choice = input("\nYour choice (1-3): ").strip()
    
    if choice == "1":
        test_policy_check_url()
    elif choice == "2":
        test_policy_check_file()
    elif choice == "3":
        print("\n👋 Goodbye!")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    try:
        while True:
            main()
            
            again = input("\n\nCheck another video? (y/n): ").strip().lower()
            if again != 'y':
                print("\n👋 Goodbye!")
                break
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
