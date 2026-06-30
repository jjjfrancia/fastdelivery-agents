"""Utilidades compartidas por los ejemplos. Lee la API key del .env y llama al LLM.

Si NO hay API key, llamar_llm() devuelve None y cada ejemplo sigue funcionando en
"modo demostración" (te muestra el prompt y un resultado de ejemplo). Así el ejemplo
SIEMPRE corre, con o sin key.
"""
import os
from pathlib import Path


def cargar_env():
    """Carga ANTHROPIC_API_KEY desde el archivo .env de la carpeta del proyecto."""
    env = Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                k, v = linea.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def hay_key():
    cargar_env()
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def llamar_llm(prompt, system="Eres un asistente útil y breve.", max_tokens=1024):
    """Ejecuta UN prompt contra el modelo Claude. Devuelve el texto, o None si no hay key."""
    cargar_env()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=os.environ.get("MODEL", "claude-sonnet-4-6"),
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def titulo(txt):
    print("\n" + "=" * 64 + f"\n  {txt}\n" + "=" * 64)
