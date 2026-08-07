import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from cleaning import limpiar_lead
from odoo_client import crear_oportunidad

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeadPayload(BaseModel):
    nombre: str = Field(default="", description="Nombre del contacto")
    empresa: str = Field(default="", description="Nombre de la empresa")
    sector: str = Field(default="", description="Sector clasificado por la IA")
    email: str = Field(default="")
    telefono: str = Field(default="")
    resumen_ejecutivo: str = Field(default="", description="Resumen generado por la IA")
    urgencia: str = Field(default="baja")
    presupuesto: str = Field(default="")
    tags: list[str] = Field(default_factory=list)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Backend Lead Scoring iniciado")
    yield


app = FastAPI(title="Lead Scoring Backend", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/leads")
def recibir_lead(payload: LeadPayload):
    try:
        lead_limpio = limpiar_lead(payload.model_dump())
    except ValueError as exc:
        logger.warning("Datos inválidos: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))

    try:
        lead_id = crear_oportunidad(lead_limpio)
    except Exception as exc:
        logger.error("Error creando lead en Odoo: %s", exc)
        raise HTTPException(status_code=502, detail="No se pudo crear la oportunidad en Odoo")

    logger.info("Lead %s creado con id %s", lead_limpio["empresa"], lead_id)
    return {"status": "ok", "odoo_id": lead_id}
