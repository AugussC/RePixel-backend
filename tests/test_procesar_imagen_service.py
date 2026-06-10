# tests/test_procesamiento_imagen.py

import pytest
from unittest.mock import patch, MagicMock
from app.services.procesarImage_services import (procesar_imagen_service)


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_enfoque(mock_imagen,mock_algoritmo,mock_crear,mock_procesador,mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"
    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    mock_crear.return_value = {"id_procesamiento": 10}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/enfoque.jpg")

    mock_procesador.return_value = procesador
    resultado = procesar_imagen_service(1,"enfocar")

    assert resultado["mensaje"] == ("Procesamiento exitoso")

    mock_actualizar.assert_called_once_with(
        10,
        estado="completado",
        ruta_resultado="uploads/enfoque.jpg"
    )


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_reduccion_ruido(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 2}
    mock_crear.return_value = {"id_procesamiento": 11}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/sin_ruido.jpg")
    mock_procesador.return_value = procesador
    resultado = procesar_imagen_service(1,"quitar_ruido")

    assert resultado["ruta_resultado"] == ("uploads/sin_ruido.jpg")


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_brillo(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):
    
    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 3}
    mock_crear.return_value = {"id_procesamiento": 12}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/brillo.jpg")
    mock_procesador.return_value = procesador

    resultado = procesar_imagen_service(1,"ajustar_brillo")
    assert resultado["id_procesamiento"] == 12


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_blanco_negro(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 4}
    mock_crear.return_value = {"id_procesamiento": 13}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/bn.jpg")
    mock_procesador.return_value = procesador

    resultado = procesar_imagen_service(1,"blanco_negro")

    assert resultado["ruta_resultado"] == ("uploads/bn.jpg")


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_restauracion(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 5}
    mock_crear.return_value = {"id_procesamiento": 14}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/restaurada.jpg")
    mock_procesador.return_value = procesador

    resultado = procesar_imagen_service(1,"restaurar")

    assert resultado["ruta_resultado"] == ("uploads/restaurada.jpg")



@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_sin_imagen(mock_imagen):
    
    mock_imagen.return_value = None

    with pytest.raises(Exception) as exc:
        procesar_imagen_service(1,"enfocar")

    assert str(exc.value) == ("Imagen no encontrada")


@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_id_imagen_invalido(mock_imagen):

    mock_imagen.return_value = None

    with pytest.raises(Exception) as exc:
        procesar_imagen_service(None,"enfocar")

    assert str(exc.value) == ("Imagen no encontrada")


@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_algoritmo_inexistente(mock_imagen,mock_algoritmo):

    imagen = MagicMock()
    imagen.ruta = "test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = None

    with pytest.raises(Exception) as exc:
        procesar_imagen_service(1,"fake")
        
    assert str(exc.value) == (
        "Algoritmo no encontrado"
    )


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_imagen_corrupta(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "corrupta.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    mock_crear.return_value = {"id_procesamiento": 15}

    procesador = MagicMock()
    procesador.procesar.side_effect = (Exception("No se pudo leer la imagen"))
    mock_procesador.return_value = procesador

    with pytest.raises(Exception):
        procesar_imagen_service(1,"enfocar")


@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_error_interno_excepcion(mock_imagen,mock_algoritmo,mock_crear,mock_procesador):

    imagen = MagicMock()
    imagen.ruta = "test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    mock_crear.return_value = {"id_procesamiento": 16}

    procesador = MagicMock()
    procesador.procesar.side_effect = (Exception("Error interno"))
    mock_procesador.return_value = procesador

    with pytest.raises(Exception):
        procesar_imagen_service(1,"enfocar")


@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_imagen_eliminada(mock_imagen):

    mock_imagen.return_value = None
    with pytest.raises(Exception):
        procesar_imagen_service(99,"enfocar")


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_se_registra_procesamiento(mock_imagen,mock_algoritmo,mock_crear,mock_procesador, mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    mock_crear.return_value = {"id_procesamiento": 20}

    procesador = MagicMock()
    procesador.procesar.return_value = ("uploads/resultado.jpg")
    mock_procesador.return_value = procesador

    procesar_imagen_service(1,"enfocar")

    mock_crear.assert_called_once_with(id_imagen=1,id_algoritmo=1,estado="procesando")

@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesar_algoritmo_vacio(mock_imagen,mock_algoritmo):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = None

    with pytest.raises(Exception) as exc:
        procesar_imagen_service(1,"")

    assert str(exc.value) == ("Algoritmo no encontrado")


@patch("app.services.procesarImage_services.actualizar_procesamiento")
@patch("app.services.procesarImage_services.obtener_procesador")
@patch("app.services.procesarImage_services.crear_procesamiento")
@patch("app.services.procesarImage_services.obtener_algoritmo_por_nombre")
@patch("app.services.procesarImage_services.obtener_imagen_por_id")
def test_procesamiento_fallido_actualiza_estado_error(mock_imagen,mock_algoritmo,mock_crear,mock_procesador,mock_actualizar):

    imagen = MagicMock()
    imagen.ruta = "uploads/test.jpg"

    mock_imagen.return_value = imagen
    mock_algoritmo.return_value = {"id_algoritmo": 1}
    mock_crear.return_value = {"id_procesamiento": 50}

    procesador = MagicMock()

    procesador.procesar.side_effect = (Exception("Error interno"))
    mock_procesador.return_value = procesador

    with pytest.raises(Exception) as exc:
        procesar_imagen_service(1,"enfocar")

    assert str(exc.value) == ("Error interno")

    mock_actualizar.assert_called_with(50,estado="error")