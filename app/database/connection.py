import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv() # Cargar las variables de entorno desde el archivo .env

class DatabaseConnection:
    def __init__(self):# Constructor de la clase DatabaseConnection, inicializa la variable de conexión a None
        self.connection = None

    def connect(self):
        try:
            load_dotenv() # Forzamos la carga
            print(f"DEBUG: Intentando conectar a {os.getenv('DB_NAME')} con el usuario {os.getenv('DB_USER')}")
            
            self.connection = psycopg2.connect(
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

    def get_cursor(self):# Método para obtener un cursor de la conexión a la base de datos, utilizando RealDictCursor para obtener resultados como diccionarios
        return self.connection.cursor(cursor_factory=RealDictCursor)
    
    def get_connection(self): # Método para obtener la conexión a la base de datos, si no existe, se establece una nueva conexión
        if self.connection is None:
            self.connect()
        return self.connection
    
    import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv() 

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self): 
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            return self.connection
        except Exception as e: 
            print(f"Error: {e}")
            return None

    def get_cursor(self):
        return self.connection.cursor(cursor_factory=RealDictCursor)
    
    def get_connection(self):
        if self.connection is None:
            self.connect()  
        return self.connection

# --- AGREGÁ ESTO AL FINAL DEL ARCHIVO (FUERA DE LA CLASE) ---

# Creamos una instancia global de la conexión
_db_instance = DatabaseConnection()

# Creamos la FUNCIÓN que tus otros archivos quieren importar
def get_connection():
    return _db_instance.get_connection()