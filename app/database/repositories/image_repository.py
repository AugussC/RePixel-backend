# app/repositories/image_repository.py

from app.database.connection import abrir_conexion
from psycopg2.extras import RealDictCursor

def insertar_imagen(data):
    connection = abrir_conexion()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT ... RETURNING *", data)
        result = cursor.fetchone()
        connection.commit()
        return result

    except Exception as e:
        connection.rollback()
        raise e 
    
def obtener_imagen_por_id_db(image_id):
    connection = abrir_conexion()
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT i.*, u.nombre, u.apellido, u.correo, u.contrasena, u.id_rol, r.nombre_rol
            FROM Imagen i
            JOIN Usuario u ON i.id_usuario = u.id_usuario
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE i.id_imagen = %s
        """

        cursor.execute(query, (image_id,))
        return cursor.fetchone()

    except Exception as e:
        connection.rollback()
        raise e
    
def obtener_imagenes_por_usuario_db(user_id):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM imagen
            WHERE id_usuario = %s AND estado = true
        """, (user_id,))

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    
def desactivar_imagen_db(image_id, fecha_expiracion):
    connection = abrir_conexion()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE imagen
            SET estado = false,
                fecha_expiracion = %s
            WHERE id_imagen = %s
        """, (fecha_expiracion, image_id))

        connection.commit()
        return True

    except Exception as e:
        connection.rollback()
        raise e