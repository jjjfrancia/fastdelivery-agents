# Ejemplos — de un prompt a un sistema multi-agente (de cero a 100)

Una serie de ejemplos **corribles**, del más simple al más completo. Cada archivo
explica su teoría arriba (en el docstring) y se ejecuta solo. **Córrelos en orden.**

> Todos funcionan **sin API key** (modo demostración). Con una key en `.env`
> (`ANTHROPIC_API_KEY=...`), los ejemplos 1, 2, 6, 7 y 8 usan el modelo de verdad.

| # | Archivo | Qué aprendes | Cómo correr |
|---|---------|--------------|-------------|
| 1 | `01_prompt_simple.py` | Ejecutar un **prompt** (mandar texto, recibir texto) | `python ejemplos/01_prompt_simple.py` |
| 2 | `02_agente_simple.py` | Crear un **agente** (LLM + prompt + herramienta) | `python ejemplos/02_agente_simple.py` |
| 3 | `03_harness_simple.py` | Crear un **harness** (coordinador que rutea) | `python ejemplos/03_harness_simple.py` |
| 4 | `04_guardrails.py` | Definir **guardrails** (límites en código) | `python ejemplos/04_guardrails.py` |
| 5 | `05_harness_con_agentes.py` | El **harness llamando a los agentes** (sistema mínimo) | `python ejemplos/05_harness_con_agentes.py` |
| 6 | `06_agente_genera_pruebas.py` | Un **agente que crea las pruebas** (TDD con IA) | `python ejemplos/06_agente_genera_pruebas.py` |
| 7 | `07_agente_genera_ui.py` | Un **agente que crea una UI** en HTML | `python ejemplos/07_agente_genera_ui.py` |
| 8 | `08_todos_juntos.py` | **Todos trabajando juntos** desde un prompt | `python ejemplos/08_todos_juntos.py` |

## Antes de empezar
```bash
cd fastdelivery-agents
python -m pip install -r requirements.txt      # instala anthropic (para los que usan LLM)
```

## El recorrido
1–2 te enseñan la diferencia entre un **prompt** y un **agente**.
3–5 construyen el **harness** y le agregan **guardrails** y **agentes**.
6–7 muestran a un agente **produciendo entregables** (pruebas y UI).
8 junta todo: un sistema multi-agente que responde de punta a punta.

Cuando entiendas estos 8, abre `src/` del proyecto: es exactamente esto, ordenado
y con pruebas reales.
