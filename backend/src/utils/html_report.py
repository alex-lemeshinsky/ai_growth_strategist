"""
HTML report generator for competitor analysis results.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime


def generate_html_report(
    task_data: Dict[str, Any],
    creatives: List[Dict[str, Any]],
    aggregated: Optional[Dict[str, Any]] = None,
    aggregation_error: Optional[str] = None
) -> str:
    """
    Generate a beautiful HTML report from analysis results.
    
    Args:
        task_data: Task metadata (page_name, total_ads, etc.)
        creatives: List of analyzed creatives
        aggregated: Aggregated analysis results
        aggregation_error: Error message if aggregation failed
    
    Returns:
        HTML string ready for display
    """
    page_name = task_data.get("page_name", "Unknown")
    total_ads = task_data.get("total_ads", len(creatives))
    analyzed_count = len(creatives)
    
    html = f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Аналіз конкурента: {page_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
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
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #333;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }}
        
        .aggregated {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .insight-grid {{
            display: grid;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .insight-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .insight-item h3 {{
            font-size: 16px;
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        
        .insight-item h3::before {{
            content: "→";
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .insight-item ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .insight-item li {{
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .insight-item li:last-child {{
            border-bottom: none;
        }}
        
        .video-prompt {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .video-prompt h3 {{
            color: #856404;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        
        .video-prompt .prompt-text {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 15px;
        }}
        
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .copy-btn:hover {{
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }}
        
        .copy-btn:active {{
            transform: translateY(0);
        }}
        
        .copy-btn.copied {{
            background: #10b981;
        }}
        
        .creative-list {{
            display: grid;
            gap: 20px;
        }}
        
        .creative-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }}
        
        .creative-card .creative-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .creative-card .creative-id {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .creative-card .summary {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-style: italic;
            color: #333;
        }}
        
        .scores {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .score-badge {{
            background: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .score-bar {{
            width: 50px;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }}
        
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            color: #856404;
        }}
        
        .warning strong {{
            display: block;
            margin-bottom: 5px;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: 1fr;
            }}
            
            .scores {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Аналіз конкурента</h1>
            <div class="meta">
                <strong>{page_name}</strong><br>
                Проаналізовано: {datetime.now().strftime("%d.%m.%Y %H:%M")}
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="number">{total_ads}</div>
                <div class="label">Всього креативів</div>
            </div>
            <div class="stat-card">
                <div class="number">{analyzed_count}</div>
                <div class="label">Проаналізовано</div>
            </div>
            <div class="stat-card">
                <div class="number">{round(analyzed_count / total_ads * 100) if total_ads > 0 else 0}%</div>
                <div class="label">Успішність</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Aggregation error warning
    if aggregation_error:
        html += f"""
            <div class="warning">
                <strong>⚠️ Увага:</strong>
                Агрегований аналіз частково провалився: {aggregation_error[:200]}
            </div>
"""
    
    # Aggregated insights
    if aggregated:
        html += generate_aggregated_section(aggregated)
    
    # Individual creatives
    if creatives:
        html += generate_creatives_section(creatives)
    
    html += """
        </div>
    </div>
    
    <script>
        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ Скопійовано!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.classList.remove('copied');
                }, 2000);
            });
        }
    </script>
</body>
</html>
"""
    
    return html


def generate_aggregated_section(aggregated: Dict[str, Any]) -> str:
    """Generate aggregated insights section."""
    html = """
            <div class="section">
                <h2 class="section-title">🎯 Загальні інсайти</h2>
                <div class="aggregated">
"""
    
    # Core idea, theme, message
    if aggregated.get("core_idea") or aggregated.get("theme") or aggregated.get("message"):
        html += '<div class="insight-grid">'
        
        if aggregated.get("core_idea"):
            html += f"""
                <div class="insight-item">
                    <h3>Ключова ідея</h3>
                    <p>{aggregated["core_idea"]}</p>
                </div>
