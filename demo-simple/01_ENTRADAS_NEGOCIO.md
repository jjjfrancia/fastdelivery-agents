# 1️⃣ ENTRADAS DEL NEGOCIO — Fastdelivery  (Sección 1 de la lámina)

> Esto NO es código. Son las decisiones que se toman en una reunión, ANTES de programar.
> Cualquier persona del negocio puede llenar esta hoja.

| Campo | Decisión |
|-------|----------|
| **Producto** | **Fastdelivery** — app de entregas a domicilio (comida y paquetería). |
| **Product Goal** | Atender al cliente en menos de 1 minuto: cotizar un envío y rastrear su pedido sin operador humano. |
| **Usuario** | El cliente que pide un envío o quiere saber dónde está su pedido. |
| **Stakeholders** | Gerente de operaciones (decide) · Agente de soporte (valida casos raros). |
| **Caso de uso #1** | Cotizar un envío (¿cuánto cuesta y en cuánto llega?). |
| **Caso de uso #2** | Rastrear un pedido (¿dónde está mi pedido?). |
| **Valor esperado** | -40% de carga en soporte humano. Métrica: % de consultas resueltas por el agente. |
| **Restricción (compliance)** | NUNCA revelar el teléfono ni los datos personales del repartidor (eso es PII protegida). |
| **Definition of Ready** | Tener listas las tarifas por zona (`tarifas.json`) y los pedidos (`pedidos.json`). ✅ |

---

## Qué quedó DENTRO y FUERA del Sprint 1

- ✅ DENTRO: Cotizar envío + Rastrear pedido + bloqueo de datos privados.
- ⛔ FUERA (para el Sprint 2): pagos, cancelaciones, reasignar repartidor, WhatsApp.
