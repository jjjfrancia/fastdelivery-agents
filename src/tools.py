"""Herramientas de dominio de FastDelivery (tool / function calling).

Cada herramienta es un contrato: entrada tipada, salida estructurada y validada,
errores explícitos. Son funciones puras y testeables sin red.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

REFUND_HITL_THRESHOLD = 100.0  # S/100 — guardrail: por encima requiere humano


def _load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def get_order_status(order_id: str) -> dict:
    """Estado de un pedido. Devuelve {found, order_id, status, eta} o found=False."""
    if not order_id:
        return {"found": False, "order_id": order_id, "error": "order_id vacío"}
    orders = _load("orders.json")
    o = orders.get(order_id.upper())
    if not o:
        return {"found": False, "order_id": order_id}
    return {"found": True, "order_id": order_id.upper(), "status": o["status"], "eta": o.get("eta")}


def search_menu(query: str) -> list:
    """Busca en el catálogo SOLO productos vigentes (active=True)."""
    q = (query or "").lower()
    items = _load("catalog.json")
    out = []
    for it in items:
        if not it.get("active"):
            continue  # nunca ofrecer descontinuados (guardrail)
        if any(tok and tok in it["name"].lower() for tok in q.split()):
            out.append(it)
    return out


def apply_refund(order_id: str, amount: float) -> dict:
    """Aplica un reembolso. Monto > S/100 => needs_human_approval (HITL)."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return {"status": "error", "error": "monto inválido"}
    if amount <= 0:
        return {"status": "error", "error": "el monto debe ser positivo"}
    if amount > REFUND_HITL_THRESHOLD:
        return {"status": "needs_human_approval", "order_id": order_id, "amount": amount,
                "reason": f"monto > S/{REFUND_HITL_THRESHOLD:.0f} requiere aprobación humana"}
    return {"status": "approved", "order_id": order_id, "amount": amount}
