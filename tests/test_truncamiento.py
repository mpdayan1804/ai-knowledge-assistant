"""Modelos de razonamiento: contenido vacío + finish_reason='length' = truncamiento, no falla."""
import asyncio

import httpx
import pytest

from app.providers.base import LLMProviderError
from app.providers.openrouter import OpenRouterProvider

MSGS = [{"role": "user", "content": "hola"}]
KW = dict(temperature=0.3, top_p=1.0, max_tokens=50)


def _provider(handler):
    return OpenRouterProvider(
        api_key="k", default_model="m", transport=httpx.MockTransport(handler)
    )


def _resp(content, finish):
    return httpx.Response(
        200,
        json={"model": "x", "choices": [{"message": {"content": content}, "finish_reason": finish}]},
    )


def test_vacio_por_length_se_reporta_como_truncamiento():
    r = asyncio.run(_provider(lambda req: _resp(None, "length")).generate(MSGS, **KW))
    assert r.content == ""
    assert r.finish_reason == "length"


def test_vacio_sin_length_sigue_siendo_error():
    with pytest.raises(LLMProviderError):
        asyncio.run(_provider(lambda req: _resp(None, "stop")).generate(MSGS, **KW))


def test_respuesta_normal_conserva_finish_reason():
    r = asyncio.run(_provider(lambda req: _resp("Hola", "stop")).generate(MSGS, **KW))
    assert r.content == "Hola" and r.finish_reason == "stop"