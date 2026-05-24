"""
# processors/sharpen_processor.py

import cv2
import numpy as np

class MejorarResolucionProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        kernel = np.array([
            [0, -0.5, 0],
            [-0.5, 3, -0.5],
            [0, -0.5, 0]
        ])
        resultado = cv2.filter2D(
            img,
            -1,
            kernel
        )

        ruta_salida = "uploads/mejorar_resolucion_result.jpg"

        cv2.imwrite(ruta_salida, resultado)

        return ruta_salida
"""    

import cv2

class MejorarResolucionProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        blur = cv2.GaussianBlur(
            img,
            (9,9),
            2
        )

        resultado = cv2.addWeighted(
            img,
            1.3,
            blur,
            -0.3,
            0
        )

        ruta_salida = "uploads/mejorar_resolucion_result.jpg"

        cv2.imwrite(
            ruta_salida,
            resultado
        )

        return ruta_salida
