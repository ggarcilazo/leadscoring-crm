# Lead Scoring CRM — Automatización de Leads con IA

Sistema automatizado de ingesta y calificación de leads B2B con IA,
integrado a un CRM (Odoo). Un formulario de contacto se clasifica
automáticamente por presupuesto, urgencia y sector, y crea la oportunidad
directamente en el CRM con etiquetas y prioridad asignadas por IA.

**Demo en vivo:** `docs/index.html` — desplegado en GitHub Pages, permite
probar el flujo completo desde el navegador sin necesidad de Postman/curl.

---

## Arquitectura

```

<img width="1662" height="946" alt="f4760504-c544-4961-95c9-1a039d3234fd" src="https://github.com/user-attachments/assets/9c3fc983-90cb-443e-ad10-d150b9c31779" />

```

1. El formulario envía los datos del lead a un **Webhook de n8n**.
2. n8n manda el mensaje a **Groq (Llama 3.3)**, que devuelve una
   clasificación estructurada en JSON (presupuesto, urgencia, sector,
   resumen ejecutivo).
3. n8n reenvía el lead + clasificación a un **backend en Python (FastAPI)**,
   que limpia/valida los datos (teléfono, email, texto).
4. El backend crea la oportunidad en **Odoo CRM** vía XML-RPC, con
   etiquetas automáticas y una alerta interna si la urgencia es alta.

## Stack

| Componente | Tecnología | Costo |
|---|---|---|
| Automatización | n8n (self-hosted, Docker) | $0 |
| Clasificación IA | Groq API (Llama 3.3 70B) | $0 (free tier, sin tarjeta) |
| Backend | Python + FastAPI | $0 |
| CRM | Odoo Community Edition (self-hosted, Docker) | $0 |
| Infraestructura | Oracle Cloud Always Free | $0 |
| Demo pública | HTML/CSS/JS estático en GitHub Pages | $0 |

## Estructura del repositorio

```
leadscoring-crm/
├── n8n-workflows/
│   ├── lead-intake.json     # Flujo exportado de n8n
│   └── prompt-schema.md      # Prompt y schema de clasificación documentados
├── backend/
│   ├── main.py                # Endpoint FastAPI que recibe el lead clasificado
│   ├── cleaning.py            # Validación y limpieza de datos
│   ├── odoo_client.py         # Integración con Odoo vía XML-RPC
│   └── requirements.txt
├── docs/
│   ├── index.html             # Demo interactiva (GitHub Pages)
│   └── ejemplos-io.md         # Casos reales de input/output probados
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Instalación local

Requisitos: Docker y Docker Compose.

```bash
git clone <url-del-repo>
cd leadscoring-crm
cp .env.example .env   # completa con tus propias credenciales
docker compose up -d
```

Esto levanta n8n (`:5678`) y Odoo (`:8069`) localmente. Importa el flujo
de `n8n-workflows/lead-intake.json` desde la UI de n8n, y configura tu
propia credencial de Groq (no se incluye ninguna key en el repo).

## Seguridad

- Ninguna credencial vive en el código: todo pasa por variables de entorno
  (`.env`, nunca versionado — ver `.gitignore`).
- El webhook de producción incluye un path no adivinable y un honeypot
  anti-bot en el formulario de demo.
- La demo pública (`docs/index.html`) limita los envíos por sesión de
  navegador como medida básica anti-saturación; la protección real de
  tasa de envíos vive en el servidor (nginx + validaciones en n8n).
- Cada componente corre en su propia credencial/API key, sin compartir
  secretos entre servicios.

## Autoría

Proyecto de portafolio desarrollado en equipo:
- **Automatización & IA** (n8n, integración con Groq/Llama): [Giovanni Joaquin Garcilazo Lopez]
- **Backend & CRM** (Python, Odoo, seguridad del repo): [Hector Jose Caballero Babilonia]
