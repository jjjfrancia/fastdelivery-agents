# Plantilla — Spec de TDD por capas para Agentes IA

> Los agentes son no deterministas: las pruebas son lo que hace seguro su comportamiento.
> Ciclo por capa: **ROJO** (test que falla, con salida de runner) → **VERDE** (código mínimo) → **REFACTOR**.
> Una capa sin evidencia de runner = NO hecha.

## 0. Bajo prueba
**Funcionalidad:** <qué método/endpoint/flujo>
**Spec / contrato de referencia:** <enlace al SPEC>

## 1. Capas de prueba (define al menos una por capa que aplique)

| Capa | Qué prueba | Caso(s) | Datos / fixtures | Evidencia esperada |
|------|-----------|---------|------------------|--------------------|
| **Unit** | lógica pura aislada | <...> | <...> | runner PASS + cobertura |
| **Contract** | esquema entrada/salida de la tool | <...> | <...> | valida/rechaza por schema |
| **Tool / API** | la herramienta contra su dependencia | <...> | <...> | resultado correcto + error manejado |
| **Prompt & Eval** | calidad de respuesta (golden set, LLM-as-judge) | <...> | dataset dorado | score ≥ umbral |
| **Safety** | guardrails (HITL, jailbreak, PII) | <...> | <...> | bloquea lo prohibido |
| **End-to-End** | flujo completo contra la app viva | <...> | <...> | status 2xx + salida real |

## 2. Ciclo RED → GREEN → REFACTOR (por caso)
| Caso | RED (salida del runner que falla) | GREEN (salida que pasa) | REFACTOR (re-corrido en verde) |
|------|-----------------------------------|-------------------------|--------------------------------|
| <caso 1> | <pegar salida> | <pegar salida> | <pegar salida> |

> El RED se califica igual de estricto que el GREEN: un RED sin salida de runner es **rojo sembrado** (no cuenta).

## 3. Métricas de calidad (objetivo)
Pass rate <≥X%> · cobertura líneas/branches <X%> · grounding/precisión <X> · latencia <Xs> · costo <X> · hallazgos de seguridad <0 críticos>

## 4. Suite de regresión
- [ ] Tests versionados junto al prompt y la tool
- [ ] Corren en CI en cada push
- [ ] Dataset de evaluación versionado

## 5. Definition of Done de pruebas
- [ ] Cada capa aplicable en verde-real con evidencia de runner
- [ ] RED previo al GREEN registrado
- [ ] Cobertura dentro del objetivo
- [ ] Sin guardrail en rojo
