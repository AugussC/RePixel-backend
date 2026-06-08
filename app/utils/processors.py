
import cv2
import numpy as np
import os

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

    def detectar_angulo_blur_robusto(self, img):
        # Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Redimensionar la imagen para el análisis de orientación.
        h, w = gray.shape
        max_dim = 600
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # Intento 1: Hough Lines tradicional modificado
        edges = cv2.Canny(gray, 30, 100)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=5)
        
        if lines is not None:
            angulos = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angulo = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                angulos.append(angulo)
            return float(np.median(angulos))
        
        # Intento 2: Análisis de orientación por gradiente (Sobel)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calcular los componentes de la matriz de estructura
        gxx = gx ** 2
        gyy = gy ** 2
        gxy = gx * gy
        
        # Suavizar para promediar localmente
        gxx = cv2.GaussianBlur(gxx, (11, 11), 0)
        gyy = cv2.GaussianBlur(gyy, (11, 11), 0)
        gxy = cv2.GaussianBlur(gxy, (11, 11), 0)
        
        # Evitar divisiones por cero
        denom = gxx - gyy
        denom[denom == 0] = 1e-6
        
        angle_rad = 0.5 * np.arctan2(2 * gxy, gxx - gyy)
        # El movimiento es perpendicular al gradiente predominante
        angulo_estimado = np.degrees(np.median(angle_rad)) + 90
        
        return float(angulo_estimado)

    def crear_kernel_movimiento(self, longitud, angulo):
        if longitud < 3:
            longitud = 3
        if longitud % 2 == 0:
            longitud += 1  

        kernel = np.zeros((longitud, longitud), dtype=np.float32)
        centro = longitud // 2

        # Calcular los extremos exactos de la línea de desenfoque
        angulo_rad = np.radians(angulo)
        dx = (longitud - 1) / 2.0 * np.cos(angulo_rad)
        dy = (longitud - 1) / 2.0 * np.sin(angulo_rad)

        x1 = int(round(centro - dx))
        y1 = int(round(centro - dy))
        x2 = int(round(centro + dx))
        y2 = int(round(centro + dy))

        # Dibujar una línea limpia con suavizado (anti-aliasing) para evitar artefactos de pixelación
        cv2.line(kernel, (x1, y1), (x2, y2), 1.0, thickness=1, lineType=cv2.LINE_AA)
        
        # Normalizar para mantener la energía/brillo de la imagen original
        suma = np.sum(kernel)
        if suma > 0:
            kernel /= suma
            
        return kernel

    def richardson_lucy_regularizado(self, img, kernel, tikhonov_alpha=0.0005, iteraciones=20):
        img = img.astype(np.float32) / 255.0
        estimacion = img.copy()
        kernel_flip = cv2.flip(kernel, -1)
        eps = 1e-6

        for _ in range(iteraciones):
            conv = cv2.filter2D(estimacion, -1, kernel)
            conv = np.clip(conv, eps, None)
            
            ratio = img / conv
            correction = cv2.filter2D(ratio, -1, kernel_flip)
            
            # Aplicar corrección a la estimación
            estimacion *= correction
            
            # Regularización suave de Tikhonov (evita la amplificación destructiva del ruido)
            if tikhonov_alpha > 0:
                laplacian = cv2.Laplacian(estimacion, cv2.CV_32F)
                estimacion += tikhonov_alpha * laplacian
                
            estimacion = np.clip(estimacion, 0, 1)

        return (estimacion * 255).astype(np.uint8)

    def mejorar_contraste_local(self, img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Mejorar contraste local con CLAHE en la luminancia
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def unsharp_mask(self, img, sigma=1.0, amount=1.5):
        gaussian = cv2.GaussianBlur(img, (0, 0), sigma)
        sharp = cv2.addWeighted(img, 1.0 + amount, gaussian, -amount, 0)
        return np.clip(sharp, 0, 255).astype(np.uint8)

    def procesar(self, ruta_entrada, ruta_salida=None, longitud_blur=35, angulo_fijo=None):
        img = cv2.imread(ruta_entrada)
        if img is None:
            raise Exception("No se pudo cargar la imagen de entrada")

        # Generar ruta de salida dinámica única para evitar colisiones de archivos entre peticiones
        if ruta_salida is None:
            nombre_base = os.path.basename(ruta_entrada)
            nombre, ext = os.path.splitext(nombre_base)
            dir_salida = os.path.dirname(ruta_entrada)
            ruta_salida = os.path.join(dir_salida, f"{nombre}_restaurada{ext}")

        # 1. Filtro Bilateral ultra rápido (en lugar de Non-Local Means que tarda segundos en CPU)
        # Reduce el ruido en áreas planas de la imagen preservando perfectamente los bordes
        img_denoise = cv2.bilateralFilter(img, d=5, sigmaColor=15, sigmaSpace=15)

        # 2. Determinar el ángulo del blur de movimiento
        if angulo_fijo is not None:
            angulo = angulo_fijo
        else:
            angulo = self.detectar_angulo_blur_robusto(img_denoise)
        
        print(f"[INFO] Ángulo de procesamiento estimado: {angulo}°")

        # 3. Construir la PSF (Kernel de movimiento de alta calidad)
        kernel = self.crear_kernel_movimiento(longitud=longitud_blur, angulo=angulo)

        # 4. Deconvolución ultra optimizada (Solo en el canal de Luminancia L)
        lab = cv2.cvtColor(img_denoise, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Richardson-Lucy en la luminancia
        l_deblur = self.richardson_lucy_regularizado(
            l, 
            kernel, 
            iteraciones=20, # 20 iteraciones son más que suficientes y rápidas en L
            tikhonov_alpha=0.0005
        )
        
        # Combinar de nuevo los canales
        resultado = cv2.merge([l_deblur, a, b])
        resultado = cv2.cvtColor(resultado, cv2.COLOR_LAB2BGR)

        # 5. Post-procesamiento estético controlado
        resultado = self.mejorar_contraste_local(resultado)
        resultado = self.unsharp_mask(resultado, sigma=1.0, amount=0.6)

        cv2.imwrite(ruta_salida, resultado)
        return ruta_salida

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
