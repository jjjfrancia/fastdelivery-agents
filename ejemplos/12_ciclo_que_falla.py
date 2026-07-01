"""
EJEMPLO 12 — Cuando un ciclo FALLA (y por qué eso es bueno).

TEORÍA
------
Un agente puede generar algo INCOMPLETO y decir "listo". No te das cuenta… hasta que
corres la prueba. Un AUDIT_VERDICT = FAIL no es una crisis: es el sistema funcionando —
atrapó el error ANTES de que llegara al cliente.

Aquí: una función que el agente dejó incompleta (le falta el campo 'total' del recibo).
La prueba lo detecta y FALLA. Ese FAIL es la señal para corregir, no para avanzar.

Correr:  python ejemplos/12_ciclo_que_falla.py
"""
from _comun import titulo

# ── Lo que "generó el agente": un recibo, pero INCOMPLETO (olvidó 'total') ──
def generar_recibo(pedido):
    return {
        "pedido": pedido["id"],
        "items": pedido["items"],
        # el agente olvidó calcular 'total' — se ve casi bien
    }

# ── La PRUEBA (el auditor): verifica que el recibo esté COMPLETO ──
CAMPOS_REQUERIDOS = ["pedido", "items", "total"]

def auditar_recibo(recibo):
    return [c for c in CAMPOS_REQUERIDOS if c not in recibo]   # [] = PASS ; con items = FAIL

titulo("EJEMPLO 12 — Un ciclo que FALLA (el sistema funcionando)")
pedido = {"id": "A1001", "items": ["Pizza"], "precio": 30}
recibo = generar_recibo(pedido)
print("El agente generó:", recibo)
print('El agente dice: "recibo listo ✅"\n')

faltan = auditar_recibo(recibo)
if faltan:
    print(f"🔴 AUDIT_VERDICT = FAIL — faltan campos: {faltan}")
    print("   → El ciclo NO está done. Vuelve a In Progress. NO avances.")
    print("   → Sin esta prueba, el recibo incompleto habría llegado al cliente.")
else:
    print("🟢 AUDIT_VERDICT = PASS — recibo completo")

print("\nIdea: el agente 'creía' que estaba listo. La prueba atrapó lo que faltaba.")
print("Un FAIL detectado a tiempo es barato; uno en producción es caro.")
print("Arréglalo: agrega 'total' en generar_recibo y vuelve a correr → verás PASS.")
