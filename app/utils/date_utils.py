from datetime import datetime, timedelta

def obtener_fechas_expiracion(horas=12):
    fecha = datetime.now()
    expiracion = fecha + timedelta(hours=horas)
    return fecha, expiracion