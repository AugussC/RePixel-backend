import cv2
import os
from datetime import datetime
from app.models.image_model import Image
from app.models.user_model import User
from app.models.rol_model import Rol
from app.services.user_services import obtener_usuario_por_id
from app.utils.image_utils import obtener_metadata_imagen
from app.utils.date_utils import obtener_fechas_expiracion
from app.database.repositories.image_repository import desactivar_imagen_db, desactivar_imagen_db, insertar_imagen, obtener_imagen_por_id_db, obtener_imagenes_por_usuario_db
from app.models.image_model import Image


def subir_imagen(filepath, current_user, id_tipoimagen):
    metadata = obtener_metadata_imagen(filepath)
    if metadata is None:
        return None

    altura, ancho, peso = metadata
    fecha, fecha_expiracion = obtener_fechas_expiracion()

    data = (
        altura,
        ancho,
        fecha,
        fecha_expiracion,
        peso,
        id_tipoimagen,
        current_user.id,
        filepath
    )

<<<<<<< Updated upstream
        altura, ancho = img.shape[:2]
        peso = os.path.getsize(filepath)
        fecha = datetime.now()
        fecha_expiracion = fecha + timedelta(hours=12)

        user_id = current_user.id
        
        cursor.execute("""
            INSERT INTO Imagen (altura, ancho, fecha_subida, fecha_expiracion, peso_subida, id_tipoimagen, id_usuario, ruta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (altura, ancho, fecha, fecha_expiracion, peso, id_tipoimagen, user_id, filepath))
=======
    result = insertar_imagen(data)
>>>>>>> Stashed changes

    return Image(
        result['id_imagen'],
        result['altura'],
        result['ancho'],
        result['fecha_subida'],
        result['fecha_expiracion'],
        result['peso_subida'],
        result['ruta'],
        result['id_tipoimagen'],
        current_user
    )
    

<<<<<<< Updated upstream
        return Image(
=======
def obtener_imagen_por_id(image_id):
    data = obtener_imagen_por_id_db(image_id)
    if not data:
        return None

    rol = Rol(data['id_rol'], data['nombre_rol'])

    usuario = User(
        data['id_usuario'],
        data['nombre'],
        data['apellido'],
        data['correo'],
        data['contrasena'],
        rol
    )

    return Image(
        data['id_imagen'],
        data['altura'],
        data['ancho'],
        data['fecha_subida'],
        data['fecha_expiracion'],
        data['peso_subida'],
        data['ruta'],
        data['id_tipoimagen'],
        usuario
    )

def obtener_imagenes_por_usuario(user_id):

    usuario_obj = obtener_usuario_por_id(user_id)

    rows = obtener_imagenes_por_usuario_db(user_id)

    images = []

    for data in rows:
        image = Image(
>>>>>>> Stashed changes
            data['id_imagen'],
            data['altura'],
            data['ancho'],
            data['fecha_subida'],
            data['fecha_expiracion'],
            data['peso_subida'],
            data['ruta'],
            data['id_tipoimagen'],
            usuario_obj
        )
        images.append(image)

    return images
    
def desactivar_imagen(image_id):

<<<<<<< Updated upstream
def get_image_by_id(image_id):
    connection = get_connection()
    if connection is None: return None

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
        data = cursor.fetchone()

        if not data: return None

        objeto_rol = Rol(data['id_rol'], data['nombre_rol'])
        usuario = User(data['id_usuario'], data['nombre'], data['apellido'], data['correo'], data['contrasena'], objeto_rol)

        return Image(
            data['id_imagen'], data['altura'], data['ancho'],
            data['fecha_subida'], data['fecha_expiracion'], data['peso_subida'],
            data['ruta'], data['id_tipoimagen'], usuario
        )

    except Exception as e:
        print(f"Error en get_image_by_id: {e}")
        return None

def get_images_by_user_service(user_id):
    connection = get_connection()
    if connection is None: return []

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)  
        
        usuario_obj = get_user_by_id(user_id)

        cursor.execute("""
            SELECT * FROM imagen
            WHERE id_usuario = %s AND estado = true
        """, (user_id,))

        rows = cursor.fetchall()
        images = []

        for data in rows:
            image = Image(
                data['id_imagen'], data['altura'], data['ancho'],
                data['fecha_subida'], data['fecha_expiracion'], data['peso_subida'],
                data['ruta'], data['id_tipoimagen'], usuario_obj
            )
            images.append(image)

        return images
    except Exception as e:
        print("Error get_images_by_user:", e)
        return []
    
def disable_image_service(image_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE imagen
            SET estado = false,
                fecha_expiracion = %s
            WHERE id_imagen = %s
        """, (datetime.now(), image_id))
        connection.commit()
        return True
    except Exception as e:
        print("Error disable_image:", e)
        return False
=======
    fecha_expiracion = datetime.now()
    return desactivar_imagen_db(image_id, fecha_expiracion)
>>>>>>> Stashed changes
