"""
EJEMPLO 1 — Ejecutar un PROMPT simple.

TEORÍA
------
Un PROMPT es la instrucción en lenguaje natural que le das al modelo (el LLM).
Esto es lo más básico de todo: mandar texto, recibir texto. Aún NO es un agente
(no tiene herramientas ni decide nada): solo responde.

Correr:  python ejemplos/01_prompt_simple.py
"""
from _comun import llamar_llm, titulo, hay_key

PROMPT = "Explica en una frase qué es FastDelivery, una app de delivery de comida."

titulo("EJEMPLO 1 — Un prompt simple")
print("PROMPT enviado al modelo:")
print(f"  «{PROMPT}»\n")

respuesta = llamar_llm(PROMPT)

if respuesta:
    print("RESPUESTA del modelo (Claude):")
    print(f"  {respuesta}")
else:
    print("(No hay API key, así que no llamo al modelo de verdad.)")
    print("Con una key, el modelo respondería algo como:")
    print("  «FastDelivery es una app que conecta clientes con restaurantes para")
    print("   pedir comida a domicilio y seguir el estado del pedido en tiempo real.»")
    print("\nPara activarlo: pon tu clave en el archivo .env (ANTHROPIC_API_KEY=...).")

print(f"\n[modo: {'LLM real' if hay_key() else 'demostración sin key'}]")
