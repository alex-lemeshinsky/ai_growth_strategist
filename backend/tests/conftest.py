"""
Pytest configuration and fixtures.
"""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_env_vars(monkeypatch):
    """Set up sample environment variables for testing"""
    monkeypatch.setenv('FB_APP_ID', 'test_app_id')
    monkeypatch.setenv('FB_APP_SECRET', 'test_app_secret')
    monkeypatch.setenv('FB_API_VERSION', 'v21.0')
    monkeypatch.setenv('FB_BASE_URL', 'https://graph.facebook.com')
    monkeypatch.setenv('REQUEST_TIMEOUT', '30')