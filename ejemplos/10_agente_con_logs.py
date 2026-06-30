"""
EJEMPLO 10 — Un agente que genera LOGS (observabilidad).

TEORÍA
------
No puedes confiar en lo que no puedes ver. Un agente debe dejar un RASTRO (logs) de
qué decidió y qué herramienta usó. Eso es OBSERVABILIDAD: si algo sale mal, lees el
log y entiendes por qué — sin adivinar. Es un requisito de diseño, no un extra.

Correr:  python ejemplos/10_agente_con_logs.py   →   escribe agente.log
"""
from pathlib import Path
from _comun import titulo

LOG = Path(__file__).resolve().parent / "agente.log"
PEDIDOS = {"A1001": {"estado": "en camino"}}

def log(evento, detalle):
    linea = f"[{evento}] {detalle}"
    print("   " + linea)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")

def agente_con_logs(pregunta):
    log("ENTRADA", f"pregunta del usuario: {pregunta!r}")
    if "pedido" not in pregunta.lower():
        log("DECISION", "no es sobre pedidos -> no atiendo")
        return "No es mi área."
    import re
    oid = (re.search(r"[A-Za-z]\d{3,}", pregunta) or [None])
    oid = oid.group(0).upper() if hasattr(oid, "group") else ""
    log("TOOL_CALL", f"get_order_status({oid})")
    dato = PEDIDOS.get(oid)
    log("TOOL_RESULT", f"{dato}")
    resp = f"Tu pedido {oid} está {dato['estado']}." if dato else "No encuentro ese pedido."
    log("RESPUESTA", resp)
    return resp

titulo("EJEMPLO 10 — Agente con logs (observabilidad)")
LOG.write_text("", encoding="utf-8")   # empezar log limpio
print("Pregunta: ¿dónde está mi pedido A1001?\nLog del agente:")
respuesta = agente_con_logs("¿dónde está mi pedido A1001?")
print(f"\nRespuesta final: {respuesta}")
print(f"\nEl rastro completo quedó en: {LOG.name}")
print("Idea: cada decisión y cada llamada a herramienta queda registrada. Si el")
print("agente falla, el log te dice exactamente dónde — eso es observabilidad.")
