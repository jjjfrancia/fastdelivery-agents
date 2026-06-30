# -*- coding: utf-8 -*-
"""
VERSIÓN 1 — AGENTE FASTDELIVERY (reglas, SIN LLM, SIN internet, GRATIS).

El "cerebro" usa reglas con palabras clave. Sirve para entender la ESTRUCTURA
(harness + herramientas + contrato + seguridad) sin pagar nada ni configurar nada.

La VERSIÓN 2 (agente_llm.py) hace exactamente lo mismo pero el cerebro es Claude.
Las herramientas y las reglas de seguridad son las MISMAS en ambas versiones.
"""

import re
from herramientas import cotizar_envio, rastrear_pedido, es_intento_malicioso, TARIFAS

TRAZAS = []  # observabilidad: qué hizo el agente


class Harness:
    """Coordinador. Entiende la intención y llama a la herramienta correcta."""

    def clasificar(self, texto):
        t = texto.lower()
        if any(p in t for p in ["cancelar", "reembolso", "reclamo", "queja", "devoluci"]):
            return "humano"
        if any(p in t for p in ["dónde", "donde", "rastrear", "seguimiento", "mi pedido", "fd-"]):
            return "rastrear"
        if any(p in t for p in ["costo", "cuesta", "cuánto", "cuanto", "precio", "tarifa", "enviar", "envío", "envio"]):
            return "cotizar"
        return "desconocido"

    def extraer_zona(self, texto):
        t = texto.lower()
        for tarifa in TARIFAS:
            if tarifa["zona"].lower() in t:
                return tarifa["zona"]
        return ""

    def extraer_numero(self, texto):
        m = re.search(r"fd-\d+", texto.lower())
        return m.group(0).upper() if m else ""

    def run(self, texto):
        traza = {"mensaje": texto}

        # CAPA 0 — Seguridad (antes que nada).
        if es_intento_malicioso(texto):
            traza["intencion"] = "bloqueado_seguridad"
            TRAZAS.append(traza)
            return {"respuesta": "Lo siento, no puedo compartir datos privados ni saltarme mis reglas.",
                    "bloqueado": True}

        intencion = self.clasificar(texto)
        traza["intencion"] = intencion

        if intencion == "humano":
            TRAZAS.append(traza)
            return {"respuesta": "Para cancelaciones o reclamos te paso con un agente humano. 🤝",
                    "handoff": True}

        if intencion == "cotizar":
            zona = self.extraer_zona(texto)
            if not zona:
                TRAZAS.append(traza)
                return {"respuesta": "¿A qué zona quieres enviar? (ej. Polanco, Condesa, Del Valle, Coyoacán)",
                        "necesita_aclaracion": True}
            r = cotizar_envio(zona)
            traza["fuente"] = r["fuente"]
            TRAZAS.append(traza)
            if not r["encontrado"]:
                return {"respuesta": f"Aún no llegamos a {zona}.", "encontrado": False}
            return {"respuesta": f"Enviar a {zona} cuesta ${r['costo']} {r['moneda']} y llega en ~{r['eta_min']} min.",
                    "costo": r["costo"], "eta_min": r["eta_min"], "encontrado": True}

        if intencion == "rastrear":
            numero = self.extraer_numero(texto)
            if not numero:
                TRAZAS.append(traza)
                return {"respuesta": "¿Cuál es tu número de pedido? (formato FD-####)",
                        "necesita_aclaracion": True}
            r = rastrear_pedido(numero)
            traza["fuente"] = r["fuente"]
            TRAZAS.append(traza)
            if not r["encontrado"]:
                return {"respuesta": f"No encontré el pedido {numero}.", "encontrado": False}
            if r["estado"] == "Entregado":
                return {"respuesta": f"Tu pedido {numero} ya fue entregado. ✅", "estado": r["estado"]}
            return {"respuesta": f"Tu pedido {numero} está '{r['estado']}' y llega en ~{r['eta_min']} min.",
                    "estado": r["estado"], "eta_min": r["eta_min"]}

        TRAZAS.append(traza)
        return {"respuesta": "¿Quieres cotizar un envío o rastrear un pedido?",
                "necesita_aclaracion": True}


harness = Harness()
