# backlog.md — Product Backlog de FastDelivery

Este es el **Sprint Backlog vivo** del proyecto. El curso lo usa como fuente única
de "qué falta y en qué orden". Cada ítem es pequeño, con valor para el usuario, y
tiene un estado verificable (no "lo dice el agente").

> El **Definition of Done** NO vive aquí — vive en su propio archivo `dod.md`
> (se trabaja en el Módulo 6). Aquí solo está el QUÉ y el orden; el DoD es el CÓMO-sé-que-está-listo.

---

## Product Goal
Un cliente puede resolver sus dudas de delivery (pedido, menú, reembolso) hablando
con un asistente, sin esperar a un humano — salvo cuando la política lo exige.

## Sprint Goal (Sprint actual)
El cliente puede **consultar el estado de su pedido y pedir un reembolso**, con el
guardrail de aprobación humana para montos altos.

---

## Backlog — ordenado por valor

| # | Ítem (PBI) | Valor para el cliente | Estado | Evidencia |
|---|-----------|----------------------|--------|-----------|
| 1 | Coordinador rutea la pregunta al agente correcto | recibe respuesta sin elegir menú | ✅ Done | tests verdes (test_unit) |
| 2 | Agente de Pedidos: estado + ETA reales | sabe dónde está su pedido | ✅ Done | test_integration |
| 3 | Agente de Menú: solo productos vigentes | no le ofrecen lo descontinuado | ✅ Done | test_unit |
| 4 | Agente de Reembolsos con guardrail > S/100 (HITL) | reembolsos seguros | ✅ Done | test_integration (HITL) |
| 5 | El asistente cita el número de pedido en cada respuesta | confianza/trazabilidad | 🔄 En curso | — |
| 6 | Pantalla de seguimiento del pedido (UI) | ve el estado sin preguntar | 📋 To Do | — |
| 7 | Agente de Quejas | canaliza reclamos | 📋 To Do (futuro) | — |

Leyenda: ✅ Done (con evidencia) · 🔄 En curso · 📋 To Do

---

## Cómo se usa este backlog en el curso
- **Sprint Planning** (Módulo 4): se elige de aquí el Sprint Backlog y se parte por valor.
- **Daily** (Módulo 5): se inspecciona el progreso REAL de estos ítems (ver `board_sync.py`).
- **Review** (Módulo 7): se demuestra lo que pasó a ✅ con evidencia.
- El estado "Done" se rige por `dod.md` (Módulo 6), no por la opinión del agente.
