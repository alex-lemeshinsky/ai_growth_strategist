# Facebook Ads Library Backend

Чиста архітектура для роботи з Facebook Ads Library API, розроблена для аналізу реклами конкурентів.

## 🏗️ Архітектура

Проект побудований за принципами чистої архітектури з dependency injection:

```
src/
├── domain/          # Бізнес логіка, інтерфейси, моделі
├── infrastructure/  # Реалізація Facebook API клієнта
├── application/     # Use cases і сервіси
├── config/          # DI контейнер і конфігурація
└── main_example.py  # Приклад використання

tests/               # Unit тести з моками
```

### Основні принципи

- **Dependency Injection**: Всі залежності ін'єктуються через інтерфейси
- **Легке тестування**: Всі компоненти легко мокаються
- **Модульність**: Кожен шар має чітку відповідальність
- **Масштабованість**: Легко додавати новий функціонал

## 🚀 Швидкий старт

### 1. Встановлення залежностей

```bash
# Основні залежності
uv sync

# Додатково для тестування
uv sync --extra test

# Активація віртуального середовища
source .venv/bin/activate
```

### 2. Налаштування середовища

Створіть файл `.env`:

```bash
FB_APP_ID=your_facebook_app_id
FB_APP_SECRET=your_facebook_app_secret
FB_API_VERSION=v21.0
FB_BASE_URL=https://graph.facebook.com
REQUEST_TIMEOUT=30
```

### 3. Запуск прикладу

```bash
python src/main_example.py
```

## 📋 Основні функції

### Пошук реклами
```python
from src.config.container import container

# Ініціалізація
container.initialize()
service = container.get_ads_search_service()

# Пошук реклами
result = await service.search_ads(
    search_terms="fitness app",
    country="US", 
    limit=10
)

print(f"Знайдено {len(result.ads)} реклам")
```

### Аналіз конкурентів
```python
# Пошук за кількома ключовими словами
keywords = ["fitness tracker", "workout app", "health monitoring"]
results = await service.get_competitor_ads(
    competitor_keywords=keywords,
    country="US",
    limit_per_keyword=5
)

for keyword, result in zip(keywords, results):
    print(f"{keyword}: {len(result.ads)} реклам")
```

### Фільтрація за платформами
```python
# Фільтрування реклами за платформами
instagram_ads = service.filter_ads_by_platform(
    ads=result.ads, 
    platforms=["instagram"]
)

facebook_ads = service.filter_ads_by_platform(
    ads=result.ads, 
    platforms=["facebook"]
)
```

## 🧪 Тестування

### Запуск тестів

```bash
# Всі тести
pytest

# З покриттям
pytest --cov=src

# Конкретний тест файл
pytest tests/test_domain_models.py

# Verbose режим
pytest -v
```

### Структура тестів

- `test_domain_models.py` - Тести бізнес моделей
- `test_ads_search_service.py` - Тести application layer з моками
- `test_facebook_ads_repository.py` - Тести infrastructure layer з моками
- `conftest.py` - Конфігурація pytest та фікстури

## 🔧 API Documentation

### Domain Models

#### FacebookAd
Основна модель реклами з Facebook Ads Library:

```python
@dataclass
class FacebookAd:
    id: str
    page_name: Optional[str]
    ad_creative_bodies: List[str]
    ad_creative_link_titles: List[str]
    publisher_platforms: List[PublisherPlatform]
    impressions: Optional[AdImpressionRange]
    spend: Optional[AdSpendRange]
    # ... інші поля
    
    @property
    def is_active(self) -> bool
    
    @property
    def primary_text(self) -> str
    
    @property 
    def formatted_platforms(self) -> str
```

#### AdSearchQuery
Параметри пошуку:

```python
@dataclass
class AdSearchQuery:
    search_terms: str
    ad_reached_countries: str = "US"
    limit: int = 20
    ad_active_status: AdActiveStatus = AdActiveStatus.ALL
```

### Services

#### AdsSearchService
Основний сервіс для роботи з рекламою:

```python
class AdsSearchService:
    async def search_ads(self, search_terms: str, country: str = "US", limit: int = 20) -> AdSearchResult
    
    async def get_competitor_ads(self, competitor_keywords: List[str], country: str = "US") -> List[AdSearchResult]
    
    async def search_by_page_name(self, page_name: str, country: str = "US") -> AdSearchResult
    
    def filter_ads_by_platform(self, ads: List[FacebookAd], platforms: List[str]) -> List[FacebookAd]
    
    def get_ads_summary(self, search_result: AdSearchResult) -> dict
```

## 🎯 Приклади використання

### 1. Базовий пошук
```python
import asyncio
from src.config.container import container

async def basic_search():
    container.initialize()
    service = container.get_ads_search_service()
    
    result = await service.search_ads("mobile games")
    
    for ad in result.ads:
        print(f"📢 {ad.page_name}")
        print(f"📝 {ad.primary_text[:100]}...")
        print(f"🎯 {ad.formatted_platforms}")
        print("-" * 40)
    
    await container.close()

asyncio.run(basic_search())
```

### 2. Аналіз конкурентів з статистикою
```python
async def competitor_analysis():
    container.initialize()
    service = container.get_ads_search_service()
    
    # Ключові слова конкурентів
    keywords = ["food delivery", "meal kit", "grocery delivery"]
    
    results = await service.get_competitor_ads(keywords, limit_per_keyword=20)
    
    for keyword, result in zip(keywords, results):
        summary = service.get_ads_summary(result)
        
        print(f"\n📊 Аналіз для '{keyword}':")
        print(f"   Всього реклам: {summary['total_ads']}")
        print(f"   Активних: {summary['active_ads']}")
        print(f"   Платформи: {summary['platforms']}")
        print(f"   Топ сторінки: {list(summary['top_pages'].keys())[:3]}")
    
    await container.close()
```

### 3. Пошук з фільтрацією
```python
async def filtered_search():
    container.initialize()
    service = container.get_ads_search_service()
    
    # Пошук всіх реклам
    result = await service.search_ads("fitness", limit=50)
    
    # Фільтрація тільки Instagram реклами
    instagram_ads = service.filter_ads_by_platform(
        result.ads, 
        ["instagram"]
    )
    
    print(f"📷 Instagram реклам: {len(instagram_ads)}")
    
    # Показати тільки активні реклами
    active_ads = [ad for ad in instagram_ads if ad.is_active]
    
    print(f"✅ Активних Instagram реклам: {len(active_ads)}")
    
    await container.close()
```

## 🔒 Безпека

- API ключі зберігаються у змінних середовища
- Ніколи не комітьте `.env` файли
- Використовуйте app access tokens (не user tokens)

## 🚧 Розвиток

### Додавання нового функціоналу

1. **Domain Layer**: Додайте нові моделі/інтерфейси
2. **Infrastructure Layer**: Реалізуйте інтерфейси
3. **Application Layer**: Створіть use cases
4. **Tests**: Напишіть тести з моками
5. **DI Container**: Зареєструйте залежності

### Архітектурні принципи

- Domain layer не знає про infrastructure
- Infrastructure реалізує domain інтерфейси
- Application orchestrates domain і infrastructure
- Всі залежності ін'єктуються через конструктор

## 📝 Ліцензія

MIT License

## 🤝 Внесок

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request