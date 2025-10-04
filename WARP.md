# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

The AI Growth Strategist is a full-stack application built for the Vibecoding hackathon. It consists of:
- **Backend**: Python-based service using Facebook Ads Library API for competitor advertising analysis
- **Frontend**: Flutter mobile application for cross-platform deployment

## Development Commands

### Backend (Python)
```bash
# Navigate to backend directory
cd backend

# Install dependencies using uv (Python package manager)
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run the main application
python main.py

# Run Facebook Ads Library script
python fb.py
```

### Frontend (Flutter)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
flutter pub get

# Run the app in development mode
flutter run

# Run tests
flutter test

# Analyze code for linting issues
flutter analyze

# Format code
dart format .

# Build for production
flutter build apk         # Android
flutter build ios         # iOS
flutter build web         # Web
```

## Architecture

### Backend Structure
- **main.py**: Entry point for the backend service (currently minimal)
- **fb.py**: Facebook Ads Library integration with comprehensive ad analysis features
- **config.py**: Configuration management (empty, ready for expansion)
- **pyproject.toml**: Python project configuration using uv package manager

The backend is designed around Facebook advertising analysis, with the `FBAdsLibrary` class providing:
- Ad search functionality across countries
- Detailed ad information extraction (creative content, metrics, platforms)
- JSON export capabilities
- Interactive CLI interface

### Frontend Structure
- Standard Flutter application structure
- **lib/main.dart**: Entry point with basic Material Design counter app
- **test/widget_test.dart**: Widget testing setup
- Uses Flutter SDK 3.9.2+ with Material Design components

### Environment Configuration
The backend requires Facebook API credentials stored in `.env`:
- `FB_APP_ID`: Facebook App ID
- `FB_APP_SECRET`: Facebook App Secret

These are combined to create an access token for the Facebook Ads Library API.

## Key Integration Points

### Facebook Ads Library API
The core backend functionality centers around the Facebook Ads Library v21.0 API:
- Search ads by keywords and country codes
- Extract comprehensive ad metadata including creative content, spend ranges, and platform targeting
- Support for pagination and result filtering
- Localized output in Ukrainian with emoji-enhanced formatting

### Data Flow
1. Backend receives search parameters (keyword, country, limit)
2. Queries Facebook Ads Library API with structured field requests
3. Processes and formats ad data with detailed metrics
4. Optionally exports results to timestamped JSON files
5. Frontend (when implemented) will consume this data for mobile presentation

## Development Notes

### Python Backend
- Uses modern Python 3.12+ with `uv` for fast dependency management
- Implements comprehensive error handling for API requests
- Provides rich console output with Unicode formatting
- Ready for expansion with additional AI/ML analysis features

### Flutter Frontend
- Standard Flutter project setup with Material Design
- Configured for cross-platform deployment
- Uses recommended linting rules via `flutter_lints`
- Ready for integration with backend API services

### Future Development Considerations
- Backend currently outputs to console/JSON but could easily be converted to a REST API
- Frontend has basic structure ready for custom UI implementation
- Environment variables pattern established for secure credential management
- Project structure supports microservices architecture if needed