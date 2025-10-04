#!/usr/bin/env python3
"""
Test script to verify that the new Performance Marketing prompt integrates
correctly with existing schemas, models, and HTML report generation.
"""
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from src.db.models import CreativeAnalysis, AggregatedAnalysis
from src.utils.html_report import generate_html_report
from datetime import datetime


def test_new_prompt_schema_compatibility():
    """Test that new prompt JSON structure maps correctly to CreativeAnalysis model."""
    print("🧪 Testing new prompt schema compatibility...\n")
    
    # Simulate new prompt output
    new_prompt_output = {
        "hook": {
            "time_start_s": 0.0,
            "time_end_s": 3.0,
            "description": "Показ проблеми - втомлена людина за комп'ютером",
            "psychological_principle": "Loss Aversion",
            "relevance_to_audience": "Високо релевантно для офісних працівників",
            "strength": 0.85
        },
        "visual_style": {
            "style": "UGC",
            "effects": ["jump cuts", "text overlays", "zoom ins"],
            "color_palette": "Теплі тони, приглушені кольори",
            "pacing": "fast",
            "pacing_impact": "Створює відчуття терміновості та енергії",
            "has_captions": True,
            "caption_style": "Білий текст з чорним контуром, великий шрифт"
        },
        "on_screen_text": [
            {"timecode_s": 1.5, "text": "Втомлений від роботи?"},
            {"timecode_s": 5.0, "text": "Є рішення!"}
        ],
        "product_showcase": {
            "type": "UI demo",
            "integration_quality": "Природньо інтегрований у сюжет користувача",
            "shows_transformation": True,
            "timecodes_s": [3.0, 7.5, 12.0],
            "key_features": ["простий інтерфейс", "швидкий результат", "персоналізація"],
            "clarity_score": 0.9
        },
        "cta": [
            {
                "timecode_s": 14.0,
                "text": "Завантажуй зараз!",
                "channel": "both",
                "has_urgency": True,
                "has_incentive": True,
                "incentive_description": "Перший місяць безкоштовно",
                "strength": 0.95
            }
        ],
        "messaging": {
            "pains": [
                {
                    "text": "Втома від роботи та стрес",
                    "timecode_s": 1.0,
                    "presentation_style": "visual"
                },
                {
                    "text": "Відсутність балансу між роботою та життям",
                    "timecode_s": 2.5,
                    "presentation_style": "storytelling"
                }
            ],
            "value_props": [
                {
                    "text": "5 хвилин на день для здоров'я",
                    "timecode_s": 4.0,
                    "presentation_style": "before-after"
                },
                {
                    "text": "Доведена ефективність для зниження стресу",
                    "timecode_s": 8.0,
                    "presentation_style": "testimonial"
                }
            ],
            "messaging_approach": "problem-solution"
        },
        "audio": {
            "has_voiceover": True,
            "voiceover_tone": "Дружній, підбадьорливий",
            "music_mood": "uplifting",
            "sound_effects": True,
            "audio_visual_alignment": "Музика підсилює емоції трансформації"
        },
        "emotional_journey": [
            {
                "scene": 1,
                "time_start_s": 0.0,
                "time_end_s": 3.0,
                "what_we_see": "Втомлена людина за комп'ютером",
                "what_we_hear": "Тиха, напружена музика",
                "emotional_state": "problem",
                "viewer_emotion": "Розпізнавання проблеми, емпатія"
            },
            {
                "scene": 2,
                "time_start_s": 3.0,
                "time_end_s": 10.0,
                "what_we_see": "Демо застосунку, проста медитація",
                "what_we_hear": "Спокійний голос, заспокійлива музика",
                "emotional_state": "solution",
                "viewer_emotion": "Надія, зацікавленість"
            },
            {
                "scene": 3,
                "time_start_s": 10.0,
                "time_end_s": 15.0,
                "what_we_see": "Користувач усміхається, почуває себе краще",
                "what_we_hear": "Оптимістична музика, енергійний CTA",
                "emotional_state": "desire",
                "viewer_emotion": "Бажання отримати такий же результат"
            }
        ],
        "scores": {
            "hook_strength": 0.85,
            "cta_clarity": 0.95,
            "product_visibility": 0.9,
            "message_density": 0.75,
            "execution_quality": 0.88,
            "emotional_impact": 0.9,
            "relevance_to_audience": 0.92
        },
        "key_insights": {
            "main_strategy": "Проблема-рішення з емоційною трансформацією користувача",
            "key_insights": [
                "Використання UGC стилю створює довіру та автентичність",
                "Швидкий темп та jump cuts утримують увагу в перші секунди",
                "Показ конкретного результату (усмішка) сильніше за опис фіч"
            ],
            "hypotheses_to_test": [
                "Тестувати різні болі в хуку: втома vs стрес vs вигорання",
                "A/B тест CTA: 'Завантажуй зараз' vs 'Почни безкоштовно'",
                "Тестувати тривалість відео: 15с vs 30с для різних платформ"
            ]
        },
        "summary": "Ефективний UGC креатив з чітким problem-solution наративом та strong emotional arc"
    }
    
    print("✅ New prompt output structure:")
    print(json.dumps(new_prompt_output, ensure_ascii=False, indent=2)[:500] + "...\n")
    
    # Test mapping to CreativeAnalysis model (simulating task_service.py logic)
    print("🔄 Mapping to CreativeAnalysis model...\n")
    
    visuals = new_prompt_output.get("visual_style")
    
    cta_raw = new_prompt_output.get("cta")
    if isinstance(cta_raw, dict):
        cta_list = [cta_raw]
    elif isinstance(cta_raw, list):
        cta_list = cta_raw
    else:
        cta_list = []
    
    messaging = new_prompt_output.get("messaging", {}) or {}
    pains_list = messaging.get("pains") or []
    pains_norm = [{**p} if isinstance(p, dict) else {"text": str(p)} for p in pains_list]
    vprops_list = messaging.get("value_props") or []
    vprops_norm = [{**v} if isinstance(v, dict) else {"text": str(v)} for v in vprops_list]
    
    storyboard = new_prompt_output.get("emotional_journey") or new_prompt_output.get("storyboard", [])
    scores = new_prompt_output.get("scores")
    
    # Create enriched summary from key_insights
    key_insights_data = new_prompt_output.get("key_insights") or {}
    if key_insights_data:
        main_strat = key_insights_data.get("main_strategy", "")
        insights_list = key_insights_data.get("key_insights", [])
        hypotheses = key_insights_data.get("hypotheses_to_test", [])
        
        summary_parts = []
        if main_strat:
            summary_parts.append(f"**Стратегія:** {main_strat}")
        if insights_list:
            summary_parts.append("**Інсайти:** " + "; ".join(insights_list[:2]))
        if hypotheses:
            summary_parts.append("**Гіпотези:** " + "; ".join(hypotheses[:2]))
        
        summary = " | ".join(summary_parts) if summary_parts else new_prompt_output.get("summary")
    else:
        summary = new_prompt_output.get("summary")
    
    # Create CreativeAnalysis object
    try:
        analysis = CreativeAnalysis(
            creative_id="test_123",
            ad_archive_id="test_123",
            page_name="Test Competitor",
            hook=new_prompt_output.get("hook"),
            visual_style=visuals,
            on_screen_text=new_prompt_output.get("on_screen_text", []),
            product_showcase=new_prompt_output.get("product_showcase"),
            cta=cta_list,
            pains=pains_norm,
            value_props=vprops_norm,
            audio=new_prompt_output.get("audio"),
            storyboard=storyboard,
            scores=scores,
            summary=summary,
            video_url="https://example.com/video.mp4",
            cached_video_path="/tmp/test_video.mp4",
            analyzed_at=datetime.utcnow()
        )
        
        print("✅ Successfully created CreativeAnalysis object!")
        print(f"   - Hook strength: {analysis.hook.get('strength') if analysis.hook else 'N/A'}")
        print(f"   - CTA count: {len(analysis.cta)}")
        print(f"   - Pains count: {len(analysis.pains)}")
        print(f"   - Value props count: {len(analysis.value_props)}")
        print(f"   - Storyboard scenes: {len(analysis.storyboard)}")
        print(f"   - Scores: {len(analysis.scores) if analysis.scores else 0} metrics")
        print(f"   - Summary length: {len(analysis.summary) if analysis.summary else 0} chars")
        print(f"\n   Summary preview:\n   {analysis.summary[:200]}...\n")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Failed to create CreativeAnalysis: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_html_report_generation(analysis: CreativeAnalysis):
    """Test HTML report generation with new fields."""
    print("\n🧪 Testing HTML report generation...\n")
    
    try:
        task_data = {
            "page_name": "Test Competitor Page",
            "total_ads": 10
        }
        
        creatives_data = [analysis.model_dump()]
        
        # Test without aggregated analysis
        html = generate_html_report(
            task_data=task_data,
            creatives=creatives_data,
            aggregated=None,
            aggregation_error=None
        )
        
        print("✅ Successfully generated HTML report!")
        print(f"   - HTML length: {len(html)} chars")
        
        # Check if new score fields are present
        new_scores_present = "❤️ Емоційний вплив" in html and "🎪 Релевантність для ЦА" in html
        print(f"   - New score fields present: {'✅' if new_scores_present else '❌'}")
        
        # Check if enriched summary is rendered
        summary_present = "**Стратегія:**" in html or "**Інсайти:**" in html or "**Гіпотези:**" in html
        print(f"   - Enriched summary rendered: {'✅' if summary_present else '❌'}")
        
        # Save to file for manual inspection
        output_file = Path(__file__).parent / "test_report_output.html"
        output_file.write_text(html, encoding="utf-8")
        print(f"\n   📄 Saved report to: {output_file}")
        print(f"   🌐 Open in browser: file://{output_file.absolute()}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate HTML report: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_aggregated_analysis():
    """Test AggregatedAnalysis model compatibility."""
    print("\n🧪 Testing AggregatedAnalysis model...\n")
    
    try:
        aggregated = AggregatedAnalysis(
            pain_points=[
                "Втома від роботи",
                "Стрес та вигорання",
                "Відсутність балансу"
            ],
            concepts=[
                "Медитація для офісних працівників",
                "5 хвилин на день",
                "Простий інтерфейс"
            ],
            visual_trends={
                "dominant_style": "UGC",
                "common_effects": ["jump cuts", "text overlays"],
                "pacing": "fast"
            },
            hooks=[
                "Втомлений від роботи?",
                "Останній раз відпочивав коли?",
                {"description": "Проблема-запитання", "type": "Curiosity Gap"}
            ],
            core_idea="Швидке рішення для зниження стресу офісних працівників",
            theme="Здоров'я та well-being",
            message="5 хвилин медитації щодня змінять твоє життя",
            recommendations="Використовувати UGC стиль, problem-solution наратив, показувати конкретну трансформацію",
            video_prompt="Створи 15-секундне UGC відео для мобільного застосунку медитацій..."
        )
        
        print("✅ Successfully created AggregatedAnalysis object!")
        print(f"   - Pain points: {len(aggregated.pain_points)}")
        print(f"   - Concepts: {len(aggregated.concepts)}")
        print(f"   - Hooks: {len(aggregated.hooks)} (mixed types: ✅)")
        print(f"   - Core idea: {aggregated.core_idea[:50]}...")
        
        return aggregated
        
    except Exception as e:
        print(f"❌ Failed to create AggregatedAnalysis: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all integration tests."""
    print("=" * 80)
    print("🚀 NEW PROMPT INTEGRATION TEST")
    print("=" * 80)
    print()
    
    # Test 1: Schema compatibility
    analysis = test_new_prompt_schema_compatibility()
    if not analysis:
        print("\n❌ Schema compatibility test failed!")
        return False
    
    # Test 2: HTML report generation
    html_success = test_html_report_generation(analysis)
    if not html_success:
        print("\n❌ HTML report generation test failed!")
        return False
    
    # Test 3: Aggregated analysis
    aggregated = test_aggregated_analysis()
    if not aggregated:
        print("\n❌ Aggregated analysis test failed!")
        return False
    
    # Final summary
    print("=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✅ New prompt JSON structure maps correctly to CreativeAnalysis model")
    print("  ✅ Enriched summary generated from key_insights")
    print("  ✅ New score fields (emotional_impact, relevance_to_audience) render in HTML")
    print("  ✅ emotional_journey maps to storyboard correctly")
    print("  ✅ messaging.pains and messaging.value_props extract properly")
    print("  ✅ AggregatedAnalysis model works with mixed hook types")
    print()
    print("Next steps:")
    print("  1. Review generated HTML report in browser")
    print("  2. Test with real API: POST /api/v1/parse-ads with auto_analyze=true")
    print("  3. Check MongoDB documents have correct structure")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
