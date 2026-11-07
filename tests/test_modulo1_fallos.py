"""Experimento 5: fallos simulados SIN consumo externo."""
import asyncio
 
import httpx
import pytest
from fastapi.testclient import TestClient
 
from app.dependencies import get_assistant_service
from app.main import app
from app.providers.base import LLMProviderError
from app.providers.fake import FakeLLMProvider
from app.providers.openrouter import OpenRouterProvider
from app.services.assistant_service import AssistantService
 
MSGS = [{"role": "user", "content": "hola"}]
KW = dict(temperature=0.3, top_p=1.0, max_tokens=50)
 
 
def _provider(handler) -> OpenRouterProvider:
    return OpenRouterProvider(
        api_key="CLAVE-SECRETA-123",
        default_model="modelo-x",
        transport=httpx.MockTransport(handler),
    )
 
 
def test_adaptador_timeout():
    def handler(request):
        raise httpx.ReadTimeout("simulado", request=request)
 
    with pytest.raises(LLMProviderError):
        asyncio.run(_provider(handler).generate(MSGS, **KW))
 
 
def test_adaptador_http_429():
    def handler(request):
        return httpx.Response(429, json={"error": "rate limit CLAVE-SECRETA-123"})
 
    with pytest.raises(LLMProviderError) as exc:
        asyncio.run(_provider(handler).generate(MSGS, **KW))
    assert "429" in str(exc.value)
    assert "CLAVE-SECRETA-123" not in str(exc.value)
 
 
def test_adaptador_json_sin_choices():
    def handler(request):
        return httpx.Response(200, json={"id": "x"})
 
    with pytest.raises(LLMProviderError):
        asyncio.run(_provider(handler).generate(MSGS, **KW))
 
 
def test_router_devuelve_502_sin_filtrar_secretos():
    fake = FakeLLMProvider(fail_with="boom CLAVE-SECRETA-123 cuerpo-sensible")
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(fake)
    try:
        client = TestClient(app)
        r = client.post("/api/v1/chat", json={"question": "¿Qué es un LLM?"})
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 502
    assert "CLAVE-SECRETA-123" not in r.text
    assert "cuerpo-sensible" not in r.text
 
 
def test_422_no_invoca_al_proveedor():
    fake = FakeLLMProvider()
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(fake)
    try:
        client = TestClient(app)
        r1 = client.post("/api/v1/chat", json={"question": "A"})
        r2 = client.post("/api/v1/chat", json={"question": "Hola válida", "temperature": -1})
    finally:
        app.dependency_overrides.clear()
    assert r1.status_code == 422 and r2.status_code == 422
    assert fake.calls == []          # el LLM nunca se ejecutó
 
 
def test_servicio_agrega_system_y_user():
    fake = FakeLLMProvider()
    service = AssistantService(fake)
    asyncio.run(service.ask("¿Qué es un LLM?", **KW))
    roles = [m["role"] for m in fake.calls[0]["messages"]]
    assert roles == ["system", "user"]
    