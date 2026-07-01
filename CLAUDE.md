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

## Proceso Scrum (cómo debes trabajar en cada Sprint)
Estas son las reglas de Scrum que sigues como agente. El equipo humano las inspecciona.
- **Trabaja hacia el Sprint Goal** (`specs/SPEC.md` ①). Todo lo que no sirve al Goal va al `backlog.md`, no lo construyes "de paso".
- **Ciclos cortos (Ciclos de Convergencia):** entrega valor **apenas lo tengas, no al final** del Sprint. Así el equipo inspecciona seguido y el trabajo no se acumula.
- **Por cada capacidad:** escribe la prueba primero (RED) → impleméntala hasta GREEN → registra `red_at`/`green_at` en `TEST_LOGS.json` (el RED debe ser anterior al GREEN).
- **No te autoapruebes.** GREEN es solo **un** ítem del DoD. Un ítem está *Done* solo con **AUDIT PASS** (agente auditor independiente) **y** todo el `dod.md` cumplido. El humano (PO) marca Done, no tú. Tu techo es: "Evidencia lista — esperando al PO".
- **Respeta los guardrails** del SPEC (⑤) y escala a humano lo que la política exige (p. ej. reembolso > S/100).
- **Deja evidencia y trazas** (logs, TEST_LOGS.json, board_sync) para que el equipo pueda inspeccionar sin creerte "de palabra".

## Estilo
- Respuestas al cliente: **1–2 frases**, amables, citando el dato real.
- Código: claro y con pruebas en `tests/`. Sin dependencias innecesarias.
