from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def obtener_usuario_por_correo_db(correo):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                id_usuario,
                nombre,
                apellido,
                correo,
                contraseña,
                id_rol
            FROM Usuario
            WHERE correo = %s AND estado = TRUE
        """, (correo,))
        return cursor.fetchone()
    except Exception as e:
        connection.rollback()
        raise e

def obtener_usuario_por_id_db(user_id):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """

        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    except Exception as e:
        connection.rollback()
        raise e


def obtener_rol_por_id_db(id_rol):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id_rol, nombre_rol FROM Rol WHERE id_rol = %s", (id_rol,))
        return cursor.fetchone()
    except Exception as e:
        connection.rollback()
        raise e


def insertar_usuario_db(nombre, apellido, correo, password_hash, id_rol):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            INSERT INTO Usuario (nombre, apellido, correo, contraseña, id_rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario
        """, (nombre, apellido, correo, password_hash, id_rol))

        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e


