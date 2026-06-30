"""
EJEMPLO 4 — Definir GUARDRAILS (límites que el agente NO puede romper).

TEORÍA
------
Un GUARDRAIL es una regla que limita lo que el agente puede hacer, por seguridad
o por reglas de negocio. La forma MÁS FUERTE es en CÓDIGO, porque no depende de
que el modelo "obedezca" el prompt: simplemente no puede saltársela.

Aquí: el guardrail de reembolsos de FastDelivery. Un reembolso mayor a S/100
SIEMPRE pasa por un humano (HITL = Human In The Loop). El agente no lo aprueba solo.

Correr:  python ejemplos/04_guardrails.py
"""
from _comun import titulo

LIMITE_HUMANO = 100.0   # S/100 — el guardrail

def aplicar_reembolso(order_id, monto):
    if monto <= 0:
        return {"estado": "error", "motivo": "el monto debe ser positivo"}
    if monto > LIMITE_HUMANO:                       # GUARDRAIL (en código)
        return {"estado": "requiere_aprobacion_humana", "monto": monto,
                "motivo": f"monto > S/{LIMITE_HUMANO:.0f}"}
    return {"estado": "aprobado", "monto": monto}

titulo("EJEMPLO 4 — Un guardrail en código (HITL de reembolsos)")
for monto in [40, 100, 150, -5]:
    r = aplicar_reembolso("A1002", monto)
    icono = {"aprobado": "✅", "requiere_aprobacion_humana": "🛡", "error": "⚠"}[r["estado"]]
    print(f"\nReembolso de S/{monto}:  {icono} {r['estado']}")
    if r.get("motivo"):
        print(f"   motivo: {r['motivo']}")

print("\nIdea clave: el guardrail vive en el CÓDIGO. Aunque el prompt o el usuario")
print("insistan, un reembolso de S/150 NUNCA se aprueba solo — lo decide un humano.")
