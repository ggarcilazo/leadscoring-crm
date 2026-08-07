# Despliegue en Hugging Face Spaces (gratis, sin tarjeta)

Guía paso a paso para publicar el backend FastAPI del Rol 2 en la nube y
conectarlo con Odoo Online + el webhook n8n del compañero.

## Arquitectura

```
Formulario demo (GitHub Pages)                    n8n (Oracle)
        │                                               │
        ▼                                               ▼
    https://consigueventas.duckdns.org  ────────►  Webhook - Lead Intake
                                                        │ (Groq clasifica)
                                                        ▼
                                    Code - Normalizar (presupuesto_estimado → presupuesto)
                                                        │
                                    ┌───────────────────┴───────────────────┐
                                    ▼                                       ▼
                            Respond to Webhook                   HTTP Request - Enviar a Backend
                                                                        │
                                                                        ▼
                                                        https://<tu-usuario>-<tu-space>.hf.space/leads
                                                                        │ (FastAPI en HF)
                                                                        ▼
                                                        Odoo Online (CRM, XML-RPC) → crm.lead
```

## Paso 1 — Cuenta y Space en Hugging Face

1. Crea cuenta gratis en https://huggingface.co/join (no pide tarjeta).
2. Ve a https://huggingface.co/new-space
   - **Space name**: `leadscoring-backend` (o el que prefieras).
   - **License**: `MIT` (o Apache-2.0).
   - **SDK**: `Docker`.
   - **Hardware**: `CPU basic · 2 vCPU · 16GB · FREE`.
   - **Space storage**: mantener `Ephemeral` (el backend es stateless; no
     guarda datos en disco).
   - Clic en **Create Space**.

## Paso 2 — Subir el código del Space

El Space es un repo Git. La carpeta `hf-space/` de este proyecto ya contiene
todo lo necesario (`Dockerfile`, `README.md` con `sdk: docker`, código del
backend). Sube su contenido:

```bash
cd hf-space

git init
git add .
git commit -m "Backend Lead Scoring para HF"

# Agrega el repo remoto que te da HF (Settings → o clona primero):
# La forma más simple: en la página del Space, "Files → Add file", o:
git remote add origin https://huggingface.co/spaces/<tu-usuario>/<tu-space>
git push -u origin main
```

HF detecta el `Dockerfile`, hace build automático y en unos minutos deja el
Space **Running**. Verás logs del build en la pestaña **Logs**.
La app quedará en: `https://<tu-usuario>-<tu-space>.hf.space`

## Paso 3 — Configurar las variables (Settings → Variables and Secrets)

En la página del Space → **Settings** → **Variables and secrets** → *New secret*
(añadir las 4; marcar como secret las que tengan valor sensible):

| Variable        | Valor                                       |
| --------------- | ------------------------------------------- |
| `ODOO_URL`      | URL de tu Odoo (ver Paso 4)                 |
| `ODOO_DB`       | Nombre de la base de datos                  |
| `ODOO_USERNAME` | Usuario Odoo (normalmente `admin`)          |
| `ODOO_API_KEY`  | API Key generada en Odoo                    |

Tras guardarlas, haz *Restart* del Space (Settings → Danger zone → Restart).

## Paso 4 — Odoo Online (trial, sin tarjeta)

1. Crea cuenta gratuita en https://www.odoo.com/trial (elegir apps:
   **CRM**; al final pide "Start my free trial"). Sin tarjeta.
2. Anota tu URL de base: `https://<tu-nombre>.odoo.com` y el nombre de la
   base de datos (lo muestra en la lista de bases de tu cuenta).
3. Instala el módulo **CRM** si no venía preactivado (Apps → CRM → Activate).
4. Genera la **API Key**:
   - Clic en tu avatar (arriba a la derecha) → **My Profile** → **Account
     Security** → **API Keys** → *New API Key*.
   - Copia la clave (solo se muestra una vez).
5. Esa información va a las variables del Paso 3:
   - `ODOO_URL=https://<tu-nombre>.odoo.com`
   - `ODOO_DB=<tu-db>`
   - `ODOO_USERNAME=admin`
   - `ODOO_API_KEY=<clave-copiada>`

## Paso 5 — Verificar el backend

Prueba la URL pública (debe responder `{"status":"ok"}`):

```
GET https://<tu-usuario>-<tu-space>.hf.space/health
```

## Paso 6 — Apuntar el webhook n8n al backend en la nube

En `n8n-workflows/lead-intake.json`, nodo **HTTP Request - Enviar a Backend**,
cambiar la URL de `http://localhost:8000/leads` a:

```
https://<tu-usuario>-<tu-space>.hf.space/leads
```

Reimporta/actualiza el workflow en tu n8n (Oracle) y guarda.

## Paso 7 — Prueba end-to-end

1. Abre la demo: https://ggarcilazo.github.io/leadscoring-crm/
2. Envía un lead de prueba.
3. En n8n verás la ejecución con la llamada al backend en verde.
4. En Odoo → **CRM** → *Oportunidades*, debería aparecer la oportunidad con
   prioridad, presupuesto y etiquetas.

## Notas y límites del free tier

- El Space free **se duerme tras ~48 h sin tráfico** y despierta con el primer
  request (arranque en frío 30–90 s). Si n8n envía justo al dormirse, puede
  fallar el primer intento; el nodo tiene `retryOnFail` si lo activas.
- El backend no guarda datos (solo los reenvía a Odoo), por eso el disco
  efímero no es un problema.
- Odoo Online trial tiene vigencia (~15 días). Al vencer, se puede migrar el
  `ODOO_URL` a cualquier otro Odoo (otro trial, Odoo local con túnel, etc.)
  sin tocar el código.
