"""
EJEMPLO 11 — Un AGENTE DE PRUEBAS separado (quien genera no se autoaprueba).

TEORÍA
------
Principio clave: el agente que PRODUCE algo NO debe ser el mismo que lo APRUEBA.
Necesitas un segundo agente (de pruebas / auditor) que revise la salida del primero
contra criterios objetivos. Separar "generar" de "verificar" evita que un agente
diga "está perfecto" sobre su propio trabajo.

Aquí: el Agente A responde; el Agente B (auditor) verifica que la respuesta cumpla
las reglas (cita el pedido, no inventa, una sola frase).

Correr:  python ejemplos/11_agente_de_pruebas.py
"""
from _comun import llamar_llm, titulo, hay_key

# AGENTE A — produce la respuesta
def agente_respuesta(order_id):
    return f"Tu pedido {order_id} está en camino, ETA 15 min."

# AGENTE B — auditor: verifica contra criterios (no confía, comprueba)
CRITERIOS = ["cita el número de pedido", "no promete cosas no pedidas", "es breve (1 frase)"]

def agente_auditor(order_id, respuesta):
    # 1) chequeos objetivos en código (siempre corren, con o sin key)
    veredicto = {
        "cita el pedido": order_id in respuesta,
        "es breve (1 frase)": respuesta.count(".") <= 1,
    }
    # 2) opcional: un juicio del LLM como segunda opinión
    juicio_llm = llamar_llm(
        f"Respuesta: «{respuesta}». ¿Cumple estos criterios? {CRITERIOS}. "
        f"Responde PASS o FAIL y una razón corta.",
        system="Eres un auditor estricto de calidad.")
    return veredicto, juicio_llm

titulo("EJEMPLO 11 — Agente de pruebas separado (auditor)")
oid = "A1001"
resp = agente_respuesta(oid)
print(f"AGENTE A responde: {resp}\n")
chequeos, juicio = agente_auditor(oid, resp)
print("AGENTE B (auditor) verifica:")
for k, ok in chequeos.items():
    print(f"   {'✅' if ok else '❌'} {k}")
veredicto = "PASS" if all(chequeos.values()) else "FAIL"
print(f"\nVeredicto por chequeos en código: {veredicto}")
if juicio:
    print(f"Segunda opinión del LLM: {juicio.strip()}")
else:
    print("(sin key) El LLM daría una segunda opinión PASS/FAIL con su razón.")
print(f"\n[modo: {'LLM real' if hay_key() else 'demostración sin key'}]")
print("Idea: quien genera NO se autoaprueba. Un auditor separado da la confianza.")
