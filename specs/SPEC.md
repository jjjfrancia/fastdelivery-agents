# SPEC — FastDelivery Agents (arquitectura, versión simple)

> Contrato verificable del sistema de agentes. Fuente de verdad del caso práctico.

## 1. Producto y objetivo
Asistente de atención al cliente de **FastDelivery** (reparto). Resuelve consultas repetitivas
—estado de pedido, menú y reembolsos— con calidad medible, trazabilidad y control humano.

**Sprint Goal:** un cliente puede consultar el estado de su pedido, preguntar por el menú y pedir
un reembolso simple, con respuestas correctas, citadas y trazables.

## 2. Arquitectura (Coordinador + Especializados)

```
Usuario
  │
  ▼
Coordinador (Harness)          clasifica intención y rutea; decide cuándo detenerse
  ├─► Agente Pedidos      ──► tool: get_order_status(order_id)
  ├─► Agente Menú         ──► tool: search_menu(query)        (RAG sobre catálogo)
  └─► Agente Reembolsos   ──► tool: apply_refund(order_id, amount)   (HITL si > S/100)
```

- **Coordinador:** orquestación centralizada. No toca herramientas de dominio; solo rutea.
- **Especializados:** ejecución distribuida. Cada uno = 1 prompt + 1 herramienta + redacción.

## 3. Contrato por agente

| Agente | Entrada | Herramienta | Salida | Aceptación |
|--------|---------|-------------|--------|------------|
| Coordinador | pregunta del usuario | — | `intent` ∈ {pedidos, menu, reembolsos, desconocido} | clasifica bien los casos de prueba |
| Pedidos | `order_id` | `get_order_status` | estado + ETA, citando el pedido | responde el estado real del pedido |
| Menú | texto libre | `search_menu` | items vigentes que coinciden | no ofrece productos descontinuados |
| Reembolsos | `order_id`, `amount` | `apply_refund` | aprobado / `needs_human_approval` | bloquea montos > S/100 |

## 4. Guardrails (no negociables)
1. Reembolso **> S/100** ⇒ `needs_human_approval` (HITL). Nunca se aprueba solo.
2. Toda respuesta **cita su fuente** (pedido, menú o política).
3. Latencia objetivo **< 5 s**; costo por consulta acotado.

## 5. Pruebas (las 3 zonas)
- **① Unitaria:** clasificador de intención y lógica de herramientas (offline).
- **② Funcional (e2e):** flujo pregunta → ruteo → herramienta → respuesta (con LLM).
- **③ Integral:** herramientas con datos reales + el HITL de reembolsos.

## 6. Definition of Done
Las 3 zonas en verde · HITL activo · respuestas citadas · dentro del SLA · aprobación del dueño del producto.
