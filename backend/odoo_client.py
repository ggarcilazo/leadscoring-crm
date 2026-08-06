import os
import xmlrpc.client

URL = os.environ["ODOO_URL"]
DB = os.environ["ODOO_DB"]
USERNAME = os.environ["ODOO_USERNAME"]
API_KEY = os.environ["ODOO_API_KEY"]


def _autenticar():
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, USERNAME, API_KEY, {})
    if not uid:
        raise ConnectionError("No se pudo autenticar en Odoo")
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    return uid, models


def _ejecutar(uid, models, modelo, metodo, *args, **kwargs):
    return models.execute_kw(DB, uid, API_KEY, modelo, metodo, args, kwargs)


def _obtener_o_crear_tags(uid, models, nombres):
    tag_ids = []
    for nombre in nombres:
        existente = _ejecutar(uid, models, "crm.tag", "search", [["name", "=", nombre]])
        if existente:
            tag_ids.append(existente[0])
        else:
            nuevo = _ejecutar(uid, models, "crm.tag", "create", {"name": nombre})
            tag_ids.append(nuevo)
    return tag_ids


def crear_oportunidad(lead_data):
    uid, models = _autenticar()

    tag_ids = _obtener_o_crear_tags(uid, models, lead_data.get("tags", []))
    urgencia = lead_data.get("urgencia", "baja")
    priority = "3" if urgencia == "alta" else "1"

    values = {
        "name": f"{lead_data['empresa']} - {lead_data['sector']}",
        "contact_name": lead_data["nombre"],
        "email_from": lead_data["email"],
        "phone": lead_data["telefono"],
        "description": lead_data["resumen_ejecutivo"],
        "tag_ids": [(6, 0, tag_ids)],
        "priority": priority,
    }

    if lead_data.get("presupuesto"):
        try:
            values["expected_revenue"] = float(lead_data["presupuesto"])
        except ValueError:
            values["expected_revenue"] = 0.0

    lead_id = _ejecutar(uid, models, "crm.lead", "create", values)

    if urgencia == "alta":
        model_ids = _ejecutar(uid, models, "ir.model", "search", [["model", "=", "crm.lead"]])
        res_model_id = model_ids[0] if model_ids else None
        if res_model_id:
            _ejecutar(
                uid,
                models,
                "mail.activity",
                "create",
                {
                    "activity_type_id": 1,
                    "res_model_id": res_model_id,
                    "res_id": lead_id,
                    "summary": "Seguimiento urgente requerido",
                    "note": "Lead clasificado como urgencia alta por la IA.",
                    "date_deadline": __import__("datetime").date.today().isoformat(),
                },
            )

    return lead_id
