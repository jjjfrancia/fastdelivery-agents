# dod.md — Definition of Done para agentes (FastDelivery)

El **Definition of Done (DoD)** es el contrato de calidad: una historia NO está "hecha"
hasta que cumple **todos** estos puntos, **con evidencia** (no porque el agente lo diga).

> El DoD vive aquí, separado del `backlog.md` (que define el QUÉ y el orden).
> El backlog dice qué construir; el DoD dice cómo sé que está realmente terminado.

---

## DoD para una historia de agentes

- [ ] La historia entrega **valor verificable** al usuario (no solo "código escrito").
- [ ] El **Agente Coordinador (harness)** ejecuta el flujo definido sin errores críticos.
- [ ] Los **agentes especializados** cumplen su rol y tienen su prueba.
- [ ] Se aplican los **guardrails y políticas** definidos (p. ej. HITL en reembolsos > S/100).
- [ ] Las respuestas citan **fuentes / datos trazables** (sin alucinación).
- [ ] **Logs y traces** quedan almacenados para auditoría (observabilidad).
- [ ] **Métricas dentro de objetivo**: tasa de éxito, precisión, tasa de alucinación.
- [ ] **Costo y latencia** dentro de los límites acordados.
- [ ] **Sin regresiones**: todas las pruebas en verde (`python -m pytest`).
- [ ] **Cobertura** suficiente en la lógica crítica (`--cov`).
- [ ] **Documentación** mínima + pruebas reproducibles.
- [ ] **Despliegue exitoso** en el entorno objetivo.

## Cómo se evalúa cada ítem
Cada punto se marca con: **Cumplido · Parcialmente cumplido · No cumplido · No aplica**.
Si algo está "parcial" o "no cumplido", la historia **no es Done** — vuelve al ciclo.

## Conexión con el resto del curso
- El **Auditor** (agente de pruebas independiente) verifica el DoD, no el mismo agente que construyó.
- El tablero (`board_sync.py`) refleja como Done **solo** lo que tiene evidencia (RED→GREEN + AUDIT PASS).
- "Los tests pasan" es una precondición, nunca la prueba final del DoD.
