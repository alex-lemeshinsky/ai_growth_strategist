# Frontend (Flutter)

Цей каталог містить Flutter-застосунок **AI Growth Strategist**. Нижче наведені інструкції з підготовки середовища, збірки та конфігурації `.env`.

## Передумови

- Flutter SDK (3.16+)
- Dart SDK (постачається з Flutter)
- Android Studio / Xcode / Visual Studio (для відповідних платформ)
- Node.js / npm не потрібні, якщо не збираєте web

Перевірити встановлений Flutter:

```bash
flutter doctor
```

## Підготовка `.env`

Створіть файл `frontend/.env` із такими змінними (приклад):

```dotenv
BASE_URL=https://your-api-host
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_secret
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/DB?retryWrites=true&w=majority
GENERATE_VIDEO_HOOK_URL=n8n-webhook-url
```

※ `BASE_URL` — базовий URL бекенду (FastAPI). Решта параметрів: OAuth Google Drive і MongoDB Atlas. Без коректних значень застосунок не підʼєднається до сервісів.

## Встановлення залежностей

```bash
flutter pub get
```

## Запуск у режимі розробки

### Android / iOS / macOS / Windows

```bash
flutter run
```

### Web (Chrome):

```bash
flutter run -d chrome
```

## Збірка

### Android

```bash
flutter build apk --release
```

### iOS (потрібен macOS + Xcode)

```bash
flutter build ios --release
```

### macOS

```bash
flutter build macos --release
```

### Web

```bash
flutter build web --release
```

## Структура `lib/`

- `app/` — MaterialApp, тема.
- `core/` — базові сервіси, утиліти, провайдери.
- `data/` — API клієнти, репозиторії, моделі JSON.
- `domain/` — доменні моделі/ентіті, сервіси.
- `presentation/` — екрани, стейт-контролери, віджети.

Додаткові інструкції з бекенду — у кореневому `README.md`.
