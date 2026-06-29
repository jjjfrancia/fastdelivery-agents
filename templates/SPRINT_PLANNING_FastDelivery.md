# Sprint Planning — FastDelivery (ejemplo lleno)

## 1. Sprint Goal
**Goal:** un cliente puede consultar el estado de su pedido y el menú, y pedir un reembolso simple, sin intervención humana.
**Por qué importa:** las consultas repetitivas (≈30%) saturan a 6 agentes humanos con respuesta media de 8 min; automatizarlas con calidad libera a los humanos y baja el tiempo de respuesta.

## 2. Entradas del negocio y del producto
- **Product Goal:** asistente confiable y trazable para atención al cliente.
- **Usuarios / stakeholders:** clientes (app y WhatsApp), operaciones, soporte.
- **Casos de uso priorizados:** 1) estado de pedido · 2) preguntas de menú · 3) reembolso simple.
- **Valor esperado:** tiempo de respuesta < 10 s en lo repetitivo; menos carga humana.
- **Restricciones / guardrails:** reembolso > S/100 ⇒ HITL · citar fuente · latencia < 5 s · costo acotado.
- **Definition of Ready:** API de pedidos accesible, catálogo indexable, política de reembolsos escrita.

## 3. Entradas técnicas del sistema de agentes
**Coordinador (Harness):** clasifica intención (pedidos/menu/reembolsos/desconocido); rutea; no toca tools de dominio.

| Agente | Dominio | Herramientas / APIs | RAG / fuentes | Entrada → Salida |
|--------|---------|---------------------|---------------|------------------|
| Pedidos | estado/seguimiento | get_order_status | orders.json (API real) | order_id → estado + ETA |
| Menú | productos | search_menu | catalog.json (RAG) | texto → items vigentes |
| Reembolsos | devoluciones | apply_refund | política | order_id, amount → aprobado / HITL |

## 4. Qué se discute
- **Definir:** Goal arriba; alcance = 3 casos; reembolsos solo monto simple.
- **Discutir:** dependencia del índice de catálogo (riesgo de datos viejos).
- **Diseñar:** contratos de las 3 tools; prompts de sistema por agente.
- **Plantear:** TDD por capas; responsables; demo en Review con métricas.

## 5. Sprint Backlog (items → tareas)
| # | Item (PBI) | Tarea atómica | Responsable | Zona(s) |
|---|-----------|---------------|-------------|---------|
| 1 | Clasificación de intención | classify_keyword + classify (LLM) | Dev A | ①② |
| 2 | Estado de pedido | get_order_status + handle_pedidos | Dev B | ①②③ |
| 3 | Menú vigente | search_menu (excluir inactivos) + handle_menu | Dev B | ①②③ |
| 4 | Reembolso con HITL | apply_refund (umbral S/100) + handle_reembolsos | Dev A | ①③ |

## 6. Plan de pruebas
- **① Unitaria:** clasificador, search_menu excluye descontinuados, umbral de apply_refund.
- **② Funcional (e2e):** clasificación con LLM enruta correctamente (gated por API key).
- **③ Integral:** flujo completo con tools reales + HITL de reembolsos.

## 7. Definition of Done
- [x] 3 zonas en verde · [x] HITL > S/100 · [x] respuestas citadas · [ ] SLA medido en Review · [ ] aprobación del dueño del producto

## 8. Riesgos, dependencias y capacidad
- **Riesgo:** índice de catálogo desactualizado → respuestas de menú erradas (mitigar: reindexar por hora).
- **Timebox:** 1 Sprint corto; reembolsos completos quedan para el Sprint 2.
