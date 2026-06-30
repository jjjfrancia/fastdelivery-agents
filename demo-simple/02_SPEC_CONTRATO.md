# 2️⃣ SPEC MÍNIMO + CONTRATO — Fastdelivery  (Secciones 2 y 4 de la lámina)

> El "contrato" es lo más importante: define EXACTAMENTE qué entra y qué sale
> de cada agente. Es como el menú de un restaurante: pides así, te entregan así.

## Arquitectura (Sección 2)

```
        CLIENTE
           │  escribe un mensaje en español
           ▼
   ┌─────────────────┐
   │  HARNESS         │  ← Coordinador. Entiende la intención y reparte el trabajo.
   │  (Coordinador)   │     (en la versión LLM, este "cerebro" es Claude)
   └───────┬─────────┘
           │
     ┌─────┴───────────────┐
     ▼                     ▼
┌──────────────┐    ┌──────────────┐
│ Herramienta  │    │ Herramienta  │
│ COTIZAR      │    │ RASTREAR     │   ← Tools. Cada una hace UNA cosa y dice la VERDAD.
└──────────────┘    └──────────────┘
```

## Contrato de la herramienta COTIZAR

**Recibe (input):**
```json
{ "zona": "Polanco" }
```
**Devuelve SIEMPRE (output):**
```json
{ "encontrado": true, "costo": 49, "moneda": "MXN", "eta_min": 35, "fuente": "tarifas.json" }
```

## Contrato de la herramienta RASTREAR

**Recibe (input):**
```json
{ "numero": "FD-1001" }
```
**Devuelve SIEMPRE (output):**
```json
{ "encontrado": true, "estado": "En camino", "eta_min": 12, "fuente": "pedidos.json" }
```
> La clave `"fuente"` es el *grounding*: prueba de dónde salió el dato.
> Regla de oro: si no está en los datos, `encontrado = false`. NUNCA se inventan precios ni estados.

## Reglas del sistema (lo que el agente tiene PROHIBIDO)

1. NUNCA inventar un costo, un tiempo o un estado de pedido.
2. NUNCA revelar el teléfono ni los datos del repartidor (PII).
3. Si el cliente quiere cancelar o reclamar → pasar a un humano (handoff).

## Reglas de ruteo (artefacto del Harness — Sección 6)

| Si el mensaje habla de… | Acción |
|-------------------------|--------|
| precio, costo, cuánto cuesta enviar, tarifa | COTIZAR |
| dónde está, rastrear, seguimiento, mi pedido, FD-#### | RASTREAR |
| cancelar, reembolso, reclamo, queja | HUMANO (handoff) |
| nada de lo anterior | pedir aclaración |
