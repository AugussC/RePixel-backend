from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def obtener_usuario_por_correo_db(correo):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id_usuario FROM Usuario WHERE correo = %s", (correo,))
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
            INSERT INTO Usuario (nombre, apellido, correo, contrasena, id_rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario
        """, (nombre, apellido, correo, password_hash, id_rol))

        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e
    
def obtener_todos_los_usuarios_db():
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e

def actualizar_usuario_db(user_id, fields, values):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        values.append(user_id)

        query = f"UPDATE Usuario SET {', '.join(fields)} WHERE id_usuario = %s"
        cursor.execute(query, tuple(values))

        cursor.execute("""
            SELECT u.*, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (user_id,))

        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e

def cambiar_estado_usuario_db(user_id):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # 1. Toggle estado
        cursor.execute("""
            UPDATE Usuario
            SET estado = NOT estado
            WHERE id_usuario = %s
        """, (user_id,))

        # 2. Traer usuario actualizado (con JOIN)
        cursor.execute("""
            SELECT u.*, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (user_id,))

        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e