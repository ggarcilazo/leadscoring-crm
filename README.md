# Lead Scoring CRM — Automatización de Leads con IA

Sistema que recibe leads desde un flujo de automatización (n8n), los clasifica
con IA (OpenAI/Gemini), limpia y valida los datos, y crea oportunidades
automáticamente en **Odoo CRM** con etiquetas de urgencia, sector y presupuesto.

> Proyecto de equipo. Este repositorio contiene la parte de **backend
> (Rol 2)**. El flujo n8n y la clasificación con IA corresponden al Rol 1.

## Arquitectura

```
n8n (Rol 1)  ──POST /leads──▶  Backend FastAPI  ──XML-RPC──▶  Odoo 17 CRM
     │                              │
     │                       [cleaning.py]          [PostgreSQL]
     └── IA clasifica ──────▶  valida y limpia
```

1. El flujo n8n recibe el lead y la IA lo clasifica (sector, urgencia, presupuesto).
2. n8n envía el JSON a `POST /leads`.
3. `cleaning.py` valida email, normaliza teléfono (E.164) y elimina HTML.
4. `odoo_client.py` crea la oportunidad en `crm.lead` con sus etiquetas.
5. Si la urgencia es `alta`, agenda una actividad de seguimiento automática.

## Estructura del repo

```
proyecto 3/
├── backend/
│   ├── main.py           # API FastAPI (POST /leads, GET /health)
│   ├── cleaning.py       # Validación y limpieza de datos
│   ├── odoo_client.py    # Cliente XML-RPC para Odoo CRM
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml    # Odoo 17 + PostgreSQL (ver manual)
├── .gitignore
└── README.md
```

## Levantar en local

### 1. Odoo 17 + PostgreSQL (Docker)

```bash
docker compose up -d
```

Abrir `http://localhost:8069`, crear la base de datos, instalar el módulo
**CRM** y generar una clave API en *Ajustes → Usuarios → tu usuario →
Seguridad de la cuenta → Nuevas claves API*.

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS
# editar .env con URL, usuario y clave API reales
uvicorn main:app --reload
```

### 3. Probar

```bash
curl -X POST http://localhost:8000/leads -H "Content-Type: application/json" -d "{\"empresa\":\"ACME SA\",\"nombre\":\"Juan\",\"email\":\"juan@acme.com\",\"telefono\":\"987654321\",\"sector\":\"Construccion\",\"urgencia\":\"alta\",\"resumen_ejecutivo\":\"Cliente interesado en CRM\"}"
```

Respuesta esperada: `{"status": "ok", "odoo_id": <id>}`

## Seguridad

- **Nunca** se suben `.env` al repositorio (está en `.gitignore`).
- Usar `.env.example` como plantilla y reemplazar las credenciales reales.
- En producción, inyectar las variables como variables de entorno del sistema,
  no como archivo.
- Antes de cada push: `git diff --staged` para verificar que no se coló ninguna clave.

## Notas

- Odoo **Community** (self-hosted) — licencia de Odoo Community (LGPL).
- Requisitos: Python 3.11+, Docker, Docker Compose.
- Las credenciales de ejemplo en `.env.example` deben reemplazarse antes de usar.
