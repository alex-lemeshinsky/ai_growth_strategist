#!/usr/bin/env python3
"""
Example script demonstrating Facebook Ads Library functionality.
Shows how to use the clean architecture implementation to search for competitor ads.
"""

import asyncio
from config.container import container
from domain.models import AdActiveStatus
from domain.exceptions import FacebookDomainError, InvalidSearchQueryError


async def print_ad_details(ad, index: int):
    """Print detailed information about a single ad"""
    print(f"\n{'=' * 80}")
    print(f"📢 Реклама #{index}")
    print(f"{'=' * 80}")
    
    print(f"\n👤 Сторінка: {ad.page_name or 'N/A'}")
    print(f"🆔 ID: {ad.id}")
    
    # Primary text
    if ad.primary_text:
        text_preview = ad.primary_text[:200] + ('...' if len(ad.primary_text) > 200 else '')
        print(f"\n📝 Текст реклами:\n   {text_preview}")
    
    # Title
    if ad.primary_title:
        print(f"\n📌 Заголовок: {ad.primary_title}")
    
    # Description
    if ad.primary_description:
        desc_preview = ad.primary_description[:100] + ('...' if len(ad.primary_description) > 100 else '')
        print(f"📄 Опис: {desc_preview}")
    
    # Platforms
    if ad.publisher_platforms:
        print(f"\n🎯 Платформи: {ad.formatted_platforms}")
    
    # Dates
    if ad.ad_delivery_start_time:
        print(f"🗓️  Запущена: {ad.ad_delivery_start_time}")
    
    if ad.ad_delivery_stop_time:
        print(f"🛑 Зупинена: {ad.ad_delivery_stop_time}")
    else:
        print(f"✅ Статус: {'АКТИВНА' if ad.is_active else 'НЕАКТИВНА'}")
    
    # Metrics
    if ad.impressions:
        print(f"\n📊 Покази: {ad.impressions.formatted}")
    
    if ad.spend and ad.currency:
        print(f"💰 Витрати: {ad.spend.formatted} {ad.currency}")
    
    # Snapshot URL
    if ad.ad_snapshot_url:
        print(f"\n🔗 Переглянути креатив: {ad.ad_snapshot_url}")


async def search_single_keyword():
    """Example: Search for ads with a single keyword"""
    print("\n" + "="*80)
    print("🔍 ПОШУК ЗА ОДНИМ КЛЮЧОВИМ СЛОВОМ")
    print("="*80)
    
    search_service = container.get_ads_search_service()
    
    keyword = input("\n🔍 Введіть ключове слово (або Enter для 'fitness app'): ").strip()
    if not keyword:
        keyword = "fitness app"
    
    country = input("🌍 Код країни (або Enter для 'US'): ").strip().upper()
    if not country:
        country = "US"
    
    try:
        result = await search_service.search_ads(
            search_terms=keyword,
            country=country,
            limit=10,
            active_status=AdActiveStatus.ALL
        )
        
        print(f"\n✅ Знайдено {len(result.ads)} рекламних оголошень:")
        
        for index, ad in enumerate(result.ads, 1):
            await print_ad_details(ad, index)
        
        # Show summary
        summary = search_service.get_ads_summary(result)
        print(f"\n📊 ПІДСУМОК:")
        print(f"   Всього реклам: {summary['total_ads']}")
        print(f"   Активних: {summary['active_ads']}")
        print(f"   Платформи: {summary['platforms']}")
        print(f"   Топ сторінки: {summary['top_pages']}")
        print(f"   Є ще сторінки: {summary['has_more_pages']}")
        
    except InvalidSearchQueryError as e:
        print(f"❌ Помилка запиту: {e}")
    except FacebookDomainError as e:
        print(f"❌ Помилка Facebook API: {e}")


async def search_competitor_analysis():
    """Example: Competitor analysis with multiple keywords"""
    print("\n" + "="*80)
    print("🏢 АНАЛІЗ КОНКУРЕНТІВ")
    print("="*80)
    
    search_service = container.get_ads_search_service()
    
    # Example competitor keywords
    competitor_keywords = [
        "fitness tracker",
        "workout app", 
        "health monitoring",
        "exercise planner"
    ]
    
    print(f"\n🎯 Шукаємо рекламу за ключовими словами: {', '.join(competitor_keywords)}")
    
    try:
        results = await search_service.get_competitor_ads(
            competitor_keywords=competitor_keywords,
            country="US",
            limit_per_keyword=5
        )
        
        for i, (keyword, result) in enumerate(zip(competitor_keywords, results), 1):
            print(f"\n{'='*60}")
            print(f"📋 Результати для '{keyword}': {len(result.ads)} реклам")
            print(f"{'='*60}")
            
            for j, ad in enumerate(result.ads[:3], 1):  # Show only first 3
                print(f"\n📢 #{j} {ad.page_name or 'Невідома сторінка'}")
                if ad.primary_title:
                    print(f"   📌 {ad.primary_title}")
                if ad.publisher_platforms:
                    print(f"   🎯 {ad.formatted_platforms}")
        
    except FacebookDomainError as e:
        print(f"❌ Помилка: {e}")


