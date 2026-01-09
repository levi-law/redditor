"""Pytest configuration and shared fixtures for Redditor tests."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def mock_reddit_client():
    """Mock Reddit client for testing without actual API calls."""
    client = MagicMock()
    client.authenticated = True
    client.username = "test_user"
    return client


@pytest.fixture
def sample_post():
    """Sample Reddit post data for testing."""
    return {
        "id": "test123",
        "title": "Test Post Title",
        "selftext": "This is the body of the test post.",
        "author": "test_author",
        "subreddit": "test_subreddit",
        "score": 100,
        "num_comments": 25,
        "created_utc": 1736380800.0,  # 2026-01-09
    }


@pytest.fixture
def sample_comment():
    """Sample Reddit comment data for testing."""
    return {
        "id": "comment123",
        "body": "This is a test comment.",
        "author": "comment_author",
        "score": 50,
        "created_utc": 1736380800.0,
    }


@pytest.fixture
def sample_pipeline_config():
    """Sample pipeline configuration for testing."""
    return {
        "name": "test_pipeline",
        "schedule": "*/5 * * * *",  # Every 5 minutes
        "enabled": True,
        "params": {
            "subreddit": "test",
            "limit": 10,
        },
    }
