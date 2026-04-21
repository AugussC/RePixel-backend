import cv2
import os
from datetime import datetime, timedelta

from flask import jsonify
from app.database.connection import get_connection
from app.models.image_model import Image
from app.models.user_model import User
from psycopg2.extras import RealDictCursor


def upload_image(filepath):
    connection = get_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        img = cv2.imread(filepath)

        if img is None:
            print("No se pudo leer la imagen")
            return None

        altura, ancho = img.shape[:2]
        peso = os.path.getsize(filepath)
        fecha = datetime.now()
        fecha_expiracion = fecha + timedelta(hours=12)
        
        cursor.execute("""
            INSERT INTO Imagen (altura, ancho, fecha_subida, fecha_expiracion, peso_subida, id_tipoimagen, id_usuario, ruta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (altura, ancho, fecha, fecha_expiracion, peso, 1, 1, filepath))

        data = cursor.fetchone()
        connection.commit()

        usuario = User(1, "dummy", "dummy", "dummy@mail.com", "", None)


        image = Image(
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

        return image

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en upload_image: {e}")
        return None


def get_image_by_id(image_id):
    connection = get_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM Imagen WHERE id_imagen = %s
        """, (image_id,))

        data = cursor.fetchone()

        if not data:
            return None

        usuario = User(1, "dummy", "dummy", "dummy@mail.com", "", None)

        image = Image(
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

        return image

    except Exception as e:
        print(f"Error en get_image_by_id: {e}")
        return None
    
def get_images_by_user_service(user_id):

    connection = get_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM imagen
            WHERE id_usuario = %s AND estado = true
        """, (user_id,))

        rows = cursor.fetchall()

        images = []

        for data in rows:

            usuario = User(user_id, "dummy", "dummy", "dummy@mail.com", "", None)

            image = Image(
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