async def search_by_page():
    """Example: Search ads from a specific Facebook page"""
    print("\n" + "="*80)
    print("📄 ПОШУК ЗА НАЗВОЮ СТОРІНКИ")
    print("="*80)
    
    search_service = container.get_ads_search_service()
    
    page_name = input("\n📄 Введіть назву Facebook сторінки: ").strip()
    if not page_name:
        print("❌ Назва сторінки не може бути пустою")
        return
    
    try:
        result = await search_service.search_by_page_name(
            page_name=page_name,
            country="US",
            limit=10
        )
        
        if result.ads:
            print(f"\n✅ Знайдено {len(result.ads)} реклам для сторінки '{page_name}':")
            
            for index, ad in enumerate(result.ads, 1):
                await print_ad_details(ad, index)
        else:
            print(f"😕 Не знайдено реклам для сторінки '{page_name}'")
        
    except FacebookDomainError as e:
        print(f"❌ Помилка: {e}")


async def platform_filtering_demo():
    """Example: Filtering ads by platform"""
    print("\n" + "="*80)
    print("🎯 ФІЛЬТРАЦІЯ ЗА ПЛАТФОРМАМИ")
    print("="*80)
    
    search_service = container.get_ads_search_service()
    
    try:
        # Search for some ads first
        result = await search_service.search_ads("mobile app", limit=10)
        
        if not result.ads:
            print("😕 Не знайдено реклам для демонстрації фільтрації")
            return
        
        print(f"\n📊 Всього знайдено {len(result.ads)} реклам")
        
        # Filter by Instagram only
        instagram_ads = search_service.filter_ads_by_platform(result.ads, ['instagram'])
        print(f"📷 Instagram тільки: {len(instagram_ads)} реклам")
        
        # Filter by Facebook only
        facebook_ads = search_service.filter_ads_by_platform(result.ads, ['facebook'])
        print(f"📘 Facebook тільки: {len(facebook_ads)} реклам")
        
        # Filter by both
        both_platforms = search_service.filter_ads_by_platform(result.ads, ['facebook', 'instagram'])
        print(f"📘📷 Facebook або Instagram: {len(both_platforms)} реклам")
        
    except FacebookDomainError as e:
        print(f"❌ Помилка: {e}")


async def main_menu():
    """Main interactive menu"""
    print("\n🚀 Facebook Ads Library - Чиста Архітектура")
    print("=" * 80)
    
    while True:
        print("\n📋 МЕНЮ:")
        print("1. 🔍 Пошук за ключовим словом")
        print("2. 🏢 Аналіз конкурентів")
        print("3. 📄 Пошук за назвою сторінки")
        print("4. 🎯 Демонстрація фільтрації платформ")
        print("5. 🚪 Вихід")
        
        choice = input("\nВиберіть опцію (1-5): ").strip()
        
        try:
            if choice == "1":
                await search_single_keyword()
            elif choice == "2":
                await search_competitor_analysis()
            elif choice == "3":
                await search_by_page()
            elif choice == "4":
                await platform_filtering_demo()
            elif choice == "5":
                print("\n👋 До побачення!")
                break
            else:
                print("❌ Невірний вибір. Спробуйте ще раз.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Програма перервана користувачем")
            break
        except Exception as e:
            print(f"\n❌ Неочікувана помилка: {e}")


async def main():
    """Main entry point"""
    try:
        # Initialize dependency injection container
        container.initialize()
        print("✅ Система ініціалізована успішно")
        
        # Test configuration
        config = container.get_config_service()
        try:
            config.get_facebook_app_id()
            config.get_facebook_app_secret()
            print("✅ Facebook API конфігурація знайдена")
        except FacebookDomainError as e:
            print(f"❌ Помилка конфігурації: {e}")
            print("💡 Переконайтесь, що FB_APP_ID і FB_APP_SECRET встановлені в .env файлі")
            return
        
        # Run main menu
        await main_menu()
        
    except KeyboardInterrupt:
        print("\n👋 Програма завершена")
    except Exception as e:
        print(f"\n❌ Критична помилка: {e}")
    finally:
        # Cleanup
        await container.close()
        print("🧹 Ресурси очищені")


if __name__ == "__main__":
    asyncio.run(main())