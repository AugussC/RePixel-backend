from datetime import datetime, timedelta

def obtener_fechas_expiracion():
    fecha = datetime.now()
    expiracion = fecha + timedelta(hours=12)
    return fecha, expiracion