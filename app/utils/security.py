import re

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ==================================================
# CONTRASEÑAS
# ==================================================

def hash_password(password):

    if not password:
        raise ValueError(
            "La contraseña no puede estar vacía"
        )

    return generate_password_hash(password)


def verify_password(
    hash_guardado,
    password_plana
):

    return check_password_hash(
        hash_guardado,
        password_plana
    )


# ==================================================
# VALIDACIONES DE SEGURIDAD
# ==================================================

def validar_correo(correo):

    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(patron, correo):
        raise ValueError(
            "Formato de correo inválido"
        )

    return correo


def validar_password(password):

    if len(password) < 8:
        raise ValueError(
            "La contraseña debe tener al menos 8 caracteres"
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Debe contener una mayúscula"
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Debe contener una minúscula"
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Debe contener un número"
        )

    return password


def detectar_sql_injection(texto):

    patrones = [
        r"(--)",
        r"(\bOR\b)",
        r"(\bAND\b)",
        r"(\bDROP\b)",
        r"(\bDELETE\b)",
        r"(\bUNION\b)",
        r"(\bSELECT\b)"
    ]

    texto = texto.upper()

    for patron in patrones:
        if re.search(patron, texto):
            raise ValueError(
                "Entrada potencialmente peligrosa"
            )

    return texto


def detectar_xss(texto):

    patrones = [
        r"<script.*?>",
        r"</script>",
        r"javascript:",
        r"onerror=",
        r"onload="
    ]

    texto_lower = texto.lower()

    for patron in patrones:
        if re.search(patron, texto_lower):
            raise ValueError(
                "Contenido potencialmente peligroso"
            )

    return texto


def validar_nombre_archivo_seguro(
    filename
):

    extensiones_permitidas = {
        "jpg",
        "jpeg",
        "png"
    }

    if "." not in filename:
        raise ValueError(
            "Archivo sin extensión"
        )

    extension = (
        filename.lower()
        .split(".")[-1]
    )

    if extension not in extensiones_permitidas:
        raise ValueError(
            "Tipo de archivo no permitido"
        )

    detectar_xss(filename)

    return filename