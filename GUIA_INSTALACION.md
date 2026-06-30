# Guía de Requisitos e Instalación — FastDelivery Agents

Esta guía te lleva de cero a tener el proyecto **corriendo y probado**, paso a paso.
No necesitas experiencia previa. Comandos pensados para **Windows** (PowerShell).

---

## 1. Requisitos

### Software obligatorio
| Requisito | Versión | Para qué |
|-----------|---------|----------|
| **Python** | 3.9 o superior (probado en 3.14) | Ejecutar el proyecto |
| **pip** | Viene con Python | Instalar las dependencias |

### Dependencias del proyecto (se instalan en el paso 4)
| Paquete | Versión | ¿Obligatorio? |
|---------|---------|---------------|
| `anthropic` | ≥ 0.40.0 | **Solo** si quieres que un LLM (Claude) redacte las respuestas |
| `pytest` | ≥ 8.0.0 | Solo para correr las pruebas |

> 💡 **Importante:** en **modo offline** (sin clave de API) el proyecto funciona **sin instalar nada extra** — usa solo la librería estándar de Python. Las dependencias son opcionales según lo que quieras hacer.

### Opcional (solo para modo con IA)
| Requisito | Para qué |
|-----------|----------|
| **API key de Anthropic** (`ANTHROPIC_API_KEY`) | Que Claude redacte las respuestas. Sin ella, funciona igual con plantillas. |

---

## 2. Verificar que tienes Python

Abre **PowerShell** y escribe:

```powershell
python --version
```

- Si ves algo como `Python 3.14.3` → ✅ continúa al paso 3.
- Si dice "no se reconoce" → instala Python desde **https://www.python.org/downloads/**
  (al instalar, marca la casilla **"Add Python to PATH"**).

---

## 3. Ubicar / descargar el proyecto

**Ya lo tienes** en:
```
C:\Users\Joel Francia\OneDrive\Documents\SAGE\academycortexgovernor\courses\scrum-para-agentes-ia\ejemplo-fastdelivery
```

O clónalo desde GitHub:
```powershell
git clone https://github.com/jjjfrancia/fastdelivery-agents.git
cd fastdelivery-agents
```

---

## 4. Instalar las dependencias

Entra a la carpeta del proyecto y (recomendado) crea un entorno virtual:

```powershell
cd "C:\Users\Joel Francia\OneDrive\Documents\SAGE\academycortexgovernor\courses\scrum-para-agentes-ia\ejemplo-fastdelivery"

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

> Si PowerShell bloquea el `Activate.ps1`, ejecuta una vez:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a intentar.
>
> **¿Solo modo offline?** Puedes saltarte este paso — el proyecto corre sin instalar nada.

---

## 5. (Opcional) ¿DÓNDE pongo mi API key?

El key va en un **archivo llamado `.env`** que debe estar **en la carpeta del proyecto**
(la misma donde está `requirements.txt`). El código lo lee automáticamente desde ahí.

**Forma fácil (recomendada):** ejecuta `EJECUTAR.bat` → opción **2 "Configurar mi API key"** → pega tu clave. Eso crea el `.env` por ti.

**Forma manual:** en la carpeta del proyecto, crea un archivo de texto llamado exactamente **`.env`** (sin nombre, solo `.env`) y dentro escribe **una sola línea**:
```
ANTHROPIC_API_KEY=sk-ant-tu-clave-real-aqui
```
Consigue tu clave en https://console.anthropic.com → API Keys.

> ⚠️ El archivo se llama `.env` — **no** `.env.txt`. En el Bloc de notas, al guardar elige "Tipo: Todos los archivos" y nómbralo `.env`.
>
> Sin clave **no pasa nada malo**: el sistema responde con plantillas (modo offline). El key solo sirve para que Claude redacte las respuestas.

---

## 6. Ejecutar el proyecto

```powershell
python -m src.main "¿dónde está mi pedido A1001?"
python -m src.main "¿tienen pizza hawaiana?"
python -m src.main "quiero un reembolso de 40 soles del pedido A1002"
```

Deberías ver respuestas como:
```
Según el pedido A1001: tu pedido está en camino, ETA 15 min.
```

---

## 7. Correr las pruebas

```powershell
python -m pytest -q
```

> Usa `python -m pytest` (no solo `pytest`): así funciona aunque el PATH de Windows no encuentre el ejecutable.

Resultado esperado: **todas en verde** (1 omitida si no pusiste API key — es lo normal).

---

## 7.5 Ver el tablero de evidencia (board_sync)

El curso habla de `board_sync`, `SPRINT_BOARD` y `TEST_LOGS.json`. Aquí los tienes de verdad:

```powershell
python board_sync.py
```

Eso lee `TEST_LOGS.json` (la evidencia), **verifica cada archivo contra el disco** y genera **`SPRINT_BOARD.html`**. Ábrelo en el navegador (doble clic) para ver el tablero.

Verás algo así en consola:
```
[2026-06-19 23:02:04] board_sync OK - 4 filas, 1 inconsistencias detectadas
   -> src/tracking.py declarado por el agente pero NO existe en disco
```

> El tablero muestra como **Done** solo lo que tiene RED→GREEN + `audit_verdict: PASS` **y** el archivo existe. Lo que el agente "declaró" sin evidencia sale como **inconsistencia** — esa es la lección.

## 8. Solución de problemas

| Problema | Solución |
|----------|----------|
| `python no se reconoce` | Reinstala Python marcando "Add to PATH", o reinicia la terminal. |
| `No module named anthropic` | Corre `pip install -r requirements.txt` (con el entorno virtual activado). |
| `Activate.ps1 ... no se puede cargar` | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y reintenta. |
| El LLM no responde / error de clave | Revisa que `.env` tenga `ANTHROPIC_API_KEY=...` correcta. O úsalo en modo offline (sin clave). |
| `pytest no se reconoce` | Usa `python -m pytest -q` (funciona aunque el PATH no encuentre el ejecutable). Si dice "No module named pytest", corre antes `python -m pip install -r requirements.txt`. |
| Puse mi key en `.env` pero el LLM no responde / sigue en modo plantillas | Verifica: (1) el archivo se llama exactamente `.env` (no `.env.txt`), (2) está en la carpeta del proyecto, (3) la línea es `ANTHROPIC_API_KEY=sk-ant-...` sin espacios ni comillas. La forma segura es usar `EJECUTAR.bat` → opción 2. |
| `ERROR: Could not open requirements file ... No such file or directory: 'requirements.txt'` | **Estás en la carpeta equivocada.** Antes de instalar, haz `cd` a la carpeta del proyecto (la que contiene `requirements.txt`). Ver la ruta exacta en el paso 3. |

---

## Resumen rápido (copiar y pegar)

```powershell
cd "C:\Users\Joel Francia\OneDrive\Documents\SAGE\academycortexgovernor\courses\scrum-para-agentes-ia\ejemplo-fastdelivery"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env        # (opcional) y pega tu API key
python -m src.main "¿dónde está mi pedido A1001?"
python -m pytest -q
python board_sync.py          # genera y actualiza SPRINT_BOARD.html (ábrelo en el navegador)
```

---
CortexGovernor™ Academy · powered by DiscoveryFast
