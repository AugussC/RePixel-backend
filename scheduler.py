from apscheduler.schedulers.background import BackgroundScheduler
from app.database.connection import abrir_conexion
from datetime import datetime

def desactivar_imagenes_expiradas():
    try:
        # 🔹 Cada ejecución crea su propia conexión
        connection = abrir_conexion()
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE imagen
            SET estado = false
            WHERE fecha_expiracion <= NOW()
              AND estado = true
        """)
        connection.commit()
        print(f"[{datetime.now()}] Scheduler: imágenes expiradas desactivadas")
        
    except Exception as e:
        print("Error en scheduler:", e)
        # 🔹 Hacer rollback solo si la conexión está abierta
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