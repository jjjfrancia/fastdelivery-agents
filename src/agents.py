"""Agentes especializados: cada uno = 1 prompt + 1 herramienta + redacción.

Las herramientas son deterministas (datos reales). El LLM solo redacta la respuesta
final si hay cliente; sin cliente, se usa una plantilla. Toda respuesta cita su fuente.
"""
import re
from pathlib import Path
from . import tools

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


def _read(name):
    return (PROMPTS / name).read_text(encoding="utf-8")


def extract_order_id(text: str):
    m = re.search(r"\b([A-Za-z]\d{3,})\b", text or "")
    return m.group(1).upper() if m else None


def extract_amount(text: str):
    m = re.search(r"(\d+(?:[.,]\d+)?)", text or "")
    return float(m.group(1).replace(",", ".")) if m else None


def _phrase(system_file, tool_result, question, client, model):
    """Redacta con el LLM usando el resultado de la herramienta (si hay cliente)."""
    if client is None:
        return None
    system = _read(system_file)
    user = f"Consulta del cliente: {question}\nResultado de la herramienta: {tool_result}"
    msg = client.messages.create(model=model, max_tokens=300, system=system,
                                 messages=[{"role": "user", "content": user}])
    return msg.content[0].text.strip()


def handle_pedidos(question, client=None, model="claude-sonnet-4-6"):
    oid = extract_order_id(question)
    res = tools.get_order_status(oid or "")
    if not res["found"]:
        base = f"No encuentro el pedido {oid or '(sin código)'}. Verifica el código, por favor."
    else:
        eta = f", ETA {res['eta']}" if res.get("eta") else ""
        base = f"Según el pedido {res['order_id']}: tu pedido está {res['status']}{eta}."
    return _phrase("pedidos.txt", res, question, client, model) or base


def handle_menu(question, client=None, model="claude-sonnet-4-6"):
    res = tools.search_menu(question)
    if not res:
        base = "Según el menú, no tengo ese producto disponible ahora. ¿Te ayudo con otra cosa?"
    else:
        items = ", ".join(f"{i['name']} (S/{i['price']:.2f})" for i in res)
        base = f"Según el menú, sí tenemos: {items}."
    return _phrase("menu.txt", res, question, client, model) or base


def handle_reembolsos(question, client=None, model="claude-sonnet-4-6"):
    oid = extract_order_id(question) or "(sin código)"
    amount = extract_amount(question) or 0.0
    res = tools.apply_refund(oid, amount)
    if res["status"] == "approved":
        base = f"Según la política de reembolsos, tu reembolso de S/{amount:.2f} del pedido {oid} fue aprobado."
    elif res["status"] == "needs_human_approval":
        base = (f"Según la política, un reembolso de S/{amount:.2f} supera el límite automático: "
                f"escalé tu caso a un agente humano y te responderá pronto.")
    else:
        base = "No pude procesar el reembolso: " + res.get("error", "datos incompletos") + "."
    return _phrase("reembolsos.txt", res, question, client, model) or base


HANDLERS = {"pedidos": handle_pedidos, "menu": handle_menu, "reembolsos": handle_reembolsos}
