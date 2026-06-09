from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def obtener_algoritmo_por_nombre(nombre):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT * FROM obtener_algoritmo_por_nombre(%s)",
            (nombre,)
        )
        return cursor.fetchone()

    except Exception as e:
        connection.rollback()
        raise e