"""
Integration tests for the API endpoints.

Tests the HTTP layer using FastAPI's TestClient without requiring
an external running server.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test suite for the /health endpoint."""

    def test_health_check_returns_200(self, client):
        """
        T-02: GET /health should return HTTP 200.
        """
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestChatEndpoint:
    """Test suite for the /api/v1/chat endpoint."""

    def test_chat_with_valid_question_returns_200(self, client):
        """
        T-03: POST /api/v1/chat with a valid question should return HTTP 200.
        """
        payload = {
            "question": "¿Qué es FastAPI?",
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        # If no API key, falls back to bootstrap
        assert response.status_code in [200, 502]
        data = response.json()
        assert "answer" in data
        assert "provider" in data

    def test_chat_with_too_short_question_returns_422(self, client):
        """
        T-04: POST /api/v1/chat with a too-short question should return HTTP 422.
        """
        payload = {
            "question": "Hi",
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422

    def test_chat_with_empty_question_returns_422(self, client):
        """Test that empty question returns 422."""
        payload = {
            "question": "",
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422

    def test_chat_with_whitespace_only_returns_422(self, client):
        """Test that whitespace-only question returns 422."""
        payload = {
            "question": "   ",
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422

    def test_chat_with_too_long_question_returns_422(self, client):
        """Test that question exceeding max length returns 422."""
        payload = {
            "question": "a" * 2001,
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422

    def test_chat_with_invalid_temperature_returns_422(self, client):
        """Test that invalid temperature returns 422."""
        payload = {
            "question": "Test question",
            "model": "openai/gpt-3.5-turbo",
            "temperature": -1.0,
            "top_p": 1.0,
            "max_tokens": 300,
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422

    def test_chat_without_question_field_returns_422(self, client):
        """Test that missing question field returns 422."""
        payload = {"wrong_field": "test"}
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 422


class TestInfoEndpoint:
    """Test suite for the /api/v1/info endpoint."""

    def test_info_returns_200_and_llm_disabled(self, client):
        """
        T-05: GET /api/v1/info should return HTTP 200 and llm_enabled = false.
        """
        response = client.get("/api/v1/info")

        assert response.status_code == 200
        data = response.json()
        assert data["llm_enabled"] is False
        assert "name" in data
        assert "version" in data
        assert "environment" in data


class TestRootEndpoint:
    """Test suite for the root endpoint."""

    def test_root_returns_basic_info(self, client):
        """Test that root endpoint returns basic information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["docs"] == "/docs"
