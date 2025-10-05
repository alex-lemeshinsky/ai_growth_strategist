# CreatorFlow AI — Pitch Deck (Text Version)

Команда: **Creators**  
Дата: 2025-10-05

1. Проблема
- Креативне відео під перформанс — найдорожча «пляшка» у воронці: бриф → референси → сценарії → озвучка/титри → монтаж → policy → переробки.
- Високий відсоток банів/перевірок → затримки та втрати бюджету.
- Масштабування варіацій потребує великої команди та часу.

2. Рішення: CreatorFlow AI
Єдиний end-to-end інструмент, що перетворює мінімальний бриф на пакет «готових до публікації» креативів під різні платформи. Починаємо з аналізу конкурентів, закінчуємо policy-safe креативами.

3. Як це працює (3 кроки)
- Step 1: Pattern Mining з реальних кейсів
  - Забираємо приклади з відкритих бібліотек (Meta Ad Library тощо)
  - Розбираємо відео на елементи: hook, стиль/темп/кольори, текст на екрані, продукт/цінність, CTA, messaging, аудіо, емоційна дуга
  - Будуємо базу патернів як фундамент для генерації
- Step 2: Генератор варіацій (MVP)
  - **Chat MVP Pro**: Інтерактивний збір брифу через conversational UI
    - Розумний діалог із Step-1 патернами як основою для пропозицій
    - Адаптивні питання на базі completeness score + missing fields detection
    - Інтеграція patterns-based suggestions (реальні приклади з аналізованих оголошень)
    - Policy hints під час збору (попереджаємо ризики на етапі брифу)
    - Платформені пресети (Facebook, TikTok, Instagram) автоматично налаштовують формат/тривалість
  - **Generation Pipeline**: Бриф → готове відео
    - Сценарії (shot list + VO + on-screen text + CTA) на основі зібраного брифу
    - Генерація VO (TTS), сабів (SRT), складання відео (ffmpeg) із завантажених ассетів
    - Автоматична адаптація під формат платформи (aspect ratio, duration, CTA styles)
    - Експорт у хмару, лінки на перегляд/завантаження
- Step 3: Policy Checker + Smart Recommendations
  - Автоматична перевірка на ризики (health claims, бренди/логотипи, музика, знаменитості, чутливі теми, NSFW, deceptive practices)
  - Детальні рекомендації та action items для кожного виявленого ризику
  - Приклади безпечних формулювань та пояснення порушень

4. Чому зараз
- Зрілість мультимодальних моделей (LLM + vision/audio)
- Доступні джерела референсів (Facebook Ad Library, TikTok Creative Center)
- Потреба ринку у швидкому, безпечному масштабуванні контенту

5. Бізнес-цінність
- Швидше: time-to-first-creative з днів → до годин/хвилин
- Дешевше: cost-per-variation ↓ 50–80%
- Безпечніше: менше банів завдяки preflight + Fix-it
- Масштабніше: 100+ варіацій/тиждень без росту команди

6. Унікальні переваги
- Патерни з реальних оголошень, не «фантазії» моделі
- Deep-analysis: психологічні тригери, емоційна дуга, гіпотези для A/B
- Comprehensive policy: детальні категорії + actionable action items
- Fix-it ланцюг: від ризику → до переписаного VO/сабів → до re-render
- Платформені пресети (формати, шрифти, CTA) для кращого відповідника

7. Поточний статус (backend)
- **Step 1: ГОТОВО ✅** — референс-видобуток, аналіз, агрегація, HTML-звіти
- **Step 2: MVP ГОТОВО ✅** — Chat MVP Pro повністю реалізований
  - Conversational UI з history, session management, completeness tracking
  - Patterns integration (пропозиції з реальних оголошень)
  - Policy hints у реальному часі
  - Платформені пресети
  - Generation pipeline структура готова (залишається тільки ffmpeg integration)
- **Step 3: ГОТОВО ✅** — policy checker + розширений HTML, action items, readiness
- **Infrastructure: ГОТОВО ✅** — документація, тести, стрімінг відео, асинхронні таски, MongoDB
- **Наступний крок**: Video Generation Engine (TTS + ffmpeg pipeline) + Global Patterns DB + Fix-it automation

8. Демо-флоу (API)
**Step 1: Pattern Mining**
- POST /api/v1/parse-ads?auto_analyze=true → отримуємо task_id
- GET /api/v1/report/task/{task_id} → HTML патернів/інсайтів

**Step 2: Chat MVP Pro (Готово!)**
- POST /api/v1/chat-mvp/session → створюємо нову сесію чату
- POST /api/v1/chat-mvp/message → надсилаємо повідомлення, отримуємо відповідь + suggestions
- GET /api/v1/chat-mvp/sessions → історія всіх сесій
- GET /static/chat_pro.html → повноцінний UI для тестування
- POST /api/v1/chat-mvp/submit → відправляємо готовий бриф на генерацію

**Step 3: Policy Check**
- POST /api/v2/policy/check → task_id для policy-перевірки
- GET /api/v1/report/policy/{task_id} → policy HTML з ризиками й фіксами

**Майбутнє:**
- POST /api/v1/generate → пакет варіацій + лінки (S3)

9. Порівняння з ринком (орієнтири)
- Референси: TikTok Creative Center, Meta Ad Library
- Генератори: AdCreative.ai, Pencil (ми додаємо policy + патерни з реальних відео)
- Відео-ген: Runway, Pika, Luma (інтегруємо як модулі для ассетів/ефектів)

10. Go-To-Market
- Ціль: performance-команди, агентства, DTC бренди
- Ціноутворення: seat + usage (рендери/перевірки), enterprise add-ons
- Канали: партнери-агентства, ком’юніті перформанс-маркетингу, інтеграції

11. Роадмап 2–4 тижні (оновлено)
**ЗАВЕРШЕНО ✅:**
- ✅ Step 1: Pattern Mining (HTML reports, insights extraction)
- ✅ Step 2: Chat MVP Pro (conversational brief collection)
- ✅ Step 3: Policy Checker (risk detection + action items)
- ✅ Infrastructure: FastAPI, MongoDB, async tasks, streaming

**НАСТУПНІ 2–4 ТИЖНІ:**
- **Тиждень 1**: Video Generation Engine
  - TTS integration (OpenAI/ElevenLabs/Google)
  - FFmpeg pipeline (складання shot list + VO + саби + ассети)
  - S3 upload + CDN лінки
- **Тиждень 2**: Global Patterns DB
  - Таксономія патернів, семантичний пошук
  - Крос-кейсовий аналіз і рекомендації
- **Тиждень 3**: Policy Fix-it Automation
  - Автоматичний перепис VO/сабів на основі policy warnings
  - Re-render pipeline з оновленими ассетами
- **Тиждень 4**: Advanced Features
  - Предиктивні скоринги (CTR/CVR predictions)
  - A/B варіації генерація
  - Enhanced UI/UX improvements

12. KPI успіху
- First creative lead time, cost/variation, pass rate без банів, кількість варіацій/тиждень

13. Запит (для пітчу/хакатону)
- Доступ до тестових ассетів і прикладів
- Інфраструктура для зберігання (S3/GCS) і рендер-черги
- Партнер для пілоту (агентство/бренд) на 2–4 тижні

14. Висновок
Замкнений процес «від брифу до безпечного креативу» економить тижні, бюджет і нерви. Патерни з реальних оголошень + генерація + policy Fix-it = стабільний конвеєр перформанс-креативів під різні платформи.