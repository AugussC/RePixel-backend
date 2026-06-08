import pytest
from app.utils.image_utils import validar_imagen

# Creamos una clase Mock más completa que simule los métodos que usa Flask (seek y tell)
class MockFile:
    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
    
    def seek(self, *args):
        # Simula el movimiento del cursor en el archivo
        pass
    
    def tell(self):
        # Devuelve el tamaño simulado
        return self.size

def test_validar_imagen_formato_correcto():
    # Simulamos el archivo y el diccionario 'request.files' de Flask
    archivo = MockFile("imagen.jpg", 3 * 1024 * 1024) # 3 MB
    archivos_request = {'file': archivo}
    
    # La validación debería ser exitosa y retornar el archivo y el id_tipo (2 para jpg)
    resultado, id_tipo = validar_imagen(archivos_request)
    assert resultado is not None
    assert id_tipo == 2

def test_validar_imagen_formato_incorrecto():
    archivo = MockFile("imagen.gif", 2 * 1024 * 1024) # 2 MB
    archivos_request = {'file': archivo}
    
    # Verificamos que lance la excepción exacta
    with pytest.raises(ValueError) as excinfo:
        validar_imagen(archivos_request)
    
    assert str(excinfo.value) == "La imagen debe tener formato (JPG/PNG/JPEG)"

def test_validar_imagen_tamano_excedido():
    archivo = MockFile("imagen.jpg", 6 * 1024 * 1024) # 6 MB
    archivos_request = {'file': archivo}
    
    with pytest.raises(ValueError) as excinfo:
        validar_imagen(archivos_request)
    
    assert str(excinfo.value) == "Su imagen supera el límite de tamaño de 5MB"

def test_validar_imagen_no_se_envio_archivo():
    # Simulamos un request sin la clave 'file'
    archivos_request = {} 
    
    with pytest.raises(ValueError) as excinfo:
        validar_imagen(archivos_request)
    
    assert str(excinfo.value) == "No se envió ningún archivo"