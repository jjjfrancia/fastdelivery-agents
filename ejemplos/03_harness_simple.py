"""
EJEMPLO 3 — Crear un HARNESS simple (agente coordinador).

TEORÍA
------
Un HARNESS (o agente coordinador) NO resuelve el problema él mismo: recibe la
petición, DECIDE quién debe atenderla (ruteo) y entrega la respuesta. Es el
"jefe de turno" que reparte el trabajo.

Aquí: un coordinador mínimo que rutea a 3 áreas según palabras clave.
(En un sistema real, esta decisión la puede tomar un LLM; la idea es la misma.)

Correr:  python ejemplos/03_harness_simple.py
"""
from _comun import titulo

# Los "agentes" especializados (aquí simplificados a funciones)
def agente_pedidos(p):     return f"[Pedidos] reviso el estado de tu pedido."
def agente_menu(p):        return f"[Menú] busco eso en la carta."
def agente_reembolsos(p):  return f"[Reembolsos] proceso tu solicitud de reembolso."

# --- EL HARNESS / COORDINADOR ---
def coordinador(pregunta):
    p = pregunta.lower()
    if "pedido" in p or "donde esta" in p:        # 1) DECIDE (ruteo)
        destino, agente = "pedidos", agente_pedidos
    elif "reembolso" in p or "devolu" in p:
        destino, agente = "reembolsos", agente_reembolsos
    elif "menu" in p or "menú" in p or "pizza" in p or "tienen" in p:
        destino, agente = "menu", agente_menu
    else:
        return ("coordinador", "No sé a qué área enviar esto. No invento una respuesta.")
    return destino, agente(pregunta)              # 2) DELEGA y devuelve

titulo("EJEMPLO 3 — Un harness simple (coordinador que rutea)")
preguntas = [
    "¿dónde está mi pedido A1001?",
    "¿tienen pizza hawaiana?",
    "quiero un reembolso de 40 soles",
    "¿qué hora es?",
]
for q in preguntas:
    destino, respuesta = coordinador(q)
    print(f"\nUsuario: {q}")
    print(f"  Coordinador → ruteo a: {destino}")
    print(f"  Respuesta: {respuesta}")

print("\nIdea clave: el harness DECIDE y DELEGA; los agentes hacen el trabajo.")
