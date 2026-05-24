from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

from app.utils.processors import MejorarResolucionProcessor

def obtener_procesador(nombre):

    procesadores = {
        "mejorar resolucion": MejorarResolucionProcessor()
    }

    return procesadores.get(nombre)

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