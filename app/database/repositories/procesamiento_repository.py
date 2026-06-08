from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def crear_procesamiento(id_imagen, id_algoritmo, estado="procesando"):

    connection = abrir_conexion()

    try:
        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            INSERT INTO procesamiento (
                id_imagen,
                id_algoritmo,
                estado_procesamiento
            )
            VALUES (
                %s,
                %s,
                %s
            )
            RETURNING *
        """, (
            id_imagen,
            id_algoritmo,
            estado
        ))

        result = cursor.fetchone()

        connection.commit()

        return result

    except Exception as e:
        connection.rollback()
        raise e
    
def obtener_procesamiento_por_id(id_procesamiento):

    connection = abrir_conexion()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT p.*, a.nombre AS nombre_algoritmo
            FROM procesamiento p JOIN algoritmo a ON p.id_algoritmo = a.id_algoritmo
            WHERE id_procesamiento = %s
        """, (id_procesamiento,))

        return cursor.fetchone()

    except Exception as e:

        connection.rollback()

        raise e
    
def actualizar_procesamiento(id_procesamiento, estado=None, ruta_resultado=None):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        fields = []
        values = []

        if estado:
            fields.append("estado_procesamiento = %s")
            values.append(estado)

        if ruta_resultado:
            fields.append("ruta_resultado = %s")
            values.append(ruta_resultado)

        if not fields:
            return None

        # Agregamos el ID al final de los valores para el WHERE
        values.append(id_procesamiento)

        # El WHERE ya no lleva un %s hardcodeado extra si mapeamos correctamente
        query = f"""
            UPDATE procesamiento
            SET {', '.join(fields)}
            WHERE id_procesamiento = %s
            RETURNING *
        """

        cursor.execute(query, tuple(values))
        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e
    
def obtener_procesamientos_por_imagen(id_imagen):

    connection = abrir_conexion()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT p.*, a.nombre AS nombre_algoritmo
            FROM Procesamiento p JOIN Algoritmo a ON p.id_algoritmo = a.id_algoritmo
            WHERE id_imagen = %s
        """, (id_imagen,))

        return cursor.fetchall()

    except Exception as e:

        connection.rollback()

        raise e
    
def eliminar_procesamiento(
    id_procesamiento
):

    connection = abrir_conexion()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            DELETE FROM procesamiento
            WHERE id_procesamiento = %s
        """, (id_procesamiento,))

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        raise e