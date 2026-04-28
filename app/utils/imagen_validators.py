MAX_SIZE = 5 * 1024 * 1024

TIPOS_IMAGEN = {
    "png": 1,
    "jpg": 2,
    "jpeg": 3
}

def validar_archivo_en_request(files):

    if 'file' not in files:
        raise ValueError("No se envió ningún archivo")

    return files['file']


def validar_nombre_archivo(file):

    if file.filename == "":
        raise ValueError("Nombre de archivo inválido")


def validar_extension_archivo(filename):

    ext = filename.lower().split('.')[-1]

    if ext not in TIPOS_IMAGEN:
        raise ValueError("La imagen debe tener formato (JPG/PNG/JPEG)")

    return TIPOS_IMAGEN[ext]


def validar_tamano_archivo(file):

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)

    if size > MAX_SIZE:
        raise ValueError("Su imagen supera el límite de tamaño de 5MB")