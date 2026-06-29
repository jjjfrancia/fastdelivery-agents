# FastDelivery Agents — Caso práctico (CortexGovernor™ Academy · powered by DiscoveryFast)

Sistema de agentes (Coordinador + Especializados) que atiende consultas de clientes de **FastDelivery**:
estado de pedidos, preguntas de menú y reembolsos — con **trazabilidad**, **control humano (HITL)** y **pruebas por capas**.

> Repositorio de aprendizaje del curso **"Scrum para desarrollar Agentes IA"**.
> Datos de ejemplo incluidos para que corra de inmediato; reemplázalos por tus fuentes reales.

## Arquitectura

```
Usuario → Coordinador (clasifica intención y rutea)
              ├── Agente Pedidos     → tool: get_order_status   (API de pedidos)
              ├── Agente Menú        → tool: search_menu        (RAG sobre catálogo)
              └── Agente Reembolsos  → tool: apply_refund       (política + HITL > S/100)
```

- **Coordinador (Harness):** ve todo, decide qué agente actúa y cuándo detenerse.
- **Especializados:** resuelven un dominio limitado con su herramienta.
- **Guardrail clave:** un reembolso mayor a **S/100** nunca se aprueba solo → `needs_human_approval`.

## Estructura

```
fastdelivery-agents/
├── README.md
├── requirements.txt
├── .env.example            # ANTHROPIC_API_KEY=...
├── .gitignore
├── specs/SPEC.md           # contrato global + por agente (acceptance)
├── prompts/                # un system prompt POR agente
│   ├── coordinator.txt
│   ├── pedidos.txt
│   ├── menu.txt
│   └── reembolsos.txt
├── data/                   # datos de ejemplo (reemplazables)
│   ├── orders.json
│   └── catalog.json
├── src/
│   ├── tools.py            # get_order_status, search_menu, apply_refund
│   ├── agents.py           # cada especializado (prompt + tool + redacción)
│   ├── coordinator.py      # clasifica intención y rutea
│   └── main.py             # CLI: hace una pregunta y responde
├── tests/                  # las 3 zonas del TDD
│   ├── test_unit.py        # ① unitaria  (lógica pura, sin red)
│   ├── test_e2e.py         # ② funcional (flujo; requiere API key)
│   └── test_integration.py # ③ integral  (tools reales + HITL)
└── .github/workflows/ci.yml
```

## Ejecutar en local

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # y coloca tu ANTHROPIC_API_KEY
python -m src.main "¿dónde está mi pedido A1001?"
python -m src.main "¿tienen pizza hawaiana?"
python -m src.main "quiero un reembolso de 40 soles del pedido A1002"
```

Sin API key, el Coordinador usa un clasificador por palabras clave y las herramientas funcionan igual
(las pruebas unitarias e integrales corren offline; las e2e con LLM se omiten si no hay key).

## Pruebas (las 3 zonas)

```bash
pytest -q                       # corre las 3 zonas
pytest tests/test_unit.py -q    # ① unitaria
pytest tests/test_integration.py -q  # ③ integral (HITL incluido)
```

## Publicar en GitHub

```bash
git init && git add . && git commit -m "feat: FastDelivery agents (caso práctico)"
gh repo create fastdelivery-agents --public --source=. --push
# o manual:
# git remote add origin https://github.com/<usuario>/fastdelivery-agents.git
# git push -u origin main
```

El workflow `.github/workflows/ci.yml` corre `pytest` en cada push.

## Definition of Done (capstone)

- [ ] Las 3 zonas en verde (unitaria, funcional, integral).
- [ ] HITL activo para reembolsos > S/100.
- [ ] Cada respuesta cita su fuente (pedido/menú/política).
- [ ] Latencia objetivo < 5 s; costo por consulta acotado.
- [ ] Aprobación explícita del dueño del producto.

---
CortexGovernor™ Academy · powered by DiscoveryFast

## Activar CI
Este repo incluye `ci.example.yml`. Para activar GitHub Actions, muévelo a `.github/workflows/ci.yml` (requiere un token con scope `workflow`) o créalo desde la web de GitHub con ese contenido.

## Segundo ejemplo: Inmobiliaria
Ver `docs/EJEMPLO_INMOBILIARIA.md` — lectura completa Planning → Spec → TDD con un agente de inmobiliaria (contratos, prompt, tool, 6 tests, ruteo).
