
from app.database.repositories.procesamiento_repository import (
    crear_procesamiento,
    actualizar_procesamiento
)
from app.database.repositories.algoritmo_repository import (obtener_algoritmo_por_nombre)
from app.services.image_services import obtener_imagen_por_id
from app.database.repositories.algoritmo_repository import obtener_procesador


def procesar_imagen_service(id_imagen, algoritmo):

    imagen = obtener_imagen_por_id(id_imagen)

    if not imagen:
        raise Exception("Imagen no encontrada")

    algoritmo_db = obtener_algoritmo_por_nombre(algoritmo)

    if not algoritmo_db:
        raise Exception(
            "Algoritmo no encontrado"
        )

    procesamiento = crear_procesamiento(
        id_imagen=id_imagen,
        id_algoritmo=algoritmo_db["id_algoritmo"],
        estado="procesando"
    )

    try:

        procesador = obtener_procesador(algoritmo)

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