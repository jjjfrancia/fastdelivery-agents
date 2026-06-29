"""ZONA ② — Prueba funcional (e2e) con el LLM real. Se omite si no hay API key."""
import os
import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="requiere ANTHROPIC_API_KEY (clasificación con LLM)",
)


def test_coordinator_clasifica_con_llm():
    import anthropic
    from src import coordinator
    client = anthropic.Anthropic()
    model = os.environ.get("MODEL", "claude-sonnet-4-6")
    assert coordinator.classify("¿dónde está mi pedido A1001?", client=client, model=model) == "pedidos"
