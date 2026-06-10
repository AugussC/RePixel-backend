import pytest
from unittest.mock import patch
from flask import Flask, session
from app.services.user_services import crear_usuario
from app.utils.user_validators import (validar_login_data,validar_register_data,validar_usuario_autenticado)


@patch("app.services.user_services.insertar_usuario_db")
@patch("app.services.user_services.hash_password")
@patch("app.services.user_services.obtener_rol_por_id_db")
@patch("app.services.user_services.obtener_usuario_por_correo_db")
def test_registrar_usuario_correctamente(mock_correo,mock_rol,mock_hash,mock_insertar):

    mock_correo.return_value = None
    mock_rol.return_value = {
        "id_rol": 1,
        "nombre_rol": "usuario"
    }
    mock_hash.return_value = "HASH123"
    mock_insertar.return_value = {"id_usuario": 10}
    resultado = crear_usuario(
        "Juan",
        "Perez",
        "juan@test.com",
        "123456",
        1
    )

    assert resultado is not None
    assert resultado.nombre == "Juan"
    assert resultado.apellido == "Perez"
    assert resultado.correo == "juan@test.com"


@patch("app.services.user_services.obtener_usuario_por_correo_db")
def test_correo_unico(mock_correo):
    
    mock_correo.return_value = None
    assert mock_correo("nuevo@test.com") is None


@patch("app.services.user_services.obtener_usuario_por_correo_db")
def test_registro_correo_existente(mock_correo):

    mock_correo.return_value = {"id_usuario": 1}
    resultado = crear_usuario(
        "Juan",
        "Perez",
        "juan@test.com",
        "123456",
        1
    )

    assert resultado is None


def test_registro_sin_nombre():
    with pytest.raises(ValueError) as excinfo:

        validar_register_data({
            "apellido": "Perez",
            "correo": "juan@test.com",
            "contraseña": "123456",
            "rol": 1
        })

    assert str(excinfo.value) == ("Todos los campos son obligatorios")


def test_registro_sin_apellido():

    with pytest.raises(ValueError):
        validar_register_data({
            "nombre": "Juan",
            "correo": "juan@test.com",
            "contraseña": "123456",
            "rol": 1
        })

def test_registro_sin_correo():

    with pytest.raises(ValueError):
        validar_register_data({
            "nombre": "Juan",
            "apellido": "Perez",
            "contraseña": "123456",
            "rol": 1
        })

def test_registro_sin_password():

    with pytest.raises(ValueError):
        validar_register_data({
            "nombre": "Juan",
            "apellido": "Perez",
            "correo": "juan@test.com",
            "rol": 1
        })

@patch("app.services.user_services.insertar_usuario_db")
@patch("app.services.user_services.hash_password")
@patch("app.services.user_services.obtener_rol_por_id_db")
@patch("app.services.user_services.obtener_usuario_por_correo_db")
def test_password_se_guarda_encriptada(mock_correo,mock_rol,mock_hash,mock_insertar):

    mock_correo.return_value = None
    mock_rol.return_value = {
        "id_rol": 1,
        "nombre_rol": "usuario"
    }

    mock_hash.return_value = "HASH_SEGURO"
    mock_insertar.return_value = {"id_usuario": 1}
    crear_usuario(
        "Juan",
        "Perez",
        "juan@test.com",
        "123456",
        1
    )

    mock_hash.assert_called_once_with("123456")

def test_login_sin_correo():

    with pytest.raises(ValueError) as excinfo:
        validar_login_data({"contraseña": "123456"})

    assert str(excinfo.value) == ("Correo y contraseña obligatorios")

def test_login_sin_password():
    with pytest.raises(ValueError) as excinfo:
        validar_login_data({
            "correo": "juan@test.com"
        })

    assert str(excinfo.value) == ("Correo y contraseña obligatorios")

def test_login_data_valida():

    correo, password = validar_login_data({
        "correo": "juan@test.com",
        "contraseña": "123456"
    })

    assert correo == "juan@test.com"
    assert password == "123456"


def test_usuario_autenticado():

    app = Flask(__name__)
    app.secret_key = "test"

    with app.test_request_context():
        session["user_id"] = 5

        resultado = validar_usuario_autenticado()

        assert resultado == 5


def test_usuario_no_autenticado():

    app = Flask(__name__)
    app.secret_key = "test"

    with app.test_request_context():
        with pytest.raises(PermissionError) as excinfo:
            validar_usuario_autenticado()

        assert str(excinfo.value) == ("No autorizado")

def test_register_data_valida():

    resultado = validar_register_data({
        "nombre": "Juan",
        "apellido": "Perez",
        "correo": "juan@test.com",
        "contraseña": "123456",
        "rol": 1
    })

    assert resultado == (
        "Juan",
        "Perez",
        "juan@test.com",
        "123456",
        1
    )