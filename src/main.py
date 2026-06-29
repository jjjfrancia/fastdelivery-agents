"""CLI del asistente FastDelivery: clasifica, rutea y responde.

Uso:  python -m src.main "¿dónde está mi pedido A1001?"
Sin ANTHROPIC_API_KEY funciona igual (clasificador por palabras clave + plantillas).
"""
import os
import sys
from . import coordinator, agents


def get_client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
        return anthropic.Anthropic()
    except Exception:
        return None


def answer(question: str) -> str:
    client = get_client()
    model = os.environ.get("MODEL", "claude-sonnet-4-6")
    intent = coordinator.classify(question, client=client, model=model)
    if intent == "desconocido":
        return ("No estoy seguro de cómo ayudarte con eso. Puedo ver el estado de tu pedido, "
                "el menú o un reembolso.")
    return agents.HANDLERS[intent](question, client=client, model=model)


def main():
    q = " ".join(sys.argv[1:]).strip()
    if not q:
        print('Uso: python -m src.main "tu pregunta"')
        return
    print(answer(q))


if __name__ == "__main__":
    main()
