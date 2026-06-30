"""
EJEMPLO 8 — TODOS trabajando juntos a partir de un PROMPT del usuario.

TEORÍA
------
Aquí se ve el sistema completo en acción: una sola pregunta del usuario entra,
el HARNESS la clasifica, el AGENTE especializado usa su HERRAMIENTA (datos reales),
el GUARDRAIL protege las acciones sensibles, y opcionalmente el LLM redacta la
respuesta final. Es el ciclo entero, de principio a fin.

    Prompt del usuario → Harness (rutea) → Agente → Herramienta/Guardrail → Respuesta

Correr:  python ejemplos/08_todos_juntos.py
"""
import re
from _comun import llamar_llm, titulo, hay_key

PEDIDOS = {"A1001": {"estado": "en camino", "eta": "15 min"},
           "A1002": {"estado": "entregado", "eta": None}}
MENU = ["Pizza Margarita", "Hamburguesa Clásica", "Lomo Saltado"]

def _id(t):    m = re.search(r"[A-Za-z]\d{3,}", t); return m.group(0).upper() if m else ""
def _monto(t): m = re.search(r"\d+", t); return float(m.group(0)) if m else 0

def manejar(pregunta):
    p = pregunta.lower()
    # HARNESS: clasifica y delega
    if "reembolso" in p:
        monto = _monto(p)
        if monto > 100:                                   # GUARDRAIL
            return f"Tu reembolso de S/{monto:.0f} supera S/100: lo aprueba un humano."
        return f"Reembolso de S/{monto:.0f} aprobado."
    if "pedido" in p or "donde" in p:
        d = PEDIDOS.get(_id(p))                            # HERRAMIENTA (dato real)
        hecho = f"pedido {_id(p)}: {d['estado']}, ETA {d['eta']}" if d else "pedido no encontrado"
    elif any(w in p for w in ["menu","menú","pizza","tienen","hamburguesa","lomo"]):
        r = [m for m in MENU if any(t in m.lower() for t in p.split())]
        hecho = f"en el menú: {', '.join(r)}" if r else "eso no está en el menú"
    else:
        return "No sé a qué área enviar esto (y no invento)."
    # el LLM redacta a partir del HECHO real (o plantilla si no hay key)
    red = llamar_llm(f"Dato real: {hecho}. Redacta UNA frase amable al cliente.",
                     system="Eres el asistente de FastDelivery. Una frase, citando datos.")
    return red or f"Información: {hecho}."

titulo("EJEMPLO 8 — Todo el sistema junto")
for q in ["¿dónde está mi pedido A1001?",
          "¿tienen pizza margarita?",
          "quiero un reembolso de 40 soles del A1002",
          "quiero un reembolso de 150 soles del A1002"]:
    print(f"\n👤 {q}\n🤖 {manejar(q)}")

print(f"\n[modo: {'LLM real redacta' if hay_key() else 'sin key (plantillas)'}]")
print("Esto es el harness + agentes + herramientas + guardrail, de punta a punta.")
