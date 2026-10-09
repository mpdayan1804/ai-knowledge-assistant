"""
Unit tests for BootstrapService.

Tests the service layer independently of HTTP endpoints.
"""

import pytest
from app.services.bootstrap_service import BootstrapService


class TestBootstrapService:
    """Test suite for BootstrapService."""

    def test_service_initialization(self):
        """Test that the service initializes correctly."""
        service = BootstrapService()
        assert service.provider == "bootstrap-local"

    def test_process_question_with_fastapi_keyword(self):
        """
        T-01: Unit test del servicio.
        The service should correctly respond to a known question.
        """
        service = BootstrapService()
        response = service.process_question("¿Qué es FastAPI?")

        assert response.answer is not None
        assert len(response.answer) > 0
        assert response.provider == "bootstrap-local"
        assert "FastAPI" in response.answer

    def test_process_question_with_python_keyword(self):
        """Test service responds correctly to Python-related questions."""
        service = BootstrapService()
        response = service.process_question("¿Qué es Python?")

        assert response.answer is not None
        assert len(response.answer) > 0
        assert response.provider == "bootstrap-local"
        assert "Python" in response.answer

    def test_process_question_with_api_keyword(self):
        """Test service responds correctly to API-related questions."""
        service = BootstrapService()
        response = service.process_question("¿Qué es una API?")

        assert response.answer is not None
        assert len(response.answer) > 0
        assert response.provider == "bootstrap-local"
        assert "API" in response.answer

    def test_process_question_with_generic_question(self):
        """Test service responds to generic questions with bootstrap message."""
        service = BootstrapService()
        question = "¿Cómo funciona el clima?"
        response = service.process_question(question)

        assert response.answer is not None
        assert len(response.answer) > 0
        assert response.provider == "bootstrap-local"
        assert question in response.answer
        assert "bootstrap" in response.answer.lower()

    def test_process_question_empty_string(self):
        """Test service handles empty string gracefully."""
        service = BootstrapService()
        response = service.process_question("")

        assert response.answer is not None
        assert response.provider == "bootstrap-local"

    def test_process_question_whitespace_only(self):
        """Test service handles whitespace-only questions."""
        service = BootstrapService()
        response = service.process_question("   ")

        assert response.answer is not None
        assert response.provider == "bootstrap-local"
