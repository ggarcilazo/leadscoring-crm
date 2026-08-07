---
title: Lead Scoring Backend
emoji: 🎯
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Lead Scoring Backend

Backend FastAPI del Rol 2 que recibe leads del webhook n8n, los limpia y crea
la oportunidad en Odoo (CRM) vía XML-RPC.

## Endpoints

- `GET /health` — estado del servicio.
- `POST /leads` — recibe un lead y lo guarda en Odoo. Ver esquema abajo.

## Variables de entorno (Settings → Variables and Secrets)

| Variable        | Ejemplo                          | Descripción                       |
| --------------- | -------------------------------- | --------------------------------- |
| `ODOO_URL`      | `https://xxxx.odoo.com`          | URL del Odoo (local u Online)     |
| `ODOO_DB`       | `leadscoring`                    | Base de datos de Odoo             |
| `ODOO_USERNAME` | `admin`                          | Usuario con acceso al CRM         |
| `ODOO_API_KEY`  | clave generada en Odoo (preferible) o contraseña | Credencial XML-RPC |

> Odoo Online: genera la API Key en tu perfil (`Preferencias → Cuenta → API Keys`).

## Esquema de `POST /leads`

```json
{
  "nombre": "Juan Pérez",
  "empresa": "Corporación Andina S.A.C.",
  "sector": "Manufactura",
  "email": "juan@empresa.com",
  "telefono": "+51999888777",
  "resumen_ejecutivo": "Cliente interesado en automatización de ventas.",
  "urgencia": "alta",
  "presupuesto": "25000",
  "tags": ["automatizacion", "crm"]
}
```
