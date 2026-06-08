from apscheduler.schedulers.background import BackgroundScheduler
from app.database.connection import abrir_conexion
from datetime import datetime

def desactivar_imagenes_expiradas():
    try:
        connection = abrir_conexion()
        cursor = connection.cursor()
        
        cursor.execute(
           "CALL desactivar_imagenes_expiradas();"
        )
        connection.commit()
        print(f"[{datetime.now()}] Scheduler: imágenes expiradas desactivadas")
        
    except Exception as e:
        print("Error en scheduler:", e)
        if 'connection' in locals() and connection and not connection.closed:
            try:
                connection.rollback()
            except:
                pass


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        desactivar_imagenes_expiradas,
        "interval",
        minutes=1
    )
    scheduler.start()