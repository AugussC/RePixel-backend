from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def obtener_tipo_imagen_disponible():
    connection = abrir_conexion()   

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT id_tipoimagen, nombre_tipoimagen FROM tipoimagen
        """)
        return cursor.fetchall()
 
    except Exception as e:
        connection.rollback()
        raise e