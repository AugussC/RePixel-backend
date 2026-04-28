import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

connection = None

def abrir_conexion():
    global connection

    try:
        if connection is None:
            connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )

        return connection

    except Exception as e:
        print(f"ERROR DE CONEXIÓN: {e}")
        return None


def obtener_cursor():
    conexion = abrir_conexion()

    if conexion:
        return conexion.cursor(
            cursor_factory=RealDictCursor
        )

    return None


def cerrar_conexion():
    global connection

    if connection:
        connection.close()
        connection = None