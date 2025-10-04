import os
from apify_client import ApifyClient


started = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=106691191787847"
# --- 1. Налаштування ---
# Вставте ваш API ключ. Краще зберігати його як змінну середовища,
# але для простоти можна вписати прямо сюди.
APIFY_API_KEY = os.environ.get('APIFY_API_KEY')

# Назва актора, якого ми використовуємо
ACTOR_NAME = "curious_coder/facebook-ads-library-scraper"

# Параметри пошуку
SEARCH_TERMS = ["IKEA", "JYSK"]  # Можна шукати по кількох брендах одночасно
COUNTRY_CODE = "UA"  # Країна для пошуку (Україна)
RESULTS_LIMIT = 15  # Скільки рекламних оголошень отримати

# --- 2. Створення клієнта та налаштування вхідних даних ---
client = ApifyClient(APIFY_API_KEY)


run_input = {
    "urls": [
        {"url": started}
    ],
    "maxResults": RESULTS_LIMIT,
    "fetchAllDetails": True, # Залишаємо, щоб отримати креативи
}
# Вхідні дані для актора згідно з його документацією
# run_input = {
#     "searchTerms": SEARCH_TERMS,
#     "country": COUNTRY_CODE,
#     "maxResults": RESULTS_LIMIT,
#     "fetchAllDetails": True,  # Дуже важливий параметр для отримання креативів!
# }

print(f"🚀 Запускаю пошук реклами для: {', '.join(SEARCH_TERMS)} в країні {COUNTRY_CODE}...")

# --- 3. Запуск актора та очікування результатів ---
try:
    run = client.actor(ACTOR_NAME).call(run_input=run_input)
    print("✅ Актор завершив роботу. Отримую дані...")

    # --- 4. Обробка та вивід результатів ---
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Витягуємо дані, використовуючи .get() для безпеки
        print(item)
        page_name = item.get('pageName')
        ad_id = item.get('adId')

        # Основні дані креативу
        creative_body = item.get('body')
        creative_title = item.get('title')
        link_url = item.get('link')
        display_format = item.get('displayFormat')

        # Прямі посилання на медіа
        image_url = item.get('imageUrl')
        video_url = item.get('videoUrl')

        print("-" * 40)
        print(f"👨‍💼 Рекламодавець: {page_name}")
        print(f"🆔 ID Реклами: {ad_id}")
        print(f"🎨 Тип креативу: {display_format}")
        print(f"📝 Заголовок: {creative_title}")
        print(f"📖 Основний текст: {creative_body}")
        print(f"🔗 Посилання: {link_url}")
        print(f"🖼️ Зображення: {image_url}")
        print(f"🎬 Відео: {video_url}")

except Exception as e:
    print(f"Виникла помилка: {e}")