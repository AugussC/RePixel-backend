
from unittest.mock import MagicMock, patch
import pytest
from app.services.image_services import desactivar_imagen, subir_imagen
from app.services.procesarImage_services import procesar_imagen_service
from flask import Flask
from app.utils.user_validators import validar_register_data

app = Flask(__name__)

@patch("app.services.image_services.insertar_imagen")
@patch("app.services.image_services.obtener_metadata_imagen")
def test_subir_imagen_doble(mock_metadata, mock_insertar):
    mock_metadata.return_value = ("2025-08-01", "2025-09-01", 800, 600, 1024, "foto.jpg" )

    mock_insertar.return_value = {
    "id_imagen": 1,
    "altura": 800,
    "ancho": 600,
    "fecha_subida": "2025-08-01",
    "fecha_expiracion": "2025-09-01",
    "peso_subida": 1024,
    "ruta": "uploads/foto.jpg",
    "id_tipoimagen": 2,
    "nombre_archivo": "foto.jpg"
}
    resultado1 = subir_imagen("uploads/foto.jpg", 1, 2)
    assert resultado1.id == 1

    mock_insertar.return_value = {
    "id_imagen": 2,
    "altura": 800,
    "ancho": 600,
    "fecha_subida": "2025-08-01",
    "fecha_expiracion": "2025-09-01",
    "peso_subida": 1024,
    "ruta": "uploads/foto.jpg",
    "id_tipoimagen": 2,
    "nombre_archivo": "foto.jpg"
}
    resultado2 = subir_imagen("uploads/foto.jpg", 1, 2)
    assert resultado2.id == 2
    
@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_imagen_multiple(mock_imagen, mock_algoritmo, mock_crear, mock_procesador, mock_actualizar):
    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"
    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    
    mock_crear.side_effect = [
        {"id_procesamiento": 10},
        {"id_procesamiento": 11}
    ]
    
    procesador = MagicMock()
    procesador.procesar.return_value = "uploads/enfoque.jpg"
    mock_procesador.return_value = procesador


    resultado1 = procesar_imagen_service(1, "enfocar")
    assert resultado1["mensaje"] == "Procesamiento exitoso"

    resultado2 = procesar_imagen_service(1, "enfocar")
    assert resultado2["mensaje"] == "Procesamiento exitoso"



@pytest.mark.parametrize("i", range(5))
@patch("app.services.image_services.insertar_imagen")
@patch("app.services.image_services.obtener_metadata_imagen")
def test_subir_imagen_exitosamente_repetido(mock_metadata, mock_insertar, i):
    mock_metadata.return_value = (
        "2025-08-01",
        "2025-09-01",
        800,
        600,
        1024,
        "foto.jpg"
    )

    mock_insertar.return_value = {
        "id_imagen": 1,
        "altura": 800,
        "ancho": 600,
        "fecha_subida": "2025-08-01",
        "fecha_expiracion": "2025-09-01",
        "peso_subida": 1024,
        "ruta": "uploads/foto.jpg",
        "id_tipoimagen": 2,
        "nombre_archivo": "foto.jpg"
    }

    resultado = subir_imagen("uploads/foto.jpg", 1, 2)

    assert resultado is not None
    assert resultado.id == 1
    assert resultado.nombre_archivo == "foto.jpg"



@pytest.mark.parametrize("i", range(5))
def test_registro_sin_apellido_repetido(i):
    with pytest.raises(ValueError):
        validar_register_data({
            "nombre": "Juan",
            "correo": "juan@test.com",
            "contraseña": "123456",
            "rol": 1
        })



@pytest.mark.parametrize("i", range(5))
@patch("app.services.image_services.desactivar_imagen_db")
def test_eliminar_imagen_doble_repetido(mock_desactivar, i):
    mock_desactivar.side_effect = [True, False] * 5  

    primer_resultado = desactivar_imagen(1)
    segundo_resultado = desactivar_imagen(1)

    assert primer_resultado is True
    assert segundo_resultado is False
    