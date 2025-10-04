"""
HTML templates for error and status pages.
"""
from datetime import datetime


def not_found_page(task_id: str, task_type: str = "task") -> str:
    """
    Generate HTML page for task not found.

    Args:
        task_id: The task ID that was not found
        task_type: Type of task (task, policy)
    """
    return f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Not Found</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }}

        .container {{
            text-align: center;
            max-width: 500px;
        }}

        .error-code {{
            font-size: 120px;
            font-weight: bold;
            opacity: 0.3;
            line-height: 1;
        }}

        h1 {{
            font-size: 32px;
            margin: 20px 0;
        }}

        p {{
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 30px;
        }}

        .task-id {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .home-link {{
            display: inline-block;
            padding: 12px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s;
        }}

        .home-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">404</div>
        <h1>🔍 Task Not Found</h1>
        <p>Задачу з таким ID не знайдено</p>
        <div class="task-id">{task_id}</div>
        <p style="font-size: 14px; opacity: 0.8;">
            Можливо, task_id неправильний або задачу було видалено
        </p>
        <a href="/" class="home-link">← Повернутись на головну</a>
    </div>
</body>
</html>
"""


def still_processing_page(task_id: str, status: str, task_type: str = "task") -> str:
    """
    Generate HTML page for task still processing with auto-refresh.

    Args:
        task_id: The task ID
        status: Current task status
        task_type: Type of task (task, policy)
    """
    status_messages = {
        "PENDING": "Задача в черзі на виконання",
        "PARSING": "Парсинг креативів...",
        "PARSED": "Креативи отримано, починаємо аналіз",
        "ANALYZING": "Аналіз креативів в процесі...",
        "CHECKING": "Перевірка відео на відповідність політикам..."
    }

    message = status_messages.get(status, "Обробка...")

    return f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <title>Processing...</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }}

        .container {{
            text-align: center;
            max-width: 600px;
        }}

        .spinner {{
            width: 80px;
            height: 80px;
            border: 8px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 30px;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 15px;
        }}

        .status {{
            font-size: 20px;
            opacity: 0.9;
            margin-bottom: 30px;
        }}

        .task-id {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .info {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 30px;
        }}

        .progress-bar {{
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.3);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 30px;
        }}

        .progress-fill {{
            height: 100%;
            background: white;
            animation: progress 2s ease-in-out infinite;
        }}

        @keyframes progress {{
            0% {{ width: 0%; }}
            50% {{ width: 70%; }}
            100% {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>⏳ Обробка задачі</h1>
        <div class="status">{message}</div>
        <div class="task-id">{task_id}</div>
        <div class="info">
            <p>Статус: <strong>{status}</strong></p>
            <p style="margin-top: 10px;">Сторінка автоматично оновиться через 5 секунд...</p>
        </div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
</body>
</html>
"""


def task_failed_page(task_id: str, error: str, task_type: str = "task") -> str:
    """
    Generate HTML page for failed task.

    Args:
        task_id: The task ID
        error: Error message
        task_type: Type of task (task, policy)
    """
    return f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Failed</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 20px;
        }}

        .container {{
            text-align: center;
            max-width: 600px;
        }}

        .error-icon {{
            font-size: 80px;
            margin-bottom: 20px;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 15px;
        }}

        .task-id {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
            margin-bottom: 30px;
        }}

        .error-box {{
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: left;
        }}

        .error-box h3 {{
            margin-bottom: 10px;
            font-size: 16px;
        }}

        .error-message {{
            font-family: monospace;
            font-size: 14px;
            opacity: 0.9;
            word-break: break-word;
        }}

        .actions {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .btn {{
            display: inline-block;
            padding: 12px 30px;
            background: white;
            color: #dc2626;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s;
        }}

        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}

        .btn-secondary {{
            background: transparent;
            border: 2px solid white;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">❌</div>
        <h1>Задача провалена</h1>
        <div class="task-id">{task_id}</div>

        <div class="error-box">
            <h3>Помилка:</h3>
            <div class="error-message">{error}</div>
        </div>

        <div class="actions">
            <a href="/" class="btn">← Повернутись на головну</a>
            <button onclick="location.reload()" class="btn btn-secondary">🔄 Оновити сторінку</button>
        </div>
    </div>
</body>
</html>
"""


def no_html_report_page(task_id: str, task_type: str = "task") -> str:
    """
    Generate HTML page when task is completed but HTML report is not yet generated.

    Args:
        task_id: The task ID
        task_type: Type of task (task, policy)
    """
    return f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3">
    <title>Generating Report...</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 20px;
        }}

        .container {{
            text-align: center;
            max-width: 600px;
        }}

        .icon {{
            font-size: 80px;
            margin-bottom: 20px;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 15px;
        }}

        .task-id {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .info {{
            font-size: 16px;
            opacity: 0.9;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📝</div>
        <h1>Генерація звіту</h1>
        <div class="task-id">{task_id}</div>
        <div class="info">
            <p>Задача завершена, але HTML звіт ще генерується</p>
            <p style="margin-top: 10px;">Оновлення через 3 секунди...</p>
        </div>
    </div>
</body>
</html>
"""
