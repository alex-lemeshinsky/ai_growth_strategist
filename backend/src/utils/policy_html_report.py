"""
Comprehensive HTML report generator for video policy compliance checks.
Supports all detailed fields from the enhanced policy checker prompt.
"""
from typing import Dict, Any, List
from datetime import datetime


def generate_comprehensive_policy_html(result: dict, video_url: str, platform: str) -> str:
    """
    Generate comprehensive HTML report for policy check results.
    Shows all detailed analysis from the new policy checker prompt.
    
    Args:
        result: Policy check result dictionary
        video_url: URL to video
        platform: Platform name
        
    Returns:
        HTML string
    """
    compliance = result.get("compliance_summary", {})
    will_pass = compliance.get("will_pass_moderation", False)
    risk_level = compliance.get("risk_level", "unknown")
    confidence = compliance.get("confidence_level", compliance.get("confidence", 0))
    
    status_emoji = "✅" if will_pass else "❌"
    status_text = "PASS" if will_pass else "FAIL"
    status_color = "#10b981" if will_pass else "#ef4444"
    
    risk_colors = {
        "low": "#10b981",
        "medium": "#f59e0b",
        "high": "#ef4444",
        "critical": "#dc2626"
    }
    risk_color = risk_colors.get(risk_level, "#6b7280")
    
    html = f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Policy Compliance Report - {platform.upper()}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        
        .status-banner {{
            background: {status_color};
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .metrics {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }}
        
        .metric {{
            flex: 1;
            min-width: 150px;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid {risk_color};
        }}
        
        .metric-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }}
        
        .section {{
            margin: 30px 0;
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .violation {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }}
        
        .violation-header {{
            font-weight: bold;
            color: #dc2626;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-critical {{ background: #fee2e2; color: #dc2626; }}
        .badge-high {{ background: #fed7aa; color: #ea580c; }}
        .badge-medium {{ background: #fef3c7; color: #d97706; }}
        .badge-low {{ background: #dbeafe; color: #2563eb; }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        
        .info-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }}
        
        .info-card h4 {{
            font-size: 14px;
            color: #667eea;
            margin-bottom: 8px;
        }}
        
        .info-card p {{
            font-size: 13px;
            color: #555;
        }}
        
        .check-item {{
            display: flex;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 6px;
        }}
        
        .check-pass {{ border-left: 3px solid #10b981; }}
        .check-fail {{ border-left: 3px solid #ef4444; }}
        
        .check-icon {{
            margin-right: 10px;
            font-size: 18px;
        }}
        
        .video-container {{
            margin: 20px 0;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        video {{
            width: 100%;
            max-height: 500px;
            display: block;
        }}
        
        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 6px;
        }}
        
        .success-box {{
            background: #d1fae5;
            border-left: 4px solid #10b981;
            padding: 15px;
            margin: 15px 0;
            border-radius: 6px;
        }}
        
        .action-items {{
            background: #f3f4f6;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .action-items h3 {{
            color: #374151;
            margin-bottom: 12px;
        }}
        
        .action-items ul {{
            list-style: none;
            padding: 0;
        }}
        
        .action-items li {{
            padding: 8px 0;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .action-items li:before {{
            content: "→";
            margin-right: 10px;
            color: #667eea;
            font-weight: bold;
        }}
        
        .collapsible {{
            cursor: pointer;
            user-select: none;
        }}
        
        .collapsible:after {{
            content: " ▼";
            font-size: 12px;
            margin-left: 5px;
        }}
        
        .collapsible.active:after {{
            content: " ▲";
        }}
        
        .collapsible-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .collapsible-content.active {{
            max-height: 2000px;
        }}
        
        @media (max-width: 768px) {{
            .metrics {{
                flex-direction: column;
            }}
            .info-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Detailed Policy Compliance Report</h1>
            <p><strong>Platform:</strong> {platform.upper()}</p>
            <p><strong>Analyzed:</strong> {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        </div>
        
        <div class="status-banner">
            {status_emoji} MODERATION STATUS: {status_text}
        </div>
        
        <div class="content">
"""
    
    # Metrics section
    html += f"""
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Risk Level</div>
                    <div class="metric-value" style="color: {risk_color}">{risk_level.upper()}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{confidence:.0%}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Violations Found</div>
                    <div class="metric-value">{len(result.get('facebook_policy_violations', []))}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Approval Probability</div>
                    <div class="metric-value">{compliance.get('approval_probability', 'N/A')}</div>
                </div>
            </div>
"""
    
    # Video section
    html += f"""
            <div class="section">
                <h2 class="section-title">🎥 Video</h2>
                <div class="video-container">
                    <video controls preload="metadata">
                        <source src="{video_url}" type="video/mp4">
                        Your browser does not support video.
                    </video>
                </div>
            </div>
"""
    
    # Critical blockers/risks
    critical_blockers = compliance.get("critical_blockers", [])
    medium_risks = compliance.get("medium_risks", [])
    low_risks = compliance.get("low_risks", [])
    
    if critical_blockers or medium_risks:
        html += """
            <div class="section">
                <h2 class="section-title">⚠️ Risk Summary</h2>
"""
        if critical_blockers:
            html += """
                <div class="warning-box">
                    <h3 style="color: #dc2626; margin-bottom: 10px;">🚫 Critical Blockers:</h3>
                    <ul>
"""
            for blocker in critical_blockers:
                html += f"                        <li>{blocker}</li>\n"
            html += "                    </ul>\n                </div>\n"
        
        if medium_risks:
            html += """
                <div class="warning-box" style="background: #fef3c7;">
                    <h3 style="color: #d97706; margin-bottom: 10px;">⚡ Medium Risks:</h3>
                    <ul>
"""
            for risk in medium_risks:
                html += f"                        <li>{risk}</li>\n"
            html += "                    </ul>\n                </div>\n"
        
        if low_risks:
            html += """
                <div class="info-card">
                    <h4>ℹ️ Low Risks:</h4>
                    <ul style="margin-left: 20px; margin-top: 8px;">
"""
            for risk in low_risks:
                html += f"                        <li>{risk}</li>\n"
            html += "                    </ul>\n                </div>\n"
        
        html += "            </div>\n"
    
    # Violations
    violations = result.get("facebook_policy_violations", [])
    if violations:
        html += f"""
            <div class="section">
                <h2 class="section-title">⛔ Policy Violations ({len(violations)})</h2>
"""
        for idx, v in enumerate(violations, 1):
            severity = v.get("severity", "unknown")
            badge_class = f"badge-{severity}"
            
            html += f"""
                <div class="violation">
                    <div class="violation-header">
                        <span class="badge {badge_class}">{severity}</span>
                        <span>#{idx} {v.get('category', 'Unknown Category')}</span>
                    </div>
                    <p><strong>Policy Section:</strong> {v.get('policy_section', 'N/A')}</p>
                    <p><strong>Description:</strong> {v.get('description', 'No description')}</p>
                    {f'<p><strong>Timestamp:</strong> {v["timestamp_seconds"]}s - {v.get("specific_frame_description", "")}</p>' if v.get('timestamp_seconds') else ''}
                    {f'<p><strong>Why it\'s a violation:</strong> {v["why_its_violation"]}</p>' if v.get('why_its_violation') else ''}
                    {f'<p style="color: #059669; margin-top: 10px;"><strong>💡 Recommendation:</strong> {v["recommendation"]}</p>' if v.get('recommendation') else ''}
                    {f'<p style="color: #0891b2;"><strong>🔄 Alternative:</strong> {v["alternative_approach"]}</p>' if v.get('alternative_approach') else ''}
                </div>
"""
        html += "            </div>\n"
    
    # NSFW Check
    nsfw = result.get("nsfw_check", {})
    if nsfw:
        safe_for_work = nsfw.get("safe_for_work", True)
        html += f"""
            <div class="section">
                <h2 class="section-title">🔞 NSFW & Safety Check</h2>
                <div class="info-grid">
                    <div class="check-item {'check-pass' if safe_for_work else 'check-fail'}">
                        <span class="check-icon">{'✅' if safe_for_work else '❌'}</span>
                        <span>Safe for Work: {'Yes' if safe_for_work else 'No'}</span>
                    </div>
                    <div class="check-item {'check-pass' if nsfw.get('family_friendly') else 'check-fail'}">
                        <span class="check-icon">{'✅' if nsfw.get('family_friendly') else '❌'}</span>
                        <span>Family Friendly: {'Yes' if nsfw.get('family_friendly') else 'No'}</span>
                    </div>
                    <div class="check-item {'check-pass' if nsfw.get('age_appropriate_13plus') else 'check-fail'}">
                        <span class="check-icon">{'✅' if nsfw.get('age_appropriate_13plus') else '❌'}</span>
                        <span>Age 13+ Appropriate: {'Yes' if nsfw.get('age_appropriate_13plus') else 'No'}</span>
                    </div>
                </div>
                {f'<div class="warning-box"><strong>Concerns:</strong> {", ".join(nsfw.get("specific_concerns", []))}</div>' if nsfw.get('specific_concerns') else ''}
                {f'<div class="warning-box"><strong>NSFW Reasons:</strong> {nsfw.get("nsfw_reasons")}</div>' if nsfw.get('nsfw_reasons') else ''}
            </div>
"""
    
    # Prohibited Content Checks
    prohibited = result.get("prohibited_content", {})
    if prohibited:
        html += """
            <div class="section">
                <h2 class="section-title collapsible">🚫 Prohibited Content Checks</h2>
                <div class="collapsible-content">
"""
        
        # Adult content
        adult = prohibited.get("adult_content", {})
        if any(adult.values()):
            html += """
                    <div class="info-card">
                        <h4>👗 Adult Content:</h4>
"""
            checks = [
                ("nudity", "Nudity"),
                ("sexually_suggestive", "Sexually Suggestive"),
                ("focus_on_body_parts", "Focus on Body Parts"),
                ("revealing_clothing", "Revealing Clothing"),
                ("sexual_innuendo", "Sexual Innuendo")
            ]
            for key, label in checks:
                if adult.get(key):
                    html += f'                        <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
            if adult.get("details"):
                html += f'                        <p><strong>Details:</strong> {adult["details"]}</p>\n'
            html += "                    </div>\n"
        
        # Violence & Weapons
        violence = prohibited.get("violence_weapons", {})
        if any(violence.values()):
            html += """
                    <div class="info-card">
                        <h4>⚔️ Violence & Weapons:</h4>
"""
            checks = [
                ("weapons_present", "Weapons Present"),
                ("violence_depicted", "Violence Depicted"),
                ("blood_gore", "Blood/Gore"),
                ("dangerous_activities", "Dangerous Activities")
            ]
            for key, label in checks:
                if violence.get(key):
                    html += f'                        <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
            if violence.get("details"):
                html += f'                        <p><strong>Details:</strong> {violence["details"]}</p>\n'
            html += "                    </div>\n"
        
        # Substances
        substances = prohibited.get("substances", {})
        if any(substances.values()):
            html += """
                    <div class="info-card">
                        <h4>🚬 Substances:</h4>
"""
            checks = [
                ("tobacco", "Tobacco"),
                ("alcohol", "Alcohol"),
                ("drugs", "Drugs"),
                ("paraphernalia", "Paraphernalia")
            ]
            for key, label in checks:
                if substances.get(key):
                    html += f'                        <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
            if substances.get("details"):
                html += f'                        <p><strong>Details:</strong> {substances["details"]}</p>\n'
            html += "                    </div>\n"
        
        # Discriminatory content
        discrim = prohibited.get("discriminatory_content", {})
        if any(discrim.values()):
            html += """
                    <div class="info-card">
                        <h4>⚖️ Discriminatory Content:</h4>
"""
            checks = [
                ("racial_stereotypes", "Racial Stereotypes"),
                ("gender_discrimination", "Gender Discrimination"),
                ("age_discrimination", "Age Discrimination"),
                ("religious_insensitivity", "Religious Insensitivity"),
                ("body_shaming", "Body Shaming")
            ]
            for key, label in checks:
                if discrim.get(key):
                    html += f'                        <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
            if discrim.get("details"):
                html += f'                        <p><strong>Details:</strong> {discrim["details"]}</p>\n'
            html += "                    </div>\n"
        
        html += "                </div>\n            </div>\n"
    
    # Health & Medical Claims
    health = result.get("health_medical_claims", {})
    if health and any([health.get("before_after_imagery"), health.get("weight_loss_claims"), 
                       health.get("disease_treatment_claims"), health.get("specific_issues")]):
        html += """
            <div class="section">
                <h2 class="section-title">🏥 Health & Medical Claims</h2>
"""
        checks = [
            ("before_after_imagery", "Before/After Imagery", "critical"),
            ("weight_loss_claims", "Weight Loss Claims", "high"),
            ("disease_treatment_claims", "Disease Treatment Claims", "critical"),
            ("unrealistic_results", "Unrealistic Results", "high"),
            ("body_focused_negative", "Body-Focused Negative", "medium"),
            ("prescription_drugs", "Prescription Drugs", "critical"),
            ("medical_devices", "Medical Devices", "high"),
            ("fda_claims", "FDA Claims", "critical"),
            ("fear_based_health_messaging", "Fear-Based Messaging", "medium")
        ]
        
        has_issues = False
        for key, label, severity in checks:
            if health.get(key):
                has_issues = True
                html += f'                <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label} <span class="badge badge-{severity}">{severity}</span></span></div>\n'
        
        if not has_issues:
            html += '                <div class="success-box">✅ No health/medical claim violations detected</div>\n'
        
        specific_issues = health.get("specific_issues", [])
        if specific_issues:
            html += "                <h3 style=\"margin-top: 15px;\">Specific Issues:</h3>\n"
            for issue in specific_issues:
                severity = issue.get("severity", "medium")
                html += f"""
                <div class="warning-box">
                    <span class="badge badge-{severity}">{severity}</span>
                    <strong>{issue.get('type', 'Unknown')}:</strong> {issue.get('description', 'No description')}
                </div>
"""
        html += "            </div>\n"
    
    # Deceptive Practices
    deceptive = result.get("deceptive_practices", {})
    if deceptive and any([deceptive.get("clickbait"), deceptive.get("misleading_headlines"),
                          deceptive.get("fake_buttons"), deceptive.get("unrealistic_promises")]):
        html += """
            <div class="section">
                <h2 class="section-title">🎣 Deceptive Practices</h2>
"""
        checks = [
            ("clickbait", "Clickbait"),
            ("misleading_headlines", "Misleading Headlines"),
            ("fake_buttons", "Fake Buttons/Elements"),
            ("unrealistic_promises", "Unrealistic Promises"),
            ("fake_scarcity", "Fake Scarcity"),
            ("false_testimonials", "False Testimonials"),
            ("phishing_indicators", "Phishing Indicators")
        ]
        
        for key, label in checks:
            if deceptive.get(key):
                html += f'                <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
        
        if deceptive.get("details"):
            html += f'                <div class="warning-box"><strong>Details:</strong> {deceptive["details"]}</div>\n'
        
        html += "            </div>\n"
    
    # Personal Attributes Targeting
    personal_attrs = result.get("personal_attributes_targeting", {})
    if personal_attrs and any([personal_attrs.get("targets_health_conditions"),
                               personal_attrs.get("targets_financial_status")]):
        html += """
            <div class="section">
                <h2 class="section-title">👤 Personal Attributes Targeting</h2>
                <div class="warning-box">
                    <p><strong>⚠️ Facebook prohibits ads that target or imply knowledge of personal attributes.</strong></p>
"""
        checks = [
            ("targets_health_conditions", "Targets Health Conditions"),
            ("targets_financial_status", "Targets Financial Status"),
            ("targets_personal_hardships", "Targets Personal Hardships"),
            ("implies_knowledge_of_user", "Implies Knowledge of User")
        ]
        
        for key, label in checks:
            if personal_attrs.get(key):
                html += f'                    <div class="check-item check-fail"><span class="check-icon">❌</span><span>{label}</span></div>\n'
        
        examples = personal_attrs.get("examples", [])
        if examples:
            html += "                    <p><strong>Examples:</strong></p><ul>\n"
            for example in examples:
                html += f"                        <li>{example}</li>\n"
            html += "                    </ul>\n"
        
        html += "                </div>\n            </div>\n"
    
    # Brands & Trademarks
    brands = result.get("brands_trademarks", {})
    detected_brands = brands.get("detected_brands", [])
    if detected_brands or brands.get("meta_platforms_mentioned") or brands.get("competitor_platforms_mentioned"):
        html += """
            <div class="section">
                <h2 class="section-title collapsible">🏷️ Brands & Trademarks</h2>
                <div class="collapsible-content">
"""
        if detected_brands:
            html += "                    <h3>Detected Brands:</h3>\n"
            for brand in detected_brands:
                issue_class = "check-fail" if brand.get("potential_issue") else "check-pass"
                icon = "⚠️" if brand.get("potential_issue") else "✅"
                html += f"""
                    <div class="check-item {issue_class}">
                        <span class="check-icon">{icon}</span>
                        <span><strong>{brand.get('brand_name')}</strong> ({brand.get('type')}) - {brand.get('duration_seconds', 0)}s - {brand.get('usage_type', 'unknown')}</span>
                    </div>
"""
        
        if brands.get("meta_platforms_mentioned"):
            html += '                    <div class="warning-box">⚠️ Meta platforms (Facebook/Instagram) mentioned - requires permission</div>\n'
        
        if brands.get("competitor_platforms_mentioned"):
            html += '                    <div class="warning-box">⚠️ Competitor platforms mentioned</div>\n'
        
        celebrity = brands.get("celebrity_endorsement", {})
        if celebrity.get("present"):
            html += f'                    <div class="warning-box">⚠️ Celebrity endorsement detected: {celebrity.get("details", "")}</div>\n'
        
        if brands.get("trademark_issues"):
            html += f'                    <div class="warning-box"><strong>Trademark Issues:</strong> {brands["trademark_issues"]}</div>\n'
        
        html += "                </div>\n            </div>\n"
    
    # Audio Copyright
    audio_copy = result.get("audio_copyright", {})
    if audio_copy:
        html += """
            <div class="section">
                <h2 class="section-title">🎵 Audio & Copyright</h2>
"""
        copyright_risk = audio_copy.get("copyright_risk_level", "low")
        risk_color_map = {"low": "#10b981", "medium": "#f59e0b", "high": "#ef4444"}
        risk_color_audio = risk_color_map.get(copyright_risk, "#6b7280")
        
        html += f"""
                <div class="info-card" style="border-left-color: {risk_color_audio};">
                    <h4>Copyright Risk: {copyright_risk.upper()}</h4>
                    <p><strong>Music Recognition:</strong> {audio_copy.get('music_recognition', 'Unknown')}</p>
                    {f'<p><strong>Copyrighted Music:</strong> {"Yes" if audio_copy.get("copyrighted_music_detected") else "No"}</p>' if audio_copy.get('copyrighted_music_detected') is not None else ''}
                    {f'<p><strong>Offensive Language:</strong> {"Yes" if audio_copy.get("offensive_language") else "No"}</p>' if audio_copy.get('offensive_language') is not None else ''}
                    {f'<div class="warning-box">{audio_copy.get("audio_issues")}</div>' if audio_copy.get('audio_issues') else ''}
                </div>
            </div>
"""
    
    # Technical Quality
    tech = result.get("technical_quality", {})
    if tech:
        html += """
            <div class="section">
                <h2 class="section-title">⚙️ Technical Quality</h2>
                <div class="info-grid">
"""
        checks = [
            ("resolution_adequate", "Resolution Adequate"),
            ("flashing_effects", "Flashing Effects (Epilepsy Risk)", True),  # True means inverted (False is good)
        ]
        
        for key, label, *invert in checks:
            is_inverted = invert[0] if invert else False
            value = tech.get(key)
            if value is not None:
                is_pass = (not value) if is_inverted else value
                html += f"""
                    <div class="check-item {'check-pass' if is_pass else 'check-fail'}">
                        <span class="check-icon">{'✅' if is_pass else '❌'}</span>
                        <span>{label}: {'No' if (is_inverted and not value) else ('Yes' if value else 'No')}</span>
                    </div>
"""
        
        if tech.get("text_overlay_percentage"):
            html += f"""
                    <div class="info-card">
                        <h4>Text Overlay</h4>
                        <p>{tech['text_overlay_percentage']} (Recommended: &lt;20%)</p>
                    </div>
"""
        
        if tech.get("viewing_comfort"):
            html += f"""
                    <div class="info-card">
                        <h4>Viewing Comfort</h4>
                        <p>{tech['viewing_comfort']}</p>
                    </div>
"""
        
        html += "                </div>\n            </div>\n"
    
    # Action Items
    action_items = result.get("action_items", {})
    if action_items:
        html += """
            <div class="section">
                <h2 class="section-title">✏️ Action Items</h2>
                <div class="action-items">
"""
        
        immediate = action_items.get("immediate_blockers", [])
        if immediate:
            html += "                    <h3 style=\"color: #dc2626;\">🚨 Immediate Blockers (Must Fix):</h3>\n                    <ul>\n"
            for item in immediate:
                html += f"                        <li>{item}</li>\n"
            html += "                    </ul>\n"
        
        recommended = action_items.get("recommended_improvements", [])
        if recommended:
            html += "                    <h3 style=\"color: #ea580c; margin-top: 15px;\">📈 Recommended Improvements:</h3>\n                    <ul>\n"
            for item in recommended:
                html += f"                        <li>{item}</li>\n"
            html += "                    </ul>\n"
        
        optional = action_items.get("optional_enhancements", [])
        if optional:
            html += "                    <h3 style=\"color: #059669; margin-top: 15px;\">💡 Optional Enhancements:</h3>\n                    <ul>\n"
            for item in optional:
                html += f"                        <li>{item}</li>\n"
            html += "                    </ul>\n"
        
        readiness = action_items.get("resubmission_readiness", "unknown")
        readiness_colors = {
            "готово до публікації": "#10b981",
            "потребує змін": "#f59e0b",
            "категорично не готово": "#ef4444"
        }
        readiness_color = readiness_colors.get(readiness, "#6b7280")
        
        html += f"""
                    <div style="margin-top: 20px; padding: 15px; background: {readiness_color}22; border-left: 4px solid {readiness_color}; border-radius: 6px;">
                        <strong>Resubmission Readiness:</strong> {readiness}
                    </div>
                </div>
            </div>
"""
    
    # Feedback & Recommendations
    feedback = result.get("feedback", {})
    if feedback:
        html += """
            <div class="section">
                <h2 class="section-title">💡 Feedback & Recommendations</h2>
"""
        
        main_issues = feedback.get("main_issues", [])
        if main_issues:
            html += "                <h3>Main Issues:</h3>\n"
            for issue in main_issues:
                impact = issue.get("impact", "unknown") if isinstance(issue, dict) else "unknown"
                must_fix = issue.get("must_fix", False) if isinstance(issue, dict) else False
                issue_text = issue.get("issue") if isinstance(issue, dict) else str(issue)
                badge_class = f"badge-{impact}" if impact != "unknown" else "badge-medium"
                
                html += f"""
                <div class="warning-box">
                    <span class="badge {badge_class}">{impact}</span>
                    {'<span class="badge badge-critical">MUST FIX</span>' if must_fix else ''}
                    <p>{issue_text}</p>
                </div>
"""
        
        required_changes = feedback.get("required_changes", [])
        if required_changes:
            html += "                <h3 style=\"margin-top: 20px;\">Required Changes:</h3>\n"
            for change in required_changes:
                if isinstance(change, dict):
                    priority = change.get("priority", "medium")
                    badge_class = f"badge-{priority}"
                    html += f"""
                <div class="info-card">
                    <span class="badge {badge_class}">{priority}</span>
                    <p><strong>Change:</strong> {change.get('change')}</p>
                    <p><strong>How to fix:</strong> {change.get('how_to_fix')}</p>
                </div>
"""
                else:
                    html += f"                    <div class=\"info-card\"><p>{change}</p></div>\n"
        
        recommendations = feedback.get("recommendations", [])
        if recommendations:
            html += "                <h3 style=\"margin-top: 20px;\">Recommendations:</h3>\n                <ul>\n"
            for rec in recommendations:
                html += f"                    <li>{rec}</li>\n"
            html += "                </ul>\n"
        
        alternatives = feedback.get("alternative_approaches", [])
        if alternatives:
            html += "                <h3 style=\"margin-top: 20px;\">Alternative Approaches:</h3>\n                <ul>\n"
            for alt in alternatives:
                html += f"                    <li>{alt}</li>\n"
            html += "                </ul>\n"
        
        best_practices = feedback.get("best_practices", [])
        if best_practices:
            html += """
                <div class="success-box" style="margin-top: 20px;">
                    <h3 style="color: #059669;">✅ Best Practices:</h3>
                    <ul>
"""
            for bp in best_practices:
                html += f"                        <li>{bp}</li>\n"
            html += "                    </ul>\n                </div>\n"
        
        html += "            </div>\n"
    
    # Overall Assessment
    html += f"""
            <div class="section">
                <h2 class="section-title">📝 Overall Assessment</h2>
                <p style="font-size: 16px; line-height: 1.8;">{compliance.get('overall_assessment', 'No assessment available')}</p>
            </div>
"""
    
    # Footer with JavaScript for collapsibles
    html += """
        </div>
    </div>
    
    <script>
        // Collapsible sections
        document.querySelectorAll('.collapsible').forEach(function(element) {
            element.addEventListener('click', function() {
                this.classList.toggle('active');
                var content = this.nextElementSibling;
                content.classList.toggle('active');
            });
        });
    </script>
</body>
</html>
"""
    
    return html
