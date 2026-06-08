
import cv2
import numpy as np
import os 
from skimage import io 
from skimage.restoration import richardson_lucy


class EnfocarProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        blur = cv2.GaussianBlur(img,(9, 9),2)

        resultado = cv2.addWeighted(img,1.3,blur,-0.3,0)

        ruta_salida = "uploads/mejorar_resolucion_result.jpg"

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida


class QuitarRuidoProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception("No se pudo cargar la imagen")

        resultado = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

        ruta_salida = "uploads/sin_ruido_result.jpg"

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
    
class BlancoNegroProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception(
                "No se pudo leer la imagen"
            )

        resultado = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ruta_salida = ("uploads/blanco_negro.jpg")

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
    
class RestaurarImagenProcessor:

    def procesar(self, ruta):
        
        img = cv2.imread(ruta)

        if img is None:
            raise Exception("No se pudo leer la imagen")

        psf = np.ones((1, 15)) / 45

        # Separamos los canales BGR y aplicamos Richardson-Lucy a cada uno
        canal_azul, canal_verde, canal_rojo = cv2.split(img)

        def restaurar_canal(canal):
            # Convertir el canal a float32 y normalizar el canal al rango [0,1]
            c = canal.astype(np.float32) / 255.0 
            # Aplicar el algoritmo de deconvolución Richardson-Lucy utilizando la PSF (Point Spread Function) definida
            restaurado = richardson_lucy(c, psf, num_iter=20)
            # Volver al rango de imagen estándar [0,255]
            restaurado = np.clip(restaurado * 255, 0, 255)
            # Convertir a uint8 para guardar con OpenCV
            return restaurado.astype(np.uint8)

        canal_azul_restaurado  = restaurar_canal(canal_azul)
        canal_verde_restaurado = restaurar_canal(canal_verde)
        canal_rojo_restaurado  = restaurar_canal(canal_rojo)

        # Reconstruimos la imagen a color uniendo los tres canales restaurados
        resultado = cv2.merge([canal_azul_restaurado, canal_verde_restaurado, canal_rojo_restaurado])

        ruta_salida = "uploads/restaurada.jpg"

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
    
class AjustarBrilloProcessor:

    def __init__(self, brillo=30):
        self.brillo = brillo

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception("No se pudo leer la imagen")

        resultado = cv2.convertScaleAbs(img,alpha=1.0,beta=self.brillo)

        ruta_salida = "uploads/ajustar_brillo_result.jpg"

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
