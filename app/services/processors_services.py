from app.utils.processors import EnfocarProcessor, QuitarRuidoProcessor, BlancoNegroProcessor, RestaurarImagenProcessor, AjustarBrilloProcessor

def obtener_procesador(nombre_algoritmo):

    procesadores = {
        "restaurar imagen": RestaurarImagenProcessor(),
        "enfocar": EnfocarProcessor(),
        "blanco y negro": BlancoNegroProcessor(),
        "quitar ruido": QuitarRuidoProcessor(),
        "ajustar brillo": AjustarBrilloProcessor()
    }

    return procesadores.get(nombre_algoritmo)