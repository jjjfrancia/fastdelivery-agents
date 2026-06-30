"""
EJEMPLO 5 — El HARNESS llamando a los AGENTES (sistema completo, mínimo).

TEORÍA
------
Aquí juntamos todo: un coordinador que rutea a agentes especializados, cada uno
con su HERRAMIENTA (datos reales) y con el GUARDRAIL aplicado. Esto es, en pequeño,
exactamente la arquitectura del proyecto FastDelivery.

    Usuario → Coordinador (decide) → Agente especializado → Herramienta (datos) → Respuesta
                                                           ↳ Guardrail (reembolsos)

Correr:  python ejemplos/05_harness_con_agentes.py
"""
from _comun import titulo

# --- DATOS / HERRAMIENTAS ---
PEDIDOS = {"A1001": {"estado": "en camino", "eta": "15 min"},
           "A1002": {"estado": "entregado", "eta": None}}
MENU = ["Pizza Margarita", "Hamburguesa Clásica", "Lomo Saltado"]

def tool_pedido(oid): return PEDIDOS.get(oid.upper())
def tool_menu(q):     return [p for p in MENU if any(t in p.lower() for t in q.lower().split())]
def tool_reembolso(monto):
    return "requiere_aprobacion_humana" if monto > 100 else "aprobado"   # GUARDRAIL

import re
def _id(t):   m = re.search(r"[A-Za-z]\d{3,}", t); return m.group(0).upper() if m else ""
def _monto(t): m = re.search(r"\d+", t); return float(m.group(0)) if m else 0

# --- AGENTES ESPECIALIZADOS ---
def agente_pedidos(p):
    d = tool_pedido(_id(p))
    return f"Tu pedido {_id(p)} está {d['estado']} (ETA {d['eta']})." if d else "No encuentro ese pedido."
def agente_menu(p):
    r = tool_menu(p);  return f"Sí, tenemos: {', '.join(r)}." if r else "No tenemos eso en el menú."
def agente_reembolsos(p):
    estado = tool_reembolso(_monto(p))
    return ("Reembolso aprobado." if estado == "aprobado"
            else "Tu reembolso supera S/100: lo revisará un humano (guardrail).")

# --- EL HARNESS ---
def harness(pregunta):
    p = pregunta.lower()
    if "reembolso" in p:                 return "reembolsos", agente_reembolsos(pregunta)
    if "pedido" in p or "donde" in p:    return "pedidos", agente_pedidos(pregunta)
    if any(w in p for w in ["menu","menú","pizza","tienen","hamburguesa"]):
        return "menu", agente_menu(pregunta)
    return "—", "No sé a qué área enviar esto (y no invento)."

titulo("EJEMPLO 5 — Harness + agentes + herramientas + guardrail")
for q in ["¿dónde está mi pedido A1001?",
          "¿tienen pizza hawaiana?",
          "quiero un reembolso de 40 soles del A1002",
          "quiero un reembolso de 150 soles del A1002"]:
    destino, resp = harness(q)
    print(f"\nUsuario: {q}\n  → [{destino}] {resp}")

print("\nEsto es un sistema multi-agente completo en miniatura. El proyecto real")
print("(src/) es esto mismo, más ordenado y con pruebas.")
