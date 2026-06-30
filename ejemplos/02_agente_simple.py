"""
EJEMPLO 2 — Crear un AGENTE simple.

TEORÍA
------
Un AGENTE es más que un prompt suelto. Es:
    LLM  +  un PROMPT que le da un ROL y reglas  +  HERRAMIENTAS  +  un bucle.
La diferencia clave: el agente NO inventa datos — usa una HERRAMIENTA para
consultarlos y luego responde basándose en ese dato real.

Aquí: un agente de Pedidos. Su herramienta consulta el estado real del pedido;
el LLM solo redacta la respuesta a partir de ese dato.

Correr:  python ejemplos/02_agente_simple.py
"""
from _comun import llamar_llm, titulo, hay_key

# --- HERRAMIENTA: consulta datos reales (no los inventa) ---
PEDIDOS = {
    "A1001": {"estado": "en camino", "eta": "15 min"},
    "A1002": {"estado": "entregado", "eta": None},
}

def herramienta_estado_pedido(order_id):
    """Tool: devuelve el estado real del pedido, o None si no existe."""
    return PEDIDOS.get(order_id.upper())

# --- EL AGENTE ---
ROL = ("Eres el agente de Pedidos de FastDelivery. Responde en UNA frase, "
       "amable, citando el número de pedido. Usa SOLO el dato que te doy.")

def agente_pedidos(order_id):
    dato = herramienta_estado_pedido(order_id)        # 1) usa la herramienta
    if not dato:
        return f"No encuentro el pedido {order_id}."
    hecho = f"Pedido {order_id}: estado={dato['estado']}, eta={dato['eta']}"
    # 2) el LLM redacta la respuesta a partir del dato real
    redaccion = llamar_llm(f"Dato: {hecho}\nRedacta la respuesta al cliente.", system=ROL)
    # 3) si no hay LLM, una plantilla simple (el agente igual funciona)
    return redaccion or f"Tu pedido {order_id} está {dato['estado']} (ETA {dato['eta']})."

titulo("EJEMPLO 2 — Un agente simple (con herramienta)")
for pid in ["A1001", "ZZZZ"]:
    print(f"\nPregunta: ¿dónde está mi pedido {pid}?")
    print(f"  → {agente_pedidos(pid)}")
print(f"\n[modo: {'LLM real' if hay_key() else 'sin key (plantilla)'}]")
