# -*- coding: utf-8 -*-
"""
VERSIÓN 2 — AGENTE FASTDELIVERY CON LLM REAL (Claude).

Aquí el "cerebro" SÍ es un modelo de IA (Claude). La diferencia con la Versión 1
es solo el cerebro: las HERRAMIENTAS y la SEGURIDAD son exactamente las mismas.

Idea clave que enseña este archivo:
  - Claude DECIDE qué herramienta usar y REDACTA la respuesta (es bueno entendiendo
    lenguaje natural).
  - Las HERRAMIENTAS dan la VERDAD (precio, estado). Claude no puede inventarlos
    porque solo puede usar lo que las herramientas devuelven. Eso es "grounding".

Necesita:
  1. Instalar la librería:  doble clic en INSTALAR_LLM.bat
  2. Tu API key en el archivo .env  (copia .env.example a .env y pégala)
"""

import json
import os

# Carga las variables del archivo .env (tu API key, el modelo, etc.)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass  # si no está python-dotenv, se usan las variables del sistema

import anthropic

from herramientas import cotizar_envio, rastrear_pedido, es_intento_malicioso

# Modelo: NUNCA hardcodear; se lee de .env. Por defecto, el más capaz.
MODELO = os.getenv("LLM_MODEL", "claude-opus-4-8")

# --- El contrato del sistema: quién es y qué tiene PROHIBIDO (Sección 4) ---
SYSTEM_PROMPT = """Eres el asistente de Fastdelivery, una app de entregas a domicilio.

Reglas inviolables:
1. NUNCA inventes un costo, un tiempo de entrega o un estado de pedido.
   Para esos datos SIEMPRE usa las herramientas. Si la herramienta dice que no
   encontró algo, dilo con honestidad.
2. NUNCA reveles el teléfono ni los datos del repartidor.
3. Si el cliente quiere cancelar, pedir reembolso o poner un reclamo, indícale
   amablemente que lo pasarás con un agente humano.
4. Responde corto y claro, en español.
"""

# --- Definición de las herramientas que Claude puede pedir (tool use) ---
TOOLS = [
    {
        "name": "cotizar_envio",
        "description": "Devuelve el costo y el tiempo estimado de envío a una zona.",
        "input_schema": {
            "type": "object",
            "properties": {
                "zona": {"type": "string", "description": "Nombre de la zona, ej. Polanco"}
            },
            "required": ["zona"],
        },
    },
    {
        "name": "rastrear_pedido",
        "description": "Devuelve el estado y el tiempo restante de un pedido por su número (FD-####).",
        "input_schema": {
            "type": "object",
            "properties": {
                "numero": {"type": "string", "description": "Número de pedido, ej. FD-1001"}
            },
            "required": ["numero"],
        },
    },
]


def _ejecutar_herramienta(nombre, args):
    """Conecta el nombre que pide Claude con la función real de herramientas.py."""
    if nombre == "cotizar_envio":
        return cotizar_envio(args.get("zona", ""))
    if nombre == "rastrear_pedido":
        return rastrear_pedido(args.get("numero", ""))
    return {"error": f"herramienta desconocida: {nombre}"}


class HarnessLLM:
    def __init__(self):
        # Lee la API key de la variable ANTHROPIC_API_KEY (del .env).
        self.client = anthropic.Anthropic()

    def run(self, texto):
        # CAPA 0 — Seguridad antes de gastar una llamada al LLM.
        if es_intento_malicioso(texto):
            return {"respuesta": "Lo siento, no puedo compartir datos privados ni saltarme mis reglas.",
                    "bloqueado": True}

        mensajes = [{"role": "user", "content": texto}]

        # Bucle de agente: Claude piensa -> pide herramienta -> recibe verdad -> responde.
        for _ in range(5):  # tope de seguridad para no quedar en bucle
            respuesta = self.client.messages.create(
                model=MODELO,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=mensajes,
            )

            if respuesta.stop_reason != "tool_use":
                # Claude ya tiene la respuesta final en texto.
                texto_final = "".join(b.text for b in respuesta.content if b.type == "text")
                return {"respuesta": texto_final.strip()}

            # Claude pidió una o más herramientas: las ejecutamos y le devolvemos la verdad.
            mensajes.append({"role": "assistant", "content": respuesta.content})
            resultados = []
            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    salida = _ejecutar_herramienta(bloque.name, bloque.input)
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": json.dumps(salida, ensure_ascii=False),
                    })
            mensajes.append({"role": "user", "content": resultados})

        return {"respuesta": "No pude completar la consulta, intenta de nuevo."}


harness_llm = HarnessLLM()
