#!/usr/bin/env python3
"""
Test script to verify that the new policy HTML report generator
works correctly with all new detailed fields from the policy checker prompt.
"""
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.policy_html_report import generate_comprehensive_policy_html


def create_mock_policy_result():
    """Create a mock policy check result with all new fields."""
    return {
        "video_description": {
            "duration_seconds": 15,
            "scene_by_scene": [
                {
                    "timestamp": "0:00-0:03",
                    "description": "Close-up of person's face looking stressed",
                    "key_elements": ["stressed expression", "office background", "dim lighting"]
                },
                {
                    "timestamp": "0:03-0:08",
                    "description": "Product showcase - mobile app interface",
                    "key_elements": ["app UI", "meditation timer", "soothing colors"]
                }
            ],
            "visual_content": "UGC-style video showing transformation from stress to relaxation",
            "people": {
                "count": 1,
                "descriptions": ["Woman, approximately 30-35 years old, office casual clothing"],
                "age_appropriateness": "всі виглядають 18+",
                "clothing_appropriateness": "відповідає стандартам",
                "actions_and_gestures": ["touching temples (stress gesture)", "smiling after using app"]
            },
            "objects_products": {
                "main_product": "Meditation mobile application",
                "visible_items": ["smartphone", "desk", "laptop", "coffee mug"],
                "potentially_problematic": []
            },
            "on_screen_text": {
                "all_text": ["Stressed at work?", "Try 5 minutes meditation", "Download now"],
                "claims_made": ["5 minutes meditation"],
                "text_to_image_ratio": "approximately 15%"
            },
            "audio_description": {
                "music": "Calm, ambient background music",
                "music_copyright_risk": "low",
                "voiceover": "Female voice explaining app benefits",
                "sound_effects": ["notification sound", "calm chime"],
                "language_appropriateness": "чиста мова"
            },
            "overall_tone": "Motivational and calming, targeting stressed professionals"
        },
        "brands_trademarks": {
            "detected_brands": [
                {
                    "brand_name": "CalmMind App",
                    "type": "logo",
                    "duration_seconds": 3.0,
                    "usage_type": "власний",
                    "potential_issue": False
                }
            ],
            "meta_platforms_mentioned": False,
            "competitor_platforms_mentioned": False,
            "celebrity_endorsement": {
                "present": False,
                "details": ""
            },
            "trademark_issues": "немає проблем",
            "brand_usage_ok": True,
            "copyright_concerns": "No concerns detected"
        },
        "prohibited_content": {
            "adult_content": {
                "nudity": False,
                "sexually_suggestive": False,
                "focus_on_body_parts": False,
                "revealing_clothing": False,
                "sexual_innuendo": False,
                "details": ""
            },
            "violence_weapons": {
                "weapons_present": False,
                "violence_depicted": False,
                "blood_gore": False,
                "dangerous_activities": False,
                "details": ""
            },
            "discriminatory_content": {
                "racial_stereotypes": False,
                "gender_discrimination": False,
                "age_discrimination": False,
                "religious_insensitivity": False,
                "body_shaming": False,
                "details": ""
            },
            "substances": {
                "tobacco": False,
                "alcohol": False,
                "drugs": False,
                "paraphernalia": False,
                "details": ""
            },
            "shocking_content": {
                "graphic_imagery": False,
                "disturbing_content": False,
                "fear_inducing": False,
                "details": ""
            }
        },
        "health_medical_claims": {
            "before_after_imagery": False,
            "weight_loss_claims": False,
            "disease_treatment_claims": False,
            "unrealistic_results": False,
            "body_focused_negative": False,
            "prescription_drugs": False,
            "medical_devices": False,
            "fda_claims": False,
            "fear_based_health_messaging": False,
            "specific_issues": []
        },
        "deceptive_practices": {
            "clickbait": False,
            "misleading_headlines": False,
            "fake_buttons": False,
            "unrealistic_promises": False,
            "fake_scarcity": False,
            "false_testimonials": False,
            "phishing_indicators": False,
            "details": ""
        },
        "personal_attributes_targeting": {
            "targets_health_conditions": False,
            "targets_financial_status": False,
            "targets_personal_hardships": False,
            "implies_knowledge_of_user": False,
            "examples": []
        },
        "audio_copyright": {
            "copyrighted_music_detected": False,
            "music_recognition": "royalty-free ambient track",
            "copyright_risk_level": "low",
            "offensive_language": False,
            "audio_issues": ""
        },
        "nsfw_check": {
            "safe_for_work": True,
            "family_friendly": True,
            "age_appropriate_13plus": True,
            "specific_concerns": [],
            "nsfw_reasons": ""
        },
        "technical_quality": {
            "resolution_adequate": True,
            "text_overlay_percentage": "approximately 15%",
            "flashing_effects": False,
            "viewing_comfort": "комфортно",
            "accessibility_concerns": "немає проблем"
        },
        "facebook_policy_violations": [
            {
                "violation_id": 1,
                "category": "Personal Attributes",
                "policy_section": "Advertising Policies - Personal Attributes",
                "severity": "medium",
                "description": "Text may imply stress level targeting",
                "timestamp_seconds": 1.5,
                "specific_frame_description": "Text overlay says 'Stressed at work?'",
                "why_its_violation": "Directly addresses viewer's emotional state which may be considered targeting personal attributes",
                "recommendation": "Change to more general phrasing like 'Need a break?' or 'Looking for calm?'",
                "alternative_approach": "Focus on solution benefits rather than problem identification"
            }
        ],
        "compliance_summary": {
            "will_pass_moderation": False,
            "confidence_level": 0.75,
            "risk_level": "medium",
            "approval_probability": "60-70%",
            "overall_assessment": "Video has good production quality and clear messaging. Main concern is potential personal attributes targeting with 'Stressed at work?' text. Recommend rephrasing to avoid direct reference to viewer's emotional state. Otherwise content is clean and appropriate.",
            "critical_blockers": [],
            "medium_risks": [
                "Personal attributes targeting in text overlay"
            ],
            "low_risks": [
                "Text overlay percentage slightly high (15%) - recommend keeping under 20%"
            ]
        },
        "feedback": {
            "main_issues": [
                {
                    "issue": "Personal attributes targeting detected in opening text",
                    "impact": "medium",
                    "must_fix": True
                }
            ],
            "required_changes": [
                {
                    "change": "Modify opening text from 'Stressed at work?' to more general phrasing",
                    "priority": "high",
                    "how_to_fix": "Replace with 'Need a moment of calm?' or 'Looking for peace?' which focuses on solution rather than problem"
                }
            ],
            "recommendations": [
                "Keep text overlay under 20% for better reach",
                "Consider adding captions for accessibility",
                "Strong UGC style works well for this category"
            ],
            "alternative_approaches": [
                "Start with solution/benefit first ('5 minutes to calm') rather than problem identification",
                "Use visual storytelling without direct questioning of viewer's state"
            ],
            "best_practices": [
                "Clear product demonstration",
                "Appropriate length (15 seconds)",
                "Family-friendly content",
                "Good production quality"
            ]
        },
        "action_items": {
            "immediate_blockers": [
                "Modify opening text to avoid personal attributes targeting"
            ],
            "recommended_improvements": [
                "Reduce text overlay percentage slightly",
                "Add captions for better accessibility"
            ],
            "optional_enhancements": [
                "Consider adding customer testimonial without health claims",
                "Test different hook variations"
            ],
            "resubmission_readiness": "потребує змін"
        },
        "metadata": {
            "video_path": "test_video.mp4",
            "video_url": "https://example.com/test_video.mp4",
            "platform": "facebook",
            "model": "models/gemini-2.0-flash",
            "analyzed_at": "2025-10-04 19:30:00"
        }
    }


