import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv() # Cargar las variables de entorno desde el archivo .env

class ConexionBaseDeDatos:
    def __init__(self):# Constructor de la clase ConexionBaseDeDatos, inicializa la variable de conexión a None
        self.connection = None

    def conectar(self):
        try:
            load_dotenv() # Forzamos la carga
            print(f"DEBUG: Intentando conectar a {os.getenv('DB_NAME')} con el usuario {os.getenv('DB_USER')}")
            
            self.connection = psycopg2.conectar(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            return self.connection
        except Exception as e:
            print(f"--- ERROR REAL DE CONEXIÓN ---: {e}") # ESTO TE DIRÁ POR QUÉ FALLA
            return None

    def obtener_cursor(self):# Método para obtener un cursor de la conexión a la base de datos, utilizando RealDictCursor para obtener resultados como diccionarios
        return self.connection.cursor(cursor_factory=RealDictCursor)
    
    def abrir_connection(self): # Método para obtener la conexión a la base de datos, si no existe, se establece una nueva conexión
        if self.connection is None:
            self.conectar()
        return self.connection
    
    def cerrar_conexion(self): # Método para cerrar la conexión a la base de datos, si existe
        if self.connection:
            self.connection.close()
            self.connection = None