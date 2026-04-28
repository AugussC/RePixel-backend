# app/utils/image_utils.py

import cv2
import os

def obtener_metadata_imagen(filepath):
    img = cv2.imread(filepath) 
    if img is None: 
        return None
    
    altura, ancho = img.shape[:2]
    peso = os.path.getsize(filepath)

    return altura, ancho, peso


def guardar_archivo(file):

    filepath = os.path.join('uploads', file.filename)

    file.save(filepath)

    return filepath