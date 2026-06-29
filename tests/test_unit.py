"""ZONA ① — Pruebas unitarias: lógica pura, sin red, sin LLM."""
from src import coordinator, tools, agents


def test_classify_keyword():
    assert coordinator.classify_keyword("¿dónde está mi pedido A1001?") == "pedidos"
    assert coordinator.classify_keyword("¿tienen pizza hawaiana?") == "menu"
    assert coordinator.classify_keyword("quiero un reembolso") == "reembolsos"
    assert coordinator.classify_keyword("hola buenas") == "desconocido"


def test_search_menu_excluye_descontinuados():
    res = tools.search_menu("pizza")
    nombres = [i["name"] for i in res]
    assert "Pizza Margarita" in nombres
    assert "Pizza Hawaiana" not in nombres  # active=False


def test_apply_refund_hitl():
    assert tools.apply_refund("A1002", 40)["status"] == "approved"
    assert tools.apply_refund("A1002", 150)["status"] == "needs_human_approval"
    assert tools.apply_refund("A1002", -5)["status"] == "error"


def test_get_order_status():
    assert tools.get_order_status("A1001")["found"] is True
    assert tools.get_order_status("ZZZZ")["found"] is False


def test_extractores():
    assert agents.extract_order_id("mi pedido A1001 por favor") == "A1001"
    assert agents.extract_amount("reembolso de 150 soles") == 150.0
