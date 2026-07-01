# CLAUDE.md — FastDelivery Agents

La **memoria escrita del proyecto**: reglas que un agente de IA (por ejemplo Claude Code)
debe seguir SIEMPRE al trabajar aquí. El agente lo lee al inicio de cada sesión.

## Proyecto
FastDelivery: asistente de atención al cliente (pedidos, menú, reembolsos) con un
**Coordinador (harness)** que rutea + **Agentes especializados**, cada uno con su herramienta.
- Contrato (qué construir): `specs/SPEC.md`
- Orden de trabajo: `backlog.md`
- Definition of Done: `dod.md`

## Reglas / Guardrails (no negociables)
- **NUNCA** apruebes un reembolso mayor a **S/100**: devuelve `needs_human_approval` (lo decide un humano).
- **NUNCA** ofrezcas productos descontinuados (`active=False`).
- **NUNCA** inventes datos: usa SOLO lo que devuelven las herramientas de `src/tools.py`.
- Toda respuesta al cliente **cita su fuente** (número de pedido, ítem del menú o política).

## Cómo trabajar (TDD)
- Escribe la **prueba primero** (RED), luego el código mínimo hasta que pase (GREEN), luego refactoriza.
- Antes de decir "listo": corre `python -m pytest` y **muestra el resultado**.
- No marques nada como **Done** sin cumplir `dod.md`.

## Estilo
- Respuestas al cliente: **1–2 frases**, amables, citando el dato real.
- Código: claro y con pruebas en `tests/`. Sin dependencias innecesarias.
