"""ZONA ③ — Pruebas integrales: flujo completo con herramientas reales + HITL (offline)."""
from src.main import answer


def test_flujo_pedido():
    r = answer("¿dónde está mi pedido A1001?")
    assert "A1001" in r and "en camino" in r


def test_flujo_menu_descontinuado():
    r = answer("¿tienen pizza hawaiana?").lower()
    assert "margarita" in r or "no" in r  # nunca ofrece la hawaiana (descontinuada)
    assert "hawaiana" not in r.replace("pizza hawaiana?", "")


def test_flujo_reembolso_aprobado():
    r = answer("quiero un reembolso de 40 soles del pedido A1002").lower()
    assert "aprobado" in r


def test_flujo_reembolso_hitl():
    r = answer("quiero un reembolso de 150 soles del pedido A1002").lower()
    assert "humano" in r or "escal" in r  # guardrail HITL > S/100
