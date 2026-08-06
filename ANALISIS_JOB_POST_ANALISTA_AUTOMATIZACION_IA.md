# Análisis de Oferta Laboral
## Analista de Automatización y Soporte / IA — Grupo Clave

> Fuente: Job post publicado (Lima, Lima — Grupo Clave)
> Modalidad: 100% remoto, con al menos 4 h de solapamiento con horario de Madrid (UTC+1/UTC+2)

---

## 1. Resumen de la oferta

| Campo | Detalle |
|---|---|
| Puesto | Analista de Automatización y Soporte / IA |
| Empresa | Grupo Clave (sector Industrial y Construcción) |
| Ubicación | Lima, Perú (trabajo remoto para empresa de España) |
| Modalidad | 100% remoto |
| Solapamiento | Mínimo 4 h con horario de Madrid |
| Valoración del post | 3.7 / 5 estrellas |
| Nivel | Egresado / Bachiller + ~3 años de experiencia |

---

## 2. Responsabilidades principales

1. **Automatización low-code / no-code**
   - Diseñar y gestionar flujos en **Make, Zapier o n8n** (webhooks, conectores, alertas).
2. **Integración de IA**
   - Integrar **APIs de IA (OpenAI)** para clasificación y extracción de datos.
3. **Odoo (ERP)**
   - Configurar y personalizar módulos: **CRM, Inventario, Proyectos**.
   - Crear automatizaciones internas dentro de Odoo.
4. **Scripting**
   - Desarrollar scripts en **Python y JavaScript** para automatizar procesos.
5. **Bases de datos**
   - Consultas básicas en **PostgreSQL** (joins, filtros, agregaciones).
   - Consumir **APIs REST** (autenticación y consumo de datos).
6. **Visualización de datos**
   - Tableros básicos en **Power BI o Metabase**.
7. **DevOps básico**
   - Uso de **Git** (control de versiones) y **Docker** (pruebas locales).
8. **Comunicación y mejora continua**
   - Documentar procesos y colaborar con usuarios de negocio proponiendo mejoras.

---

## 3. Requisitos exigidos

### Formación
- Egresado o Bachiller en: Ingeniería en Sistemas, Informática, Software, Automatización, Ciencias de la Computación o carreras técnicas afines.

### Experiencia
- **3 años o más** montando flujos en Make, Zapier o n8n (webhooks, conectores, alertas y reportes automáticos).

### Habilidades técnicas
| Área | Herramientas / tecnología |
|---|---|
| Automatización | Make, Zapier, n8n |
| IA | OpenAI API (clasificación, extracción de datos) |
| ERP | Odoo (CRM, Inventario, Proyectos) |
| Programación | Python, JavaScript (scripting) |
| Backend / APIs | REST, autenticación, consumo de datos |
| BD | PostgreSQL (joins, filtros, agregaciones) |
| BI | Power BI o Metabase |
| DevOps | Git, Docker (entorno local) |

### Certificaciones (deseables)
- Cursos/certificaciones en Odoo, Python, JavaScript, Docker, APIs REST, Power BI, etc.

---

## 4. Análisis por bloques de competencias

### A. Automatización de flujos (Make / Zapier / n8n) — NÚCLEO DEL PUESTO
- Es la competencia con mayor peso (mencionada como requisito de 3+ años).
- Implica: webhooks entrantes/salientes, conectores (Gmail, Sheets, Telegram, Slack, CRMs), rutas condicionales, manejo de errores, y envío de alertas/reportes.
- **n8n** es el más cercano al desarrollo (self-hosted, se ejecuta con Docker), encaja con el resto del stack.

### B. Integración de IA (OpenAI)
- Casos de uso típicos: clasificación de documentos/tickets, extracción de campos desde texto o PDFs (NER), generación de resúmenes.
- Patrón de integración: trigger (webhook o conector) → llamada a `/v1/chat/completions` o `/v1/embeddings` → post-procesamiento → acción (crear registro en Odoo, responder, alertar).

### C. Odoo
- Personalización de módulos estándar + automatizaciones (reglas de automatización, acciones del servidor, flujos con "Odoo Studio").
- Requiere entender el modelo de datos de Odoo (res.partner, crm.lead, product.product, project.project).

### D. Programación (Python / JavaScript)
- Python: scripting de ETL, cliente HTTP (`requests`), manejo de JSON, agenda de tareas (APScheduler/cron).
- JavaScript: Node.js para n8n (nodos custom / Function nodes), scripts en el front de Odoo (Owl/JS).

### E. Datos y reportes
- PostgreSQL: SELECT con JOINs, WHERE, GROUP BY, agregaciones.
- Power BI / Metabase: conectarse a la BD, crear tableros básicos (KPIs, filtros, gráficos).

### F. Entorno de trabajo
- Git: ramas, commits, PRs, .gitignore.
- Docker: levantar Postgres, n8n, Metabase, Odoo en contenedores para pruebas locales.

---

## 5. Stack técnico completo del puesto

```
[Flujos: Make / Zapier / n8n]  →  [OpenAI API]  →  [Odoo]  →  [PostgreSQL]
                                      │
                              [Power BI / Metabase]
                                      │
                         [Git + Docker (entorno local)]
```

---

## 6. Plan de preparación sugerido (portafolio)

Para demostrar las competencias, se recomienda construir un mini-proyecto integral que toque todo el stack:

### Proyecto demo sugerido: "Automatización de tickets de soporte con IA"
1. **n8n + Docker**: levantar n8n y PostgreSQL en `docker-compose.yml`.
2. **Webhook**: recibir solicitudes (ej. un formulario / email).
3. **OpenAI API**: clasificar el ticket (categoría) y extraer campos clave (fecha, monto, cliente).
4. **Odoo**: crear/actualizar un `crm.lead` o tarea automáticamente (vía XML-RPC o REST).
5. **PostgreSQL**: almacenar el histórico y hacer consultas de agregación.
6. **Metabase**: tablero con tickets por categoría y estado.
7. **Python script**: ETL de respaldo + pruebas locales.
8. **Git**: documentar todo el proceso en un README.

---

## 7. Puntos a preparar para la entrevista

1. Explicar un flujo real armado en Make/Zapier/n8n (trigger → proceso → acción).
2. Cómo autenticas una API REST (Bearer token, OAuth2, API keys).
3. Ejemplo de llamada a OpenAI para clasificación (diseño del prompt + parsing del JSON de respuesta).
4. Consulta SQL con JOIN entre tablas de Odoo/ventas.
5. Cómo levantarías un entorno local con Docker (volúmenes, puertos, redes).
6. Cómo documentas procesos y propones mejoras a usuarios de negocio.

---

## 8. Conexión con proyectos previos

| Competencia del puesto | Proyecto previo relacionado |
|---|---|
| Python / análisis de datos | Proyecto 1: `modelo_scoring_riesgo.py` |
| Full-stack / API / DevOps | Proyecto 2: plataforma retail de microservicios |
| PostgreSQL / APIs REST | Ambos proyectos previos (base de datos y servicios) |
| Documentación técnica | Guías de trabajo y propuestas técnicas elaboradas previamente |

**Gap principal a cubrir:** Make / Zapier / n8n (flujos low-code), integraciones OpenAI API y módulos de Odoo. Son las 3 áreas de mayor peso en esta oferta.