"""
        
        if aggregated.get("theme"):
            html += f"""
                <div class="insight-item">
                    <h3>Тема</h3>
                    <p>{aggregated["theme"]}</p>
                </div>
"""
        
        if aggregated.get("message"):
            html += f"""
                <div class="insight-item">
                    <h3>Основний меседж</h3>
                    <p>{aggregated["message"]}</p>
                </div>
"""
        
        html += '</div>'
    
    # Pain points, concepts, hooks
    html += '<div class="insight-grid" style="margin-top: 20px;">'
    
    if aggregated.get("pain_points"):
        html += """
                <div class="insight-item">
                    <h3>Болі аудиторії</h3>
                    <ul>
"""
        for pain in aggregated["pain_points"][:5]:
            html += f"                        <li>• {pain}</li>\n"
        html += "                    </ul>\n                </div>\n"
    
    if aggregated.get("concepts"):
        html += """
                <div class="insight-item">
                    <h3>Повторювані концепції</h3>
                    <ul>
"""
        for concept in aggregated["concepts"][:5]:
            html += f"                        <li>• {concept}</li>\n"
        html += "                    </ul>\n                </div>\n"
    
    if aggregated.get("hooks"):
        html += """
                <div class="insight-item">
                    <h3>Популярні хуки</h3>
                    <ul>
"""
        for hook in aggregated["hooks"][:5]:
            hook_text = hook if isinstance(hook, str) else hook.get("description", str(hook))
            html += f"                        <li>• {hook_text}</li>\n"
        html += "                    </ul>\n                </div>\n"
    
    html += '            </div>'
    
    # Recommendations
    if aggregated.get("recommendations"):
        html += f"""
                <div class="insight-item" style="margin-top: 20px;">
                    <h3>💡 Рекомендації</h3>
                    <p>{aggregated["recommendations"]}</p>
                </div>
"""
    
    # Video prompt
    if aggregated.get("video_prompt"):
        html += f"""
                <div class="video-prompt">
                    <h3>🎥 Промпт для генерації відео</h3>
                    <div class="prompt-text" id="videoPrompt">{aggregated["video_prompt"]}</div>
                    <button class="copy-btn" onclick="copyToClipboard('videoPrompt')">
                        📋 Копіювати промпт
                    </button>
                </div>
"""
    
    html += """
                </div>
            </div>
"""
    
    return html


def generate_creatives_section(creatives: List[Dict[str, Any]]) -> str:
    """Generate individual creatives section."""
    html = """
            <div class="section">
                <h2 class="section-title">🎬 Деталі креативів</h2>
                <div class="creative-list">
"""
    
    for i, creative in enumerate(creatives, 1):
        ad_id = creative.get("ad_archive_id", f"creative_{i}")
        page_name = creative.get("page_name", "Unknown")
        summary = creative.get("summary", "Опис недоступний")
        scores = creative.get("scores", {})
        
        html += f"""
                    <div class="creative-card">
                        <div class="creative-header">
                            <div>
                                <div class="creative-id">#{i} {ad_id}</div>
                                <small>{page_name}</small>
                            </div>
                        </div>
                        <div class="summary">{summary}</div>
"""
        
        if scores:
            html += '                        <div class="scores">\n'
            
            score_labels = {
                "hook_strength": "💥 Сила хука",
                "cta_clarity": "🎯 Чіткість CTA",
                "product_visibility": "👁️ Видимість продукту",
                "message_density": "📊 Щільність меседжів",
                "execution_quality": "✨ Якість виконання"
            }
            
            for key, label in score_labels.items():
                if key in scores:
                    score = scores[key]
                    html += f"""
                            <div class="score-badge">
                                {label}: <strong>{score:.2f}</strong>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {score * 100}%"></div>
                                </div>
                            </div>
"""
            
            html += '                        </div>\n'
        
        html += '                    </div>\n'
    
    html += """
                </div>
            </div>
"""
    
    return html
