"""ZONA — Pruebas de contrato: la SALIDA de cada herramienta cumple su forma."""
from src import tools

def test_order_status_tiene_campos():
    r = tools.get_order_status("A1001")
    assert "found" in r and "order_id" in r and "status" in r

def test_refund_status_es_texto():
    r = tools.apply_refund("A1002", 40)
    assert isinstance(r["status"], str)

def test_search_menu_devuelve_lista():
    assert isinstance(tools.search_menu("pizza"), list)

def test_menu_items_precio_numerico():
    for it in tools.search_menu("pizza"):
        assert isinstance(it["price"], (int, float))

def test_menu_items_solo_activos():
    for it in tools.search_menu("pizza"):
        assert it.get("active") is True
