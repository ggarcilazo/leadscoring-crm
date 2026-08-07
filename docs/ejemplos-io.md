# Ejemplos reales de Input/Output — Flujo de Clasificación

Casos probados end-to-end contra el webhook de producción
(`n8n → Groq/Llama 3.3 → normalización`). Cada ejemplo fue ejecutado
realmente contra el flujo, no simulado.

---

## Caso 1 — Lead urgente, presupuesto alto

**Input (formulario):**
```json
{
  "nombre": "Carlos Mendoza",
  "empresa": "Constructora Andina SAC",
  "email": "carlos@constructoraandina.pe",
  "telefono": "+51987654321",
  "mensaje": "Necesitamos con urgencia una cotización para 500 metros de cableado industrial, el proyecto arranca en dos semanas y el presupuesto es alto."
}
```

**Output (clasificación de la IA):**
```json
{
  "presupuesto_estimado": "alto",
  "urgencia": "alta",
  "sector": "construcción",
  "resumen_ejecutivo": "Cotización urgente para 500 metros de cableado industrial para proyecto de la Constructora Andina SAC con inicio en dos semanas"
}
```

**Análisis:** la IA identificó correctamente la urgencia por las palabras
"con urgencia" y el plazo de dos semanas, y el presupuesto por la mención
explícita de "presupuesto es alto". El sector se infirió del nombre de la
empresa y del tipo de material (cableado industrial → construcción).

---

## Caso 2 — Lead de baja urgencia / presupuesto no especificado

_Pendiente de ejecutar y documentar. Sugerencia de mensaje de prueba:_

```json
{
  "nombre": "María Torres",
  "empresa": "Estudio Contable Torres & Asociados",
  "email": "maria@torrescontable.pe",
  "telefono": "+51912345678",
  "mensaje": "Hola, quisiera información general sobre sus servicios para más adelante, no hay apuro por ahora."
}
```

## Caso 3 — Mensaje ambiguo / poca información

_Pendiente de ejecutar y documentar. Sugerencia de mensaje de prueba:_

```json
{
  "nombre": "Jorge Ramírez",
  "empresa": "Textiles del Sur",
  "email": "jorge@textilesdelsur.pe",
  "telefono": "+51998877665",
  "mensaje": "Buenas, ¿trabajan con empresas textiles?"
}
```

---

## Cómo agregar más casos

1. Envía el POST de prueba al webhook (test o producción).
2. Copia el JSON de entrada y el JSON de salida real que devuelva.
3. Agrega un breve análisis de por qué la IA clasificó así (o si se
   equivocó — documentar errores también es valioso para el portafolio).
