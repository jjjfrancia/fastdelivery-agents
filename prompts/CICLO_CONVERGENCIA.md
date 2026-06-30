# Prompt — Genera una prueba y córrela (un Ciclo de Convergencia con TDD)

Copia este prompt y pégalo en tu agente de IA (por ejemplo **Claude Code**) **dentro de la
carpeta del proyecto** `fastdelivery-agents`. Sirve para que el agente **cree una prueba que
primero falla (RED), luego implemente el código hasta que la prueba pase (GREEN)** — el ciclo
que el curso llama *Ciclo de Convergencia*.

> Antes de empezar: ten el proyecto instalado (`python -m pip install -r requirements.txt`)
> y las herramientas de reporte (`python -m pip install pytest pytest-cov pytest-html`).

---

## PROMPT (cópialo tal cual y cambia lo que está entre ⟨corchetes⟩)

```
Trabaja en este proyecto FastDelivery usando TDD estricto (RED → GREEN → REFACTOR).
NO escribas código de producción antes que su prueba.

Quiero esta nueva capacidad:
⟨describe en una frase qué debe hacer — ejemplo:
"una función estimar_tiempo(order_id) en src/tools.py que devuelva el ETA del pedido,
o None si el pedido no existe"⟩

Sigue estos pasos y muéstrame cada uno:

1. RED — Escribe PRIMERO la prueba en tests/ (usa pytest). La prueba debe describir el
   comportamiento esperado con casos concretos (incluye al menos un caso normal y un caso
   límite/erróneo). Córrela con `python -m pytest -q` y muéstrame que FALLA (rojo). Eso prueba
   que la prueba realmente verifica algo.

2. GREEN — Ahora implementa el código mínimo para que esa prueba pase. Córrela de nuevo con
   `python -m pytest -q` y muéstrame que PASA (verde). No agregues nada que la prueba no exija.

3. REFACTOR — Si el código quedó feo o repetido, límpialo SIN cambiar el comportamiento, y
   vuelve a correr las pruebas para confirmar que siguen en verde.

4. EVIDENCIA — Corre la cobertura: `python -m pytest --cov=src --cov-report=term` y dime el %
   total y si tu código nuevo quedó cubierto.

Reglas:
- Una prueba a la vez. Primero falla, luego pasa.
- No toques pruebas existentes para "hacerlas pasar". Si una se rompe, es un hallazgo real.
- No declares nada como "listo" sin mostrarme la prueba en verde y la cobertura.
```

---

## Después de que el agente termine — verifícalo TÚ (no le creas, compruébalo)

```bash
python -m pytest -q                         # todas las pruebas en verde
python -m pytest --cov=src --cov-report=html # genera htmlcov/index.html (cobertura)
python board_sync.py                         # actualiza el tablero SPRINT_BOARD.html
```

- Abre **htmlcov/index.html** → mira el % de cobertura y qué líneas nuevas quedaron probadas.
- Abre **SPRINT_BOARD.html** → tu nueva capacidad debe aparecer como evidencia real, no como
  una afirmación. **Eso es un Ciclo de Convergencia completado.**

> Regla de oro: "los tests pasan" NO es la prueba final. La prueba es la **prueba en verde +
> la cobertura + el tablero** que cualquiera puede abrir y revisar. Esa es la transparencia.
