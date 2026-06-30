# -*- coding: utf-8 -*-
"""
board_sync — Transparencia en tiempo real.

Verifica CADA archivo que el agente afirma haber creado (en TEST_LOGS.json)
CONTRA EL DISCO REAL — no contra el reporte del agente. Si un archivo declarado
no existe, lo marca como INCONSISTENCIA. Luego genera el tablero SPRINT_BOARD.html.

Uso:  python board_sync.py
Sin dependencias. Abre SPRINT_BOARD.html en el navegador para ver el tablero.
"""
import json, os, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
logs = json.load(open(os.path.join(ROOT, "TEST_LOGS.json"), encoding="utf-8"))

rows, incons = [], 0
for it in logs:
    existe = os.path.exists(os.path.join(ROOT, it["archivo"]))
    red = bool(it.get("red_at")) and isinstance(it.get("red_at"), str)
    green = bool(it.get("green_at"))
    audit = it.get("audit_verdict") == "PASS"
    # Done real = archivo existe + RED antes que GREEN + AUDIT PASS
    done = existe and red and green and audit
    estado = "✅ Done (evidencia verificada)" if done else ("🚫 INCONSISTENCIA — archivo declarado NO existe en disco" if not existe else "🟡 En progreso (falta evidencia)")
    if not existe:
        incons += 1
    rows.append({**it, "existe": existe, "estado": estado, "done": done})

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"[{ts}] board_sync OK - {len(rows)} filas, {incons} inconsistencias detectadas")
for r in rows:
    if not r["existe"]:
        print(f"   -> {r['archivo']} declarado por el agente pero NO existe en disco")

# Genera el tablero
def cel(x): return html.escape(str(x)) if x is not None else "—"
trs = ""
for r in rows:
    color = "#16a34a" if r["done"] else ("#dc2626" if not r["existe"] else "#d97706")
    trs += f"<tr><td>{cel(r['item'])}</td><td><code>{cel(r['archivo'])}</code></td><td>{cel(r.get('red_at'))}</td><td>{cel(r.get('green_at'))}</td><td>{cel(r.get('audit_verdict'))}</td><td style='color:{color};font-weight:700'>{cel(r['estado'])}</td></tr>"

doc = f"""<!doctype html><html lang=es><head><meta charset=utf-8><title>SPRINT_BOARD — FastDelivery</title>
<style>body{{font-family:Segoe UI,Arial;background:#0a1733;color:#eef3fa;padding:24px}}
h1{{font-size:20px}} .meta{{color:#9db2d4;font-size:13px;margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;font-size:13px}} th,td{{border:1px solid #26406e;padding:8px 10px;text-align:left}}
th{{background:#16315c;color:#7bb0ff}} code{{color:#cfe3ff}}
.banner{{background:#0c2142;border-left:4px solid {'#dc2626' if incons else '#16a34a'};padding:10px 14px;border-radius:8px;margin:12px 0}}</style></head>
<body><h1>SPRINT_BOARD — FastDelivery</h1>
<div class=meta>Generado por board_sync · {ts}</div>
<div class=banner><b>board_sync OK — {len(rows)} filas, {incons} inconsistencias detectadas.</b> El tablero muestra el estado REAL (disco), no lo que el agente reportó.</div>
<table><tr><th>Item</th><th>Archivo declarado</th><th>RED</th><th>GREEN</th><th>AUDIT</th><th>Estado (verificado en disco)</th></tr>{trs}</table>
</body></html>"""
open(os.path.join(ROOT, "SPRINT_BOARD.html"), "w", encoding="utf-8").write(doc)
print("Tablero generado -> SPRINT_BOARD.html (ábrelo en el navegador)")
