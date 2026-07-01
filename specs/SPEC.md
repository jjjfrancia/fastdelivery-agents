# SPEC — FastDelivery Agents (contrato de 7 componentes)

> Ejemplo REAL de un spec de 7 componentes — el mismo que enseña el curso.
> Fuente de verdad del caso práctico. El QUÉ construir. (El detalle de "terminado"
> vive en `dod.md`; el orden de trabajo, en `backlog.md`.)

## ① SPRINT GOAL
Un cliente puede **consultar el estado de su pedido y pedir un reembolso simple por chat**,
con respuestas correctas, citadas y trazables — y con aprobación humana para montos altos.

## ② USER STORY
Como **cliente de FastDelivery**, quiero **preguntar por mi pedido, el menú o un reembolso**
y recibir una respuesta correcta al instante, para **no esperar a un agente humano**.

## ③ ACCEPTANCE CRITERIA (numerados, binarios — sí/no)
- **AC1:** Ante "¿dónde está mi pedido A1001?", responde el estado real y el ETA del pedido A1001.
- **AC2:** Ante una pregunta de menú, ofrece SOLO productos vigentes (nunca descontinuados).
- **AC3:** Un reembolso ≤ S/100 se aprueba; uno > S/100 devuelve `needs_human_approval`.
- **AC4:** Toda respuesta cita su fuente (número de pedido, ítem del menú o política).
- **AC5:** Si no reconoce la intención, responde "no sé cómo ayudarte con eso" y NO inventa.

## ④ TECHNICAL CONSTRAINTS
- **Stack:** Python (librería estándar) + `anthropic` (opcional, para el LLM).
- **Arquitectura:** Coordinador (harness) que rutea + Agentes especializados (Pedidos, Menú, Reembolsos), cada uno con su herramienta.
- **Herramientas / APIs:** `get_order_status`, `search_menu`, `apply_refund` (en `src/tools.py`).
- **Datos:** `data/orders.json`, `data/catalog.json`.
- **Patrones:** un agente = 1 prompt + 1 herramienta + redacción. Coordinador solo rutea.

## ⑤ GUARDRAILS (× = prohibido)
- × Aprobar un reembolso **> S/100** sin humano (HITL obligatorio).
- × Ofrecer productos **descontinuados** (`active=False`).
- × **Inventar** datos: usar SOLO lo que devuelven las herramientas.
- × Responder **sin citar** la fuente.

## ⑥ EDGE CASES
- Si el pedido **no existe** → responder "no encuentro ese pedido", sin inventar.
- Si el monto del reembolso es **inválido o negativo** → error claro, no aprobar.
- Si la intención es **ambigua/desconocida** → ofrecer las 3 áreas y no adivinar.

## ⑦ DEFINITION OF DONE
- Las **3 zonas de prueba** en verde (unitaria, funcional, integral) — detalle en `dod.md`.
- **HITL activo** para reembolsos > S/100.
- Toda respuesta **cita su fuente**.
- Dentro del **SLA** de latencia (< 5 s) y costo acotado.
- **Aprobación** del dueño del producto.
