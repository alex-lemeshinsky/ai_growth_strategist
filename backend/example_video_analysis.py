#!/usr/bin/env python3
"""
Example: How to integrate video analysis into the creative analysis workflow.
"""

# Example 1: Analyze a single video file directly
def example_direct_analysis():
    from src.analysis.video_analyzer import analyze_video_file
    
    video_path = ".cache/videos/your_video.mp4"
    
    meta = {
        "page_name": "Guru Apps",
        "creative_id": "1285097509489804",
        "platforms": ["FACEBOOK", "INSTAGRAM"]
    }
    
    result = analyze_video_file(video_path, meta=meta)
    
    print("Hook:", result.get("hook"))
    print("CTAs:", result.get("cta"))
    print("Scores:", result.get("scores"))
    return result


# Example 2: Batch analyze all cached videos
def example_batch_analysis():
    from pathlib import Path
    from src.analysis.video_analyzer import analyze_video_file
    import json
    
    cache_dir = Path(".cache/videos")
    output_dir = Path("analysis/video_analyses")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    for video_path in cache_dir.glob("*.mp4"):
        print(f"\nAnalyzing: {video_path.name}")
        
        try:
            result = analyze_video_file(str(video_path))
            result["video_filename"] = video_path.name
            results.append(result)
            
            # Save individual result
            output_path = output_dir / f"{video_path.stem}_analysis.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error analyzing {video_path.name}: {e}")
    
    # Save combined results
    combined_path = output_dir / "all_analyses.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Analyzed {len(results)} videos")
    print(f"📁 Results saved to: {output_dir}")
    return results


# Example 3: Compare hooks across multiple videos
def example_compare_hooks():
    from pathlib import Path
    from src.analysis.video_analyzer import analyze_video_file
    
    cache_dir = Path(".cache/videos")
    videos = list(cache_dir.glob("*.mp4"))[:3]  # Analyze first 3
    
    hooks = []
    for video_path in videos:
        result = analyze_video_file(str(video_path))
        if "hook" in result and result["hook"]:
            hooks.append({
                "video": video_path.name,
                "hook": result["hook"]
            })
    
    # Sort by hook strength
    hooks.sort(key=lambda x: x["hook"].get("strength", 0), reverse=True)
    
    print("\n📊 Hook Comparison (sorted by strength):")
    for item in hooks:
        hook = item["hook"]
        print(f"\n{item['video']}:")
        print(f"  Strength: {hook.get('strength', 'N/A')}")
        print(f"  Tactic: {hook.get('tactic', 'N/A')}")
        print(f"  Description: {hook.get('description', 'N/A')[:80]}...")
    
    return hooks


# Example 4: Extract all on-screen text with timestamps
def example_extract_text():
    from pathlib import Path
    from src.analysis.video_analyzer import analyze_video_file
    
    cache_dir = Path(".cache/videos")
    video_path = list(cache_dir.glob("*.mp4"))[0]
    
    result = analyze_video_file(str(video_path))
    
    if "on_screen_text" in result:
        print(f"\n📝 On-screen text from {video_path.name}:")
        for item in result["on_screen_text"]:
            print(f"  {item.get('timecode_s', 'N/A')}s: {item.get('text', 'N/A')}")
    
    return result.get("on_screen_text", [])


# Example 5: Get storyboard breakdown
def example_get_storyboard():
    from pathlib import Path
    from src.analysis.video_analyzer import analyze_video_file
    
    cache_dir = Path(".cache/videos")
    video_path = list(cache_dir.glob("*.mp4"))[0]
    
    result = analyze_video_file(str(video_path))
    
    if "storyboard" in result:
        print(f"\n🎬 Storyboard for {video_path.name}:")
        for scene in result["storyboard"]:
            print(f"\nScene {scene.get('scene', 'N/A')}: "
                  f"{scene.get('time_start_s', 'N/A')}-{scene.get('time_end_s', 'N/A')}s")
            print(f"  Visual: {scene.get('what_we_see', 'N/A')}")
            print(f"  Audio: {scene.get('what_we_hear', 'N/A')}")
    
    return result.get("storyboard", [])


if __name__ == "__main__":
    import sys
    
    examples = {
        "1": ("Direct analysis", example_direct_analysis),
        "2": ("Batch analysis", example_batch_analysis),
        "3": ("Compare hooks", example_compare_hooks),
        "4": ("Extract text", example_extract_text),
        "5": ("Get storyboard", example_get_storyboard),
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in examples:
        name, func = examples[sys.argv[1]]
        print(f"\n🚀 Running: {name}\n")
        func()
    else:
        print("Usage: python example_video_analysis.py [1-5]")
        print("\nExamples:")
        for key, (name, _) in examples.items():
            print(f"  {key}: {name}")
