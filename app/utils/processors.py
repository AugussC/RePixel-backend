
# processors/sharpen_processor.py

import cv2
import numpy as np

class EnfocarProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        blur = cv2.GaussianBlur(
            img,
            (9, 9),
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

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida


class QuitarRuidoProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception("No se pudo cargar la imagen")

        resultado = cv2.fastNlMeansDenoisingColored(
            img,
            None,
            10,
            10,
            7,
            21
        )

        ruta_salida = "uploads/sin_ruido_result.jpg"

        cv2.imwrite(
            ruta_salida,
            resultado
        )


        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
    
class BlancoNegroProcessor:

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception(
                "No se pudo leer la imagen"
            )

        resultado = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        ruta_salida = ("uploads/blanco_negro.jpg")

        cv2.imwrite(ruta_salida,resultado)

        return ruta_salida
    
class RestaurarImagenProcessor:

    def detectar_angulo_blur(self, img):

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray,50,150)

        lines = cv2.HoughLinesP(edges,1,np.pi/180,80,minLineLength=40,maxLineGap=10)

        if lines is None:
            return 0

        angulos = []

        for line in lines:

            x1,y1,x2,y2 = line[0]

            angulo = np.degrees(
                np.arctan2(
                    y2-y1,
                    x2-x1
                )
            )

            angulos.append(
                angulo
            )

        return np.median(
            angulos
        )



    def crear_kernel_movimiento(
        self,
        longitud,
        angulo
    ):

        kernel = np.zeros(
            (longitud,longitud),
            dtype=np.float32
        )

        kernel[
            longitud//2,
            :
        ] = 1

        centro = (
            longitud/2,
            longitud/2
        )

        M = cv2.getRotationMatrix2D(
            centro,
            angulo,
            1
        )

        kernel = cv2.warpAffine(
            kernel,
            M,
            (longitud,longitud)
        )

        kernel /= np.sum(kernel)

        return kernel



    def richardson_lucy(
        self,
        img,
        kernel,
        iteraciones=40
    ):

        img = img.astype(
            np.float32
        )/255.0

        estimacion = img.copy()

        kernel_flip = cv2.flip(
            kernel,
            -1
        )

        eps = 1e-8

        for _ in range(iteraciones):

            conv = cv2.filter2D(
                estimacion,
                -1,
                kernel
            )

            ratio = img/(conv+eps)

            correction = cv2.filter2D(
                ratio,
                -1,
                kernel_flip
            )

            estimacion *= correction

        estimacion = np.clip(
            estimacion,
            0,
            1
        )

        return (
            estimacion*255
        ).astype(np.uint8)



    def mejorar_contraste(
        self,
        img
    ):

        lab = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2LAB
        )

        l,a,b = cv2.split(
            lab
        )

        clahe = cv2.createCLAHE(
            clipLimit=3,
            tileGridSize=(8,8)
        )

        l = clahe.apply(
            l
        )

        lab = cv2.merge(
            [l,a,b]
        )

        return cv2.cvtColor(
            lab,
            cv2.COLOR_LAB2BGR
        )



    def sharpen(
        self,
        img
    ):

        gaussian = cv2.GaussianBlur(
            img,
            (0,0),
            2
        )

        return cv2.addWeighted(
            img,
            1.8,
            gaussian,
            -0.8,
            0
        )



    def procesar(
        self,
        ruta
    ):

        img = cv2.imread(
            ruta
        )

        if img is None:
            raise Exception(
                "Error cargando imagen"
            )

        angulo = self.detectar_angulo_blur(
            img
        )

        kernel = self.crear_kernel_movimiento(
            longitud=25,
            angulo=angulo
        )

        canales=[]

        for i in range(3):  

            canal = self.richardson_lucy(
                img[:,:,i],
                kernel,
                iteraciones=50
            )

            canales.append(
                canal
            )

        resultado = cv2.merge(canales)

        resultado = cv2.fastNlMeansDenoisingColored(resultado,None,4,4,7,21)

        resultado = self.mejorar_contraste(resultado)

        resultado = self.sharpen(resultado)

        cv2.imwrite("uploads/restaurada.jpg",resultado)

        return "uploads/restaurada.jpg"

class AjustarBrilloProcessor:

    def __init__(self, brillo=30):
        self.brillo = brillo

    def procesar(self, ruta):

        img = cv2.imread(ruta)

        if img is None:
            raise Exception("No se pudo leer la imagen")

        resultado = cv2.convertScaleAbs(
            img,
            alpha=1.0,
            beta=self.brillo
        )

        ruta_salida = "uploads/ajustar_brillo_result.jpg"

        cv2.imwrite(
            ruta_salida,
            resultado
        )

        return ruta_salida
