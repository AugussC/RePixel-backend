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


def subir_imagen(filepath, user_id, id_tipoimagen):
    metadata = obtener_metadata_imagen(filepath)
    if metadata is None:
        return None

    fecha, fecha_expiracion, altura, ancho, peso = metadata
    
    data = (
        altura,
        ancho,
        fecha,
        fecha_expiracion,
        peso,
        id_tipoimagen,
        user_id,
        filepath
    )

    result = insertar_imagen(data)

    return Image(
        result['id_imagen'],
        result['altura'],
        result['ancho'],
        result['fecha_subida'],
        result['fecha_expiracion'],
        result['peso_subida'],
        result['ruta'],
        result['id_tipoimagen'],
        user_id
    )
    

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
        data['contraseña'],
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

    fecha_expiracion = datetime.now()
    return desactivar_imagen_db(image_id, fecha_expiracion)
