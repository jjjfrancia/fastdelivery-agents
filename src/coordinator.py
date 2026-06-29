"""Coordinador (Harness): clasifica la intención y rutea. No responde la consulta."""
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
INTENTS = ("pedidos", "menu", "reembolsos", "desconocido")

_KEYWORDS = {
    "pedidos": ("pedido", "donde esta", "dónde está", "seguimiento", "rastrear", "llega", "eta"),
    "reembolsos": ("reembolso", "devolu", "devuelvan", "mi dinero", "reintegro"),
    "menu": ("menu", "menú", "tienen", "precio", "cuesta", "plato", "pizza", "hamburguesa", "carta"),
}


def classify_keyword(question: str) -> str:
    """Clasificador offline por palabras clave (sin red). Orden: pedidos, reembolsos, menu."""
    q = (question or "").lower()
    # Orden importante: 'reembolsos' antes que 'pedidos' (un reembolso suele mencionar "pedido").
    for intent in ("reembolsos", "pedidos", "menu"):
        if any(k in q for k in _KEYWORDS[intent]):
            return intent
    return "desconocido"


def classify(question: str, client=None, model: str = "claude-sonnet-4-6") -> str:
    """Clasifica con el LLM si hay cliente; si no, usa el clasificador por palabras clave."""
    if client is None:
        return classify_keyword(question)
    system = (PROMPTS / "coordinator.txt").read_text(encoding="utf-8")
    msg = client.messages.create(
        model=model, max_tokens=10, system=system,
        messages=[{"role": "user", "content": question}],
    )
    label = msg.content[0].text.strip().lower()
    return label if label in INTENTS else "desconocido"