def test_html_generation():
    """Test HTML generation with mock data."""
    print("🧪 Testing Policy HTML Report Generation\n")
    print("=" * 80)
    
    # Create mock result
    result = create_mock_policy_result()
    video_url = "https://example.com/test_video.mp4"
    platform = "facebook"
    
    print("✅ Mock policy result created")
    print(f"   - Violations: {len(result['facebook_policy_violations'])}")
    print(f"   - Risk Level: {result['compliance_summary']['risk_level']}")
    print(f"   - Will Pass: {result['compliance_summary']['will_pass_moderation']}")
    print()
    
    # Generate HTML
    try:
        html = generate_comprehensive_policy_html(result, video_url, platform)
        print("✅ HTML report generated successfully!")
        print(f"   - HTML length: {len(html):,} characters")
        print()
        
        # Check for key sections
        sections_to_check = [
            ("Risk Summary", "⚠️ Risk Summary"),
            ("Policy Violations", "⛔ Policy Violations"),
            ("NSFW Check", "🔞 NSFW"),
            ("Prohibited Content", "🚫 Prohibited Content"),
            ("Health Claims", "🏥 Health"),
            ("Deceptive Practices", "🎣 Deceptive"),
            ("Personal Attributes", "👤 Personal Attributes"),
            ("Brands & Trademarks", "🏷️ Brands"),
            ("Audio Copyright", "🎵 Audio"),
            ("Technical Quality", "⚙️ Technical"),
            ("Action Items", "✏️ Action Items"),
            ("Feedback", "💡 Feedback"),
            ("Overall Assessment", "📝 Overall Assessment")
        ]
        
        print("📊 Section Check:")
        for section_name, section_marker in sections_to_check:
            present = section_marker in html
            status = "✅" if present else "❌"
            print(f"   {status} {section_name}: {'Present' if present else 'Missing'}")
        print()
        
        # Check for specific new fields
        new_fields_check = [
            ("Critical Blockers", "critical_blockers" in result['compliance_summary']),
            ("Medium Risks", "medium_risks" in result['compliance_summary']),
            ("Action Items", "action_items" in result),
            ("Required Changes", "required_changes" in result['feedback']),
            ("Alternative Approaches", "alternative_approaches" in result['feedback']),
            ("Best Practices", "best_practices" in result['feedback']),
            ("Resubmission Readiness", "resubmission_readiness" in result['action_items'])
        ]
        
        print("🔍 New Fields Check:")
        for field_name, field_present in new_fields_check:
            status = "✅" if field_present else "❌"
            print(f"   {status} {field_name}: {'In data' if field_present else 'Missing'}")
        print()
        
        # Save to file
        output_file = Path(__file__).parent / "test_policy_report_output.html"
        output_file.write_text(html, encoding="utf-8")
        print(f"💾 Saved HTML report to: {output_file}")
        print(f"🌐 Open in browser: file://{output_file.absolute()}")
        print()
        
        # Check collapsible sections
        collapsible_count = html.count('class="collapsible"')
        print(f"📂 Collapsible sections: {collapsible_count}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate HTML: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_violations():
    """Test HTML with multiple violations."""
    print("\n" + "=" * 80)
    print("🧪 Testing with Multiple Violations\n")
    
    result = create_mock_policy_result()
    
    # Add more violations
    result["facebook_policy_violations"].extend([
        {
            "violation_id": 2,
            "category": "Health Claims",
            "policy_section": "Advertising Policies - Health",
            "severity": "high",
            "description": "Before/after imagery detected",
            "timestamp_seconds": 8.5,
            "specific_frame_description": "Shows transformation from stressed to relaxed",
            "why_its_violation": "May be interpreted as health claim without proper disclaimers",
            "recommendation": "Remove before/after visual metaphor or add medical disclaimer",
            "alternative_approach": "Show product benefits without transformation imagery"
        },
        {
            "violation_id": 3,
            "category": "Text Overlay",
            "policy_section": "Best Practices",
            "severity": "low",
            "description": "Text overlay slightly above recommended 20%",
            "timestamp_seconds": None,
            "specific_frame_description": "",
            "why_its_violation": "May reduce reach due to high text ratio",
            "recommendation": "Reduce text amount or spread across frames",
            "alternative_approach": "Use voiceover instead of on-screen text"
        }
    ])
    
    # Update compliance
    result["compliance_summary"]["will_pass_moderation"] = False
    result["compliance_summary"]["risk_level"] = "high"
    result["compliance_summary"]["critical_blockers"] = [
        "Health claims without proper disclaimers"
    ]
    
    result["health_medical_claims"]["before_after_imagery"] = True
    
    try:
        html = generate_comprehensive_policy_html(
            result,
            "https://example.com/test_video.mp4",
            "facebook"
        )
        
        violations_count = html.count('<div class="violation">')
        print(f"✅ Generated HTML with {violations_count} violations displayed")
        print(f"   - Critical blockers section: {'Yes' if '🚫 Critical Blockers' in html else 'No'}")
        print(f"   - Health claims flagged: {'Yes' if '🏥 Health' in html else 'No'}")
        
        # Save
        output_file = Path(__file__).parent / "test_policy_report_violations.html"
        output_file.write_text(html, encoding="utf-8")
        print(f"💾 Saved to: {output_file}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("🚀 POLICY HTML REPORT GENERATION TEST")
    print("=" * 80)
    print()
    
    # Test 1: Basic generation
    test1 = test_html_generation()
    
    # Test 2: Multiple violations
    test2 = test_with_violations()
    
    # Summary
    print("\n" + "=" * 80)
    if test1 and test2:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  {'✅' if test1 else '❌'} Basic HTML generation")
    print(f"  {'✅' if test2 else '❌'} Multiple violations handling")
    print()
    print("Generated files:")
    print("  - test_policy_report_output.html (basic)")
    print("  - test_policy_report_violations.html (with violations)")
    print()
    
    return test1 and test2


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
