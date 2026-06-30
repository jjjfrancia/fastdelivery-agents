# -*- coding: utf-8 -*-
"""
Dashboard de pruebas — transparencia real.

Corre la suite con cobertura y genera PRUEBAS_DASHBOARD.html con:
  - tarjetas resumen + donut de passed/skipped/failed
  - cobertura (% del código realmente probado) por archivo y total, con barras
  - cada prueba por NOMBRE y su estado

Uso:  python test_dashboard.py     (luego abre PRUEBAS_DASHBOARD.html)
Requiere: pytest, pytest-cov  ->  python -m pip install pytest pytest-cov
"""
import subprocess, sys, os, json, html, datetime
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
JUNIT = os.path.join(ROOT, ".junit.xml")
COVJSON = os.path.join(ROOT, ".coverage.json")

print("Corriendo pruebas con cobertura...")
subprocess.run([sys.executable, "-m", "pytest", "--cov=src",
                f"--cov-report=json:{COVJSON}", f"--junitxml={JUNIT}", "-q"],
               cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- nombres y estado de cada prueba (de JUnit) ---
tests = []
if os.path.exists(JUNIT):
    for tc in ET.parse(JUNIT).iter("testcase"):
        st = "passed"
        if tc.find("failure") is not None or tc.find("error") is not None:
            st = "failed"
        elif tc.find("skipped") is not None:
            st = "skipped"
        archivo = (tc.get("classname") or "").split(".")[-1]
        tests.append({"file": archivo, "name": tc.get("name"), "status": st,
                      "time": float(tc.get("time") or 0)})
passed = sum(1 for t in tests if t["status"] == "passed")
skipped = sum(1 for t in tests if t["status"] == "skipped")
failed = sum(1 for t in tests if t["status"] == "failed")
total_t = max(passed + skipped + failed, 1)

# --- cobertura (de coverage json) ---
cov_files, cov_total = [], 0.0
if os.path.exists(COVJSON):
    cj = json.load(open(COVJSON, encoding="utf-8"))
    cov_total = cj["totals"]["percent_covered"]
    for f, d in sorted(cj["files"].items()):
        cov_files.append({"file": f.replace("\\", "/"),
                          "pct": d["summary"]["percent_covered"],
                          "stmts": d["summary"]["num_statements"],
                          "miss": d["summary"]["missing_lines"]})

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
tcol = "#16a34a" if cov_total >= 80 else ("#d97706" if cov_total >= 50 else "#dc2626")
p_end = passed / total_t * 100
s_end = p_end + skipped / total_t * 100
donut = f"conic-gradient(#16a34a 0 {p_end:.1f}%, #d97706 {p_end:.1f}% {s_end:.1f}%, #dc2626 {s_end:.1f}% 100%)"

# filas de cobertura
crows = ""
for c in cov_files:
    col = "#16a34a" if c["pct"] >= 80 else ("#d97706" if c["pct"] >= 50 else "#dc2626")
    crows += (f"<tr><td><code>{html.escape(c['file'])}</code></td><td>{c['stmts']}</td>"
              f"<td>{c['miss']}</td><td><div class=cv><div style='width:{c['pct']:.0f}%;background:{col}'>"
              f"{c['pct']:.0f}%</div></div></td></tr>")

# filas de pruebas
BADGE = {"passed": ("#15803d", "#dcfce7", "passed"),
         "skipped": ("#b45309", "#fef3c7", "skipped"),
         "failed": ("#b91c1c", "#fee2e2", "failed")}
trows = ""
for t in sorted(tests, key=lambda x: (x["file"], x["name"])):
    fg, bg, lbl = BADGE[t["status"]]
    trows += (f"<tr><td><code>{html.escape(t['file'])}</code></td><td>{html.escape(t['name'])}</td>"
              f"<td><span class=bdg style='color:{fg};background:{bg}'>{lbl}</span></td>"
              f"<td>{t['time']:.3f}s</td></tr>")

doc = f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Dashboard de Pruebas — FastDelivery</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#f4f6fb;color:#1e2a44;padding:24px;margin:0}}
.head{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:4px}}
h1{{font-size:22px;margin:0}} .meta{{color:#64748b;font-size:12.5px;margin-bottom:18px}}
.brand{{font-size:12px;color:#7c3aed;font-weight:700}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:18px}}
.card{{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.card .n{{font-size:30px;font-weight:800;line-height:1}} .card .l{{color:#64748b;font-size:11.5px;margin-top:6px;letter-spacing:.03em}}
.grid2{{display:grid;grid-template-columns:340px 1fr;gap:16px;margin-bottom:18px}}
@media(max-width:780px){{.grid2{{grid-template-columns:1fr}}}}
.panel{{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.panel h2{{font-size:14px;margin:0 0 14px;color:#1e2a44}}
.donut{{width:170px;height:170px;border-radius:50%;background:{donut};margin:6px auto;display:flex;align-items:center;justify-content:center}}
.donut .hole{{width:106px;height:106px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.donut .hole b{{font-size:22px}} .donut .hole span{{font-size:11px;color:#64748b}}
.legend{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;font-size:12.5px;margin-top:10px}}
.legend i{{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:middle}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{border-bottom:1px solid #eef2f7;padding:8px 10px;text-align:left}}
th{{color:#64748b;font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.04em}}
code{{color:#7c3aed;background:#f3f0ff;padding:1px 5px;border-radius:4px;font-size:12px}}
.cv{{height:18px;border-radius:5px;background:#eef2f7;overflow:hidden;min-width:140px}}
.cv>div{{height:100%;color:#fff;font-size:11px;font-weight:700;text-align:right;padding:1px 6px;line-height:16px;min-width:24px}}
.bdg{{font-weight:700;font-size:11.5px;padding:2px 10px;border-radius:20px}}
</style></head>
<body>
<div class=head><h1>🧪 Dashboard de Pruebas — FastDelivery</h1>
<div class=brand>CortexGovernor™ Academy · powered by DiscoveryFast</div></div>
<div class=meta>Generado automáticamente por <code>test_dashboard.py</code> · {ts}</div>
<div class=cards>
  <div class=card><div class="n" style="color:{tcol}">{cov_total:.0f}%</div><div class=l>COBERTURA TOTAL</div></div>
  <div class=card><div class="n">{total_t}</div><div class=l>PRUEBAS TOTALES</div></div>
  <div class=card><div class="n" style="color:#16a34a">{passed}</div><div class=l>PASSED</div></div>
  <div class=card><div class="n" style="color:#d97706">{skipped}</div><div class=l>SKIPPED</div></div>
  <div class=card><div class="n" style="color:#dc2626">{failed}</div><div class=l>FAILED</div></div>
</div>
<div class=grid2>
  <div class=panel><h2>Resultado de las pruebas</h2>
    <div class=donut><div class=hole><b style="color:{tcol}">{passed}/{total_t}</b><span>passed</span></div></div>
    <div class=legend><span><i style="background:#16a34a"></i>passed {passed}</span><span><i style="background:#d97706"></i>skipped {skipped}</span><span><i style="background:#dc2626"></i>failed {failed}</span></div>
  </div>
  <div class=panel><h2>Cobertura por archivo — % del código realmente probado</h2>
    <table><tr><th>Archivo</th><th>Líneas</th><th>Sin probar</th><th>Cobertura</th></tr>{crows}
    <tr><td><b>TOTAL</b></td><td></td><td></td><td><b style="color:{tcol}">{cov_total:.0f}%</b></td></tr></table>
  </div>
</div>
<div class=panel><h2>Pruebas por nombre y estado ({total_t})</h2>
  <table><tr><th>Archivo</th><th>Prueba</th><th>Estado</th><th>Tiempo</th></tr>{trows}</table>
</div>
</body></html>"""
open(os.path.join(ROOT, "PRUEBAS_DASHBOARD.html"), "w", encoding="utf-8").write(doc)
print(f"OK -> {passed} passed, {skipped} skipped, {failed} failed | cobertura total {cov_total:.0f}%")
print("Dashboard generado -> PRUEBAS_DASHBOARD.html (ábrelo en el navegador)")
