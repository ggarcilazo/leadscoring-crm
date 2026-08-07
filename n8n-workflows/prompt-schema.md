# Prompt & Schema de Clasificación — Nodo IA

## Modelo usado

`llama-3.3-70b-versatile` vía **Groq API** (`https://api.groq.com/openai/v1/chat/completions`,
compatible con el formato de OpenAI Chat Completions).

> Nota: el diseño original contemplaba Gemini API, pero se migró a Groq porque
> el free tier de Gemini pasó a requerir una cuenta de facturación vinculada
> (prepago) para responder, incluso dentro de su cuota gratuita. Groq no
> requiere tarjeta para su free tier.

## Prompt (system/user combinado en un solo mensaje)

```
Analiza este mensaje de un formulario de contacto B2B y clasifícalo.
Responde SOLO con un JSON válido, sin texto adicional, con este formato
exacto: {"presupuesto_estimado": "bajo|medio|alto|no_especificado",
"urgencia": "baja|media|alta", "sector": "string", "resumen_ejecutivo":
"string"}. Mensaje: {mensaje}. Empresa: {empresa}.
```

Se fuerza el modo JSON con `response_format: { "type": "json_object" }`,
que en la API de Groq garantiza una salida parseable sin markdown ni texto
envolvente (equivalente al `responseSchema` de Gemini, pero sin schema
tipado nativo — por eso el formato exacto se especifica en el prompt).

## Schema de salida esperado

| Campo | Tipo | Valores posibles | Descripción |
|---|---|---|---|
| `presupuesto_estimado` | string (enum) | `bajo`, `medio`, `alto`, `no_especificado` | Presupuesto inferido del mensaje del lead |
| `urgencia` | string (enum) | `baja`, `media`, `alta` | Urgencia del pedido, según lenguaje y plazos mencionados |
| `sector` | string (libre) | — | Industria/sector del prospecto, inferido del mensaje/empresa |
| `resumen_ejecutivo` | string (libre) | — | Resumen de 1-2 líneas para que el vendedor lo lea rápido |

## Por qué estos 4 campos

Estos son los campos que consume directamente el backend (Odoo CRM) para:
- Etiquetar la oportunidad (`urgencia`, `sector`).
- Priorizar el registro (`presupuesto_estimado` + `urgencia` → prioridad interna).
- Poblar la descripción inicial de la oportunidad sin que el vendedor tenga
  que releer el mensaje original completo (`resumen_ejecutivo`).

## Manejo de errores del modelo

Si el modelo devuelve un JSON malformado o campos fuera del enum esperado,
el nodo "Code - Normalizar" no valida estrictamente el schema (mejora
pendiente: agregar validación con fallback a valores por defecto en vez de
que el flujo falle completo).
