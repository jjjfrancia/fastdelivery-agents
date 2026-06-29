# Plantilla — Sprint Planning para Agentes IA

> Rellena cada sección. Un Sprint sin Goal no empieza. Reemplaza el texto entre `<...>`.

## 1. Sprint Goal (la hipótesis de valor)
**Goal:** <qué necesita el usuario>
**Por qué importa:** <qué valor valida este Sprint>

## 2. Entradas del negocio y del producto
- **Product Goal:** <objetivo de producto>
- **Usuarios / stakeholders:** <quién>
- **Casos de uso priorizados:** <1, 2, 3>
- **Valor esperado:** <impacto / métrica>
- **Restricciones / guardrails:** <límites, seguridad, presupuesto, latencia, HITL>
- **Definition of Ready:** <qué debe existir para empezar>

## 3. Entradas técnicas del sistema de agentes
**Coordinador (Harness):** objetivo · reglas de ruteo · memoria · permisos · criterios de handoff humano
**Agentes especializados (uno por fila):**

| Agente | Dominio | Herramientas / APIs | RAG / fuentes | Entrada → Salida |
|--------|---------|---------------------|---------------|------------------|
| <nombre> | <dominio> | <tools> | <fuentes> | <contrato I/O> |

## 4. Qué se discute (Definir · Discutir · Diseñar · Plantear)
- **Definir:** Goal, valor, alcance
- **Discutir:** PBIs, dependencias, riesgos
- **Diseñar:** arquitectura mínima, contratos, prompts, herramientas
- **Plantear:** plan, responsables, pruebas

## 5. Sprint Backlog (items → tareas atómicas)
| # | Item (PBI) | Tarea atómica (1 método/endpoint/migración) | Responsable | Zona(s) de prueba |
|---|-----------|---------------------------------------------|-------------|-------------------|
| 1 | <item> | <tarea> | <quién> | ①②③ |

## 6. Plan de pruebas (las 3 zonas)
- **① Unitaria:** <qué lógica>
- **② Funcional (e2e):** <qué flujo contra la app viva>
- **③ Integral:** <qué tool/API real + datos>

## 7. Definition of Done
- [ ] 3 zonas en verde-real (evidencia de runner)
- [ ] Guardrails activos (incl. HITL donde aplique)
- [ ] Respuestas citan su fuente · trazabilidad
- [ ] Dentro del SLA (latencia/costo)
- [ ] Aprobación explícita del dueño del producto

## 8. Riesgos, dependencias y capacidad
- **Riesgos:** <...>  · **Dependencias:** <...>  · **Timebox / capacidad:** <horas>
