import json
import os
import requests  # Библиотека для скачивания файлов по URL

# Вставьте ваш JSON сюда. Для удобства он представлен как многострочный текст.
json_data_string = """
{
    "ad_archive_id": "1278360484326626",
    "page_id": "106691191787847",
    "snapshot": {
        "page_name": "SHUBA",
        "cards": [
            {
                "body": "3 головні ознаки, як вибрати справді якісний фарш \\nЧитай у статті SHUBA",
                "original_image_url": "https://scontent.fmvd4-1.fna.fbcdn.net/v/t39.35426-6/555948543_1318019886733283_8637400567824637972_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=YVvs9TIt5m0Q7kNvwHC4Hsm&_nc_oc=AdkiFfzrc0IPDkZvkvnSieP3o76gKVRzuh-E8k5AIqepH_CsXapIPpD0qNP21aTEH5PY_t42xLOYVderaBdkd5L2&_nc_zt=14&_nc_ht=scontent.fmvd4-1.fna&_nc_gid=rB9X9zuObhjqki4R9ouSNQ&oh=00_AfeeZL-WdeV45Zv3B_FrcOz3okEiwQf4zlmPdppnKEyoCA&oe=68E6D2DF"
            },
            {
                "body": "3 головні ознаки, як вибрати справді якісний фарш \\nЧитай у статті SHUBA",
                "original_image_url": "https://scontent.fmvd2-1.fna.fbcdn.net/v/t39.35426-6/557545003_1332829641888069_2333620788234190375_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=uj0h1ESORZgQ7kNvwGjsMm4&_nc_oc=AdkS3I92RbmWQvACHIt2POWGX9iZw3_rPo1TmhgrMd9bxIsTvFdnxCTStL_RwFlqNRiW7ezuGsVD9JCbd_F4EnS5&_nc_zt=14&_nc_ht=scontent.fmvd2-1.fna&_nc_gid=rB9X9zuObhjqki4R9ouSNQ&oh=00_AfcmJGLwBSdoGsu4GlWvgDZeHNGSP3En_7x5E6Wb4rrehQ&oe=68E6CF77"
            }
        ]
    }
}
"""

# Преобразуем текстовый JSON в словарь Python
data = json.loads(json_data_string)

# --- Основная логика скрипта ---

# 1. Определяем папку для сохранения креативов
output_folder = "creatives"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Папка '{output_folder}' создана.")

# 2. Извлекаем полезную информацию для названия файлов
page_name = data.get('snapshot', {}).get('page_name', 'unknown_page')
ad_id = data.get('ad_archive_id', 'unknown_ad')

# 3. Находим список "карточек" с креативами
# В вашем случае это "карусель" из нескольких изображений
creative_cards = data.get('snapshot', {}).get('cards', [])

if not creative_cards:
    print("В данных не найдены карточки с креативами.")
else:
    print(f"Найдено {len(creative_cards)} креативов. Начинаю скачивание...")
    # 4. Проходим по каждой карточке и скачиваем изображение
    for i, card in enumerate(creative_cards):
        image_url = card.get('original_image_url')

        if image_url:
            try:
                # Отправляем запрос на скачивание картинки
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()  # Проверяем, что запрос успешный (код 200)

                # Создаем уникальное имя файла
                # Например: creatives/SHUBA_1278360484326626_1.jpg
                file_name = f"{page_name}_{ad_id}_{i + 1}.jpg"
                file_path = os.path.join(output_folder, file_name)

                # Сохраняем картинку на диск
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                print(f"✅ Изображение {i + 1} сохранено как: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"❌ Ошибка при скачивании изображения {i + 1}: {e}")
        else:
            print(f"⚠️ В карточке {i + 1} не найдена ссылка на изображение.")