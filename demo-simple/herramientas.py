# -*- coding: utf-8 -*-
"""
HERRAMIENTAS (tools) de Fastdelivery — Sección 4: "Tool calling / permisos".

Estas funciones son la ÚNICA fuente de verdad. Tanto el agente de reglas
(agente.py) como el agente con LLM (agente_llm.py) las usan. Así garantizamos
que el LLM NUNCA inventa precios ni estados: solo puede decir lo que estas
funciones devuelven.
"""

import json
import os

RUTA = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(RUTA, "tarifas.json"), encoding="utf-8") as f:
    TARIFAS = json.load(f)

with open(os.path.join(RUTA, "pedidos.json"), encoding="utf-8") as f:
    PEDIDOS = json.load(f)


def cotizar_envio(zona):
    """SOLO LECTURA. Devuelve costo y tiempo estimado de una zona."""
    for t in TARIFAS:
        if t["zona"].lower() == zona.lower():
            return {
                "encontrado": True,
                "costo": t["costo"],
                "moneda": t["moneda"],
                "eta_min": t["eta_min"],
                "fuente": "tarifas.json",
            }
    return {"encontrado": False, "fuente": "tarifas.json"}


def rastrear_pedido(numero):
    """SOLO LECTURA. Devuelve el estado de un pedido.
    Importante: NO devuelve el telefono_repartidor (eso es PII protegida)."""
    for p in PEDIDOS:
        if p["numero"].lower() == numero.lower():
            return {
                "encontrado": True,
                "estado": p["estado"],
                "eta_min": p["eta_min"],
                "fuente": "pedidos.json",
            }
    return {"encontrado": False, "fuente": "pedidos.json"}


def es_intento_malicioso(texto):
    """Guarda de seguridad — Sección 5: 'Safety Tests'.
    Detecta intentos de robar datos privados o saltarse las reglas."""
    t = texto.lower()
    señales = ["ignora", "olvida tus reglas", "olvida tus instrucciones",
               "telefono del repartidor", "teléfono del repartidor",
               "datos del repartidor", "numero del repartidor", "número del repartidor"]
    return any(s in t for s in señales)
