#!/usr/bin/env python3
"""
List available Gemini models for video analysis.
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY is not set")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Available Gemini models:\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        video_support = "📹 Video" if "video" in str(model.supported_generation_methods).lower() else "🚫 No video"
        print(f"✅ {model.name}")
        print(f"   {video_support}")
        print(f"   Input: {model.input_token_limit if hasattr(model, 'input_token_limit') else 'N/A'} tokens")
        print(f"   Output: {model.output_token_limit if hasattr(model, 'output_token_limit') else 'N/A'} tokens")
        print()

print("\n💡 Recommended for video analysis:")
print("   • models/gemini-1.5-flash (fast & cheap)")
print("   • models/gemini-1.5-pro (accurate & capable)")
print("\n⚙️  Set via: export GEMINI_MODEL=models/gemini-1.5-flash")
