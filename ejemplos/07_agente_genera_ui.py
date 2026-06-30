"""
EJEMPLO 7 — Un AGENTE que CREA una UI (interfaz) en HTML.

TEORÍA
------
Un agente también puede generar la INTERFAZ. Le describes la pantalla que quieres y
genera el HTML. Esto muestra cómo un agente produce un entregable que un humano usa
de verdad (no solo texto).

Con API key: el modelo genera el HTML.
Sin key: se escribe una UI de ejemplo, para que veas el resultado igual.

Correr:  python ejemplos/07_agente_genera_ui.py   →   abre ejemplos/ui_generada.html
"""
from pathlib import Path
from _comun import llamar_llm, titulo, hay_key

PROMPT = """Crea una página HTML simple y autocontenida (sin librerías externas) para
un asistente de FastDelivery: un título, una caja de texto para escribir la pregunta,
un botón 'Preguntar', y un área de respuesta. Estilo limpio. Devuelve SOLO el HTML."""

UI_SIN_KEY = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>FastDelivery — Asistente</title><style>
body{font-family:Segoe UI,Arial,sans-serif;background:#f1f5f9;display:flex;justify-content:center;padding:40px}
.box{background:#fff;border-radius:14px;padding:24px;max-width:480px;width:100%;box-shadow:0 6px 20px rgba(0,0,0,.08)}
h1{font-size:20px;color:#1e293b;margin:0 0 12px}
input{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:8px;font-size:14px;box-sizing:border-box}
button{margin-top:10px;background:#2563eb;color:#fff;border:0;border-radius:8px;padding:12px 18px;font-size:14px;cursor:pointer}
#resp{margin-top:16px;background:#f8fafc;border-radius:8px;padding:14px;color:#334155;min-height:40px}
</style></head><body><div class="box">
<h1>🍔 Asistente FastDelivery</h1>
<input id="q" placeholder="Ej: ¿dónde está mi pedido A1001?">
<button onclick="document.getElementById('resp').innerText='(Aquí respondería el agente: pedido A1001 en camino, ETA 15 min.)'">Preguntar</button>
<div id="resp">Tu respuesta aparecerá aquí.</div>
</div></body></html>"""

titulo("EJEMPLO 7 — Un agente genera la UI")
print("PROMPT que se le da al agente:")
print(f"  «{PROMPT.splitlines()[0]} ...»\n")

html = llamar_llm(PROMPT, system="Eres un experto en frontend. Respondes solo HTML.") or UI_SIN_KEY
# si el modelo devolvió texto con ```html, limpiarlo
if "```" in html:
    html = html.split("```")[1].replace("html", "", 1).strip() if html.count("```") >= 2 else html

salida = Path(__file__).resolve().parent / "ui_generada.html"
salida.write_text(html, encoding="utf-8")
print(f"UI generada (ábrela en el navegador): ejemplos/ui_generada.html")
print(f"\n[modo: {'LLM real' if hay_key() else 'demostración sin key'}]")
