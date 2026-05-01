# app/utils/image_utils.py

from datetime import datetime, timedelta

import cv2
import os

from app.utils.imagen_validators import validar_archivo_en_request, validar_extension_archivo, validar_nombre_archivo, validar_tamano_archivo

def obtener_metadata_imagen(filepath):
    img = cv2.imread(filepath) 
    if img is None: 
        return None
    
    altura, ancho = img.shape[:2]
    peso = os.path.getsize(filepath)
    fecha = datetime.now()
    expiracion = fecha + timedelta(hours= 12)
    return fecha, expiracion, altura, ancho, peso
    


def guardar_archivo(file):

    filepath = os.path.join('uploads', file.filename)

    file.save(filepath)

    return filepath

def validar_imagen(file_storage):
    file = validar_archivo_en_request(file_storage)
    validar_nombre_archivo(file)
    id_tipoimagen = validar_extension_archivo(file.filename)
    validar_tamano_archivo(file)
            
    return file, id_tipoimagen