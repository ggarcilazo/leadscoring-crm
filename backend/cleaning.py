import html
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_DIGITS_RE = re.compile(r"\d{9}")
TAG_RE = re.compile(r"<[^>]+>")


def sanitizar_texto(valor):
    texto = html.unescape(str(valor or ""))
    texto = TAG_RE.sub(" ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def validar_email(email):
    return bool(email and EMAIL_RE.match(str(email).strip()))


def normalizar_telefono(telefono):
    if not telefono:
        return None
    digitos = re.sub(r"\D", "", str(telefono))
    if len(digitos) == 9 and digitos.startswith("9"):
        return f"+51{digitos}"
    if len(digitos) == 11 and digitos.startswith("51"):
        return f"+{digitos}"
    return None


def limpiar_lead(payload):
    email = sanitizar_texto(payload.get("email"))
    telefono = normalizar_telefono(payload.get("telefono"))
    errores = []

    if not validar_email(email):
        errores.append("email_invalido")
    if not telefono:
        errores.append("telefono_invalido")

    empresa = sanitizar_texto(payload.get("empresa"))
    if not empresa:
        errores.append("empresa_vacia")

    if errores:
        raise ValueError(";".join(errores))

    return {
        "nombre": sanitizar_texto(payload.get("nombre")),
        "empresa": empresa,
        "sector": sanitizar_texto(payload.get("sector")) or "Sin clasificar",
        "email": email,
        "telefono": telefono,
        "resumen_ejecutivo": sanitizar_texto(payload.get("resumen_ejecutivo")),
        "urgencia": sanitizar_texto(payload.get("urgencia")).lower() or "baja",
        "presupuesto": sanitizar_texto(payload.get("presupuesto")),
        "tags": [sanitizar_texto(t) for t in payload.get("tags", []) if sanitizar_texto(t)],
    }
