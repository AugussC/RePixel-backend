import pytest
from unittest.mock import patch

from app.services.image_services import desactivar_imagen


# ==================================================
# ELIMINAR IMAGEN EXISTENTE
# ==================================================

@patch("app.services.image_services.desactivar_imagen_db")
def test_eliminar_imagen_existente(
    mock_desactivar
):

    mock_desactivar.return_value = True

    resultado = desactivar_imagen(1)

    assert resultado is True
    mock_desactivar.assert_called_once()


# ==================================================
# ELIMINAR IMAGEN INEXISTENTE
# ==================================================

@patch("app.services.image_services.desactivar_imagen_db")
def test_eliminar_imagen_inexistente(
    mock_desactivar
):

    mock_desactivar.return_value = False 

    resultado = desactivar_imagen(999)

    assert resultado is False


# ==================================================
# ERROR AL ELIMINAR
# ==================================================

@patch("app.services.image_services.desactivar_imagen_db")
def test_eliminar_imagen_error(
    mock_desactivar
):

    mock_desactivar.side_effect = Exception(
        "Imagen no encontrada"
    )

    with pytest.raises(Exception) as excinfo:
        desactivar_imagen(999)

    assert str(excinfo.value) == (
        "Imagen no encontrada"
    )


# ==================================================
# ELIMINAR IMAGEN DOS VECES
# ==================================================

@patch("app.services.image_services.desactivar_imagen_db")
def test_eliminar_imagen_doble(
    mock_desactivar
):

    mock_desactivar.side_effect = [
        True,
        False
    ]

    primer_resultado = desactivar_imagen(1)
    segundo_resultado = desactivar_imagen(1)

    assert primer_resultado is True
    assert segundo_resultado is False


# ==================================================
# VERIFICAR QUE SE LLAMA AL REPOSITORIO
# ==================================================

@patch("app.services.image_services.desactivar_imagen_db")
def test_desactivar_imagen_llama_repositorio(
    mock_desactivar
):

    mock_desactivar.return_value = True

    desactivar_imagen(5)

    mock_desactivar.assert_called_once()