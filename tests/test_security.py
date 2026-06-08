import pytest

from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.user_validators import (
    validar_login_data,
    validar_register_data
)

from app.utils.imagen_validators import (
    validar_extension_archivo
)


# ==================================================
# PASSWORD ENCRIPTADA
# ==================================================

def test_password_encriptada():

    password = "123456"

    hash_generado = hash_password(password)

    assert hash_generado != password
    assert verify_password(
        hash_generado,
        password
    )


# ==================================================
# SQL INJECTION LOGIN
# ==================================================

def test_sql_injection_login():

    correo, password = validar_login_data({
        "correo": "' OR 1=1 --",
        "contraseña": "123456"
    })

    assert correo == "' OR 1=1 --"


# ==================================================
# SQL INJECTION REGISTRO
# ==================================================

def test_sql_injection_registro():

    resultado = validar_register_data({
        "nombre": "'; DROP TABLE usuario; --",
        "apellido": "Perez",
        "correo": "test@test.com",
        "contraseña": "123456",
        "rol": 1
    })

    assert resultado[0] == "'; DROP TABLE usuario; --"


# ==================================================
# XSS NOMBRE USUARIO
# ==================================================

def test_xss_nombre_usuario():

    resultado = validar_register_data({
        "nombre": "<script>alert('xss')</script>",
        "apellido": "Perez",
        "correo": "test@test.com",
        "contraseña": "123456",
        "rol": 1
    })

    assert "<script>" in resultado[0]


# ==================================================
# XSS NOMBRE ARCHIVO
# ==================================================

def test_xss_nombre_archivo():

    nombre = "<script>alert(1)</script>.jpg"

    tipo = validar_extension_archivo(nombre)

    assert tipo == 2


# ==================================================
# ARCHIVO EJECUTABLE
# ==================================================

def test_subida_archivo_ejecutable():

    with pytest.raises(ValueError):

        validar_extension_archivo(
            "virus.exe"
        )


# ==================================================
# SCRIPT PHP
# ==================================================

def test_subida_script_php():

    with pytest.raises(ValueError):

        validar_extension_archivo(
            "shell.php"
        )


# ==================================================
# CONTENIDO MALICIOSO
# ==================================================

def test_subida_archivo_contenido_malicioso():

    with pytest.raises(ValueError):

        validar_extension_archivo(
            "malware.bat"
        )