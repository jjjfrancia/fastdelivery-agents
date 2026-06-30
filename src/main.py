"""CLI del asistente FastDelivery: clasifica, rutea y responde.

Uso:  python -m src.main "¿dónde está mi pedido A1001?"
Sin ANTHROPIC_API_KEY funciona igual (clasificador por palabras clave + plantillas).
"""
import os
import sys
from pathlib import Path
from . import coordinator, agents


def _load_env():
    """Carga variables desde un archivo .env en la raíz del proyecto (si existe).

    Así, poner ANTHROPIC_API_KEY en .env SÍ funciona — sin dependencias externas.
    """
    env = Path(__file__).resolve().parent.parent / ".env"
    if not env.exists():
        return
    for raw in env.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def get_client():
    _load_env()
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
