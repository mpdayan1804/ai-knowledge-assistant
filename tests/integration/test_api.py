"""Pruebas de integración de la API (T-02 a T-05 + validaciones 422).
 
Las pruebas de /chat usan FakeLLMProvider: no llaman a OpenRouter.
"""
import pytest
from fastapi.testclient import TestClient
 
from app.dependencies import get_assistant_service
from app.main import app
from app.providers.fake import FakeLLMProvider
from app.services.assistant_service import AssistantService
 
 
@pytest.fixture
def client():
    fake = FakeLLMProvider(answer="Respuesta de prueba")
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(fake)
    yield TestClient(app)
    app.dependency_overrides.clear()
 
 
class TestHealthEndpoint:
    def test_health_check_returns_200(self, client):
        """T-02: GET /health retorna 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
 
 
class TestChatEndpoint:
    def test_chat_with_valid_question_returns_200(self, client):
        """T-03: pregunta válida -> 200 (con proveedor falso)."""
        response = client.post("/api/v1/chat", json={"question": "¿Qué es FastAPI?"})
        assert response.status_code == 200
        body = response.json()
        assert body["answer"] == "Respuesta de prueba"
        assert body["provider"] == "fake"
 
    def test_chat_with_too_short_question_returns_422(self, client):
        """T-04: pregunta muy corta -> 422."""
        response = client.post("/api/v1/chat", json={"question": "Hi"})
        assert response.status_code == 422
 
    def test_chat_with_empty_question_returns_422(self, client):
        response = client.post("/api/v1/chat", json={"question": ""})
        assert response.status_code == 422
 
    def test_chat_with_whitespace_only_returns_422(self, client):
        response = client.post("/api/v1/chat", json={"question": "   "})
        assert response.status_code == 422
 
    def test_chat_with_too_long_question_returns_422(self, client):
        response = client.post("/api/v1/chat", json={"question": "a" * 2001})
        assert response.status_code == 422
 
    def test_chat_without_question_field_returns_422(self, client):
        response = client.post("/api/v1/chat", json={"wrong_field": "test"})
        assert response.status_code == 422
 
    def test_chat_with_negative_temperature_returns_422(self, client):
        """Nuevo (Módulo I): temperature=-1 es rechazada por Pydantic."""
        response = client.post(
            "/api/v1/chat", json={"question": "Pregunta válida", "temperature": -1}
        )
        assert response.status_code == 422
 
 
class TestInfoEndpoint:
    def test_info_returns_200_and_llm_disabled(self, client):
        """T-05: GET /api/v1/info -> 200 y llm_enabled = false."""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        assert response.json()["llm_enabled"] is False
 
 
class TestRootEndpoint:
    def test_root_returns_basic_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()