from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

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

def obtener_algoritmo_por_nombre(nombre):

    connection = abrir_conexion()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM algoritmo
            WHERE nombre=%s
        """,(nombre,))

        return cursor.fetchone()

    except Exception as e:

        connection.rollback()

        raise e