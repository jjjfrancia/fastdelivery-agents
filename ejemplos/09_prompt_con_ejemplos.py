"""
EJEMPLO 9 — Un buen PROMPT: con CONTEXTO y EJEMPLOS (few-shot).

TEORÍA
------
Un prompt mejora muchísimo si le das (1) CONTEXTO del dominio y (2) EJEMPLOS de
entrada→salida ("few-shot"). El modelo imita el formato de tus ejemplos, así que
las respuestas salen consistentes y útiles. Es la diferencia entre pedir "clasifica
esto" y mostrar 2-3 ejemplos de cómo quieres la clasificación.

Correr:  python ejemplos/09_prompt_con_ejemplos.py
"""
from _comun import llamar_llm, titulo, hay_key

ENTRADA = "no me llegó mi pedido y ya pagué"

PROMPT_POBRE = f"Clasifica este mensaje: {ENTRADA}"

PROMPT_BUENO = f"""CONTEXTO: Eres el clasificador de FastDelivery, una app de delivery.
Clasifica el mensaje del cliente en una de: PEDIDO, MENU, REEMBOLSO, QUEJA.
Responde SOLO la etiqueta.

EJEMPLOS:
Mensaje: "¿dónde está mi pedido A1001?"      -> PEDIDO
Mensaje: "¿tienen pizza hawaiana?"            -> MENU
Mensaje: "quiero que me devuelvan mi dinero"  -> REEMBOLSO
Mensaje: "el repartidor fue grosero"          -> QUEJA

Mensaje: "{ENTRADA}" ->"""

titulo("EJEMPLO 9 — Prompt con contexto y ejemplos (few-shot)")
print("❌ Prompt pobre (sin contexto ni ejemplos):")
print(f"   «{PROMPT_POBRE}»\n")
print("✅ Prompt bueno (contexto + 4 ejemplos):")
print("   incluye el rol, las etiquetas válidas y ejemplos entrada→salida.\n")

r = llamar_llm(PROMPT_BUENO, system="Respondes solo con la etiqueta, en mayúsculas.")
if r:
    print(f"Resultado del prompt BUENO para «{ENTRADA}»:  {r.strip()}")
else:
    print(f"(sin key) Con el prompt bueno, el modelo respondería:  REEMBOLSO")
    print("Con el prompt pobre, respondería texto largo e impredecible.")
print(f"\n[modo: {'LLM real' if hay_key() else 'demostración sin key'}]")
print("Regla: en el Sprint Planning, define el CONTEXTO y los EJEMPLOS del prompt como")
print("parte del diseño del agente. Un prompt sin ejemplos es una fuente de errores.")
