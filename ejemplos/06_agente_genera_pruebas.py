"""
EJEMPLO 6 — Un AGENTE que CREA las pruebas (TDD asistido por IA).

TEORÍA
------
Una de las cosas más útiles de un agente: que escriba las PRUEBAS por ti, siguiendo
TDD. Le das una función (o su descripción) y el agente genera un test de pytest con
casos normales y casos límite. Tú luego lo corres y verificas.

Con API key: el modelo genera el test de verdad y lo guarda.
Sin key: te muestra el prompt exacto y un test de ejemplo (para que veas el resultado).

Correr:  python ejemplos/06_agente_genera_pruebas.py
"""
from pathlib import Path
from _comun import llamar_llm, titulo, hay_key

FUNCION = '''
def calcular_total(precio_unitario, cantidad, descuento=0.0):
    """Total = precio*cantidad menos un descuento (0..1). Error si datos inválidos."""
    if precio_unitario < 0 or cantidad < 0:
        raise ValueError("precio y cantidad no pueden ser negativos")
    return precio_unitario * cantidad * (1 - descuento)
'''

PROMPT = f"""Escribe un archivo de pruebas de pytest para esta función.
Incluye: un caso normal, un caso con descuento, y un caso de error (ValueError).
Devuelve SOLO el código Python, sin explicaciones.

{FUNCION}"""

EJEMPLO_SIN_KEY = '''import pytest
from calcular import calcular_total

def test_caso_normal():
    assert calcular_total(10, 3) == 30

def test_con_descuento():
    assert calcular_total(10, 2, 0.5) == 10

def test_error_negativos():
    with pytest.raises(ValueError):
        calcular_total(-1, 2)'''

titulo("EJEMPLO 6 — Un agente genera las pruebas (TDD con IA)")
print("Función a probar:")
print(FUNCION)
print("PROMPT que se le da al agente:")
print(f"  «{PROMPT.splitlines()[0]} ...»\n")

generado = llamar_llm(PROMPT, system="Eres un experto en pruebas con pytest. Respondes solo código.")
test = generado or EJEMPLO_SIN_KEY

salida = Path(__file__).resolve().parent / "salida_test_generado.py"
salida.write_text(test, encoding="utf-8")
print("PRUEBA GENERADA (guardada en ejemplos/salida_test_generado.py):\n")
print(test)
print(f"\n[modo: {'LLM real' if hay_key() else 'demostración sin key'}]")
print("Siguiente paso (TDD): correrías esta prueba con  python -m pytest  para verla en verde.")
