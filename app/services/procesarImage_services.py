
from app.database.repositories.procesamiento_repository import (crear_procesamiento,actualizar_procesamiento)
from app.database.repositories.algoritmo_repository import (obtener_algoritmo_por_nombre)
from app.services.image_services import obtener_imagen_por_id
from app.services.processors_services import obtener_procesador

def procesar_imagen_service(id_imagen, nombre_algoritmo):
    imagen = obtener_imagen_por_id(id_imagen)
    if not imagen:
        raise Exception("Imagen no encontrada")

    algoritmo = obtener_algoritmo_por_nombre(nombre_algoritmo)
    if not algoritmo:
        raise Exception("Algoritmo no encontrado")

    procesamiento = crear_procesamiento(
        id_imagen=id_imagen,
        id_algoritmo=algoritmo["id_algoritmo"],
        estado="procesando"
    )

    try:
        procesador = obtener_procesador(nombre_algoritmo)
        if not procesador:
            raise Exception("No se encontró un procesador de código para este algoritmo")
            
        ruta_resultado = procesador.procesar(imagen.ruta)

        actualizar_procesamiento(
            procesamiento["id_procesamiento"],
            estado="completado",
            ruta_resultado=ruta_resultado
        )

        return {
            "id_procesamiento": procesamiento["id_procesamiento"],
            "mensaje": "Procesamiento exitoso",
            "ruta_resultado": ruta_resultado
        }

    except Exception as e:
        actualizar_procesamiento(
            procesamiento["id_procesamiento"],
            estado="error"
        )
        raise e