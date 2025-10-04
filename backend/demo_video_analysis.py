#!/usr/bin/env python3
"""
Demo: Analyze first cached video from the creatives.
"""
import os
import json
from pathlib import Path

# Check for cached videos
cache_dir = Path(__file__).parent / ".cache" / "videos"

if not cache_dir.exists():
    print("❌ No .cache/videos directory found. Run MVP pipeline first to cache videos.")
    exit(1)

videos = list(cache_dir.glob("*.mp4"))
if not videos:
    print("❌ No cached videos found. Run MVP pipeline first.")
    exit(1)

print(f"✅ Found {len(videos)} cached video(s)")
print(f"📹 Will analyze: {videos[0].name}\n")

# Import analyzer
from src.analysis.video_analyzer import analyze_video_prototype

# Analyze
output_path = Path(__file__).parent / "analysis" / f"video_analysis_{videos[0].stem}.json"
output_path.parent.mkdir(exist_ok=True)

print(f"🎬 Analyzing video: {videos[0]}")
print(f"💾 Output will be saved to: {output_path}\n")

result = analyze_video_prototype(str(videos[0]), str(output_path))

print("\n" + "="*60)
print("📊 ANALYSIS RESULTS")
print("="*60)

# Pretty print key sections
if "hook" in result and result["hook"]:
    print("\n🎣 HOOK:")
    print(f"  Time: {result['hook'].get('time_start_s', 0)}-{result['hook'].get('time_end_s', 3)}s")
    print(f"  Tactic: {result['hook'].get('tactic', 'N/A')}")
    print(f"  Description: {result['hook'].get('description', 'N/A')}")
    print(f"  Strength: {result['hook'].get('strength', 'N/A')}")

if "visual_style" in result and result["visual_style"]:
    print("\n🎨 VISUAL STYLE:")
    print(f"  Style: {result['visual_style'].get('style', 'N/A')}")
    print(f"  Effects: {', '.join(result['visual_style'].get('effects', []))}")
    print(f"  Has Captions: {result['visual_style'].get('has_captions', 'N/A')}")

if "cta" in result and result["cta"]:
    print("\n📢 CALL TO ACTION:")
    for i, cta in enumerate(result["cta"], 1):
        print(f"  CTA {i}:")
        print(f"    Time: {cta.get('timecode_s', 'N/A')}s")
        print(f"    Text: {cta.get('text', 'N/A')}")
        print(f"    Channel: {cta.get('channel', 'N/A')}")
        print(f"    Strength: {cta.get('strength', 'N/A')}")

if "product_showcase" in result and result["product_showcase"]:
    print("\n📱 PRODUCT SHOWCASE:")
    print(f"  Type: {result['product_showcase'].get('type', 'N/A')}")
    print(f"  Timecodes: {result['product_showcase'].get('timecodes_s', [])}")
    print(f"  Features: {result['product_showcase'].get('key_features', [])}")
    print(f"  Clarity: {result['product_showcase'].get('clarity_score', 'N/A')}")

if "scores" in result and result["scores"]:
    print("\n📈 SCORES:")
    for key, value in result["scores"].items():
        print(f"  {key}: {value}")

if "summary" in result:
    print(f"\n💡 SUMMARY:")
    print(f"  {result['summary']}")

print("\n" + "="*60)
print(f"📄 Full JSON saved to: {output_path}")
print("="*60)
