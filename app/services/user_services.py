from app.models.rol_model import Rol  # Asegurate de tener este modelo importado
from app.models.user_model import User
from app.database.connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

 

def create_user(nombre, apellido, correo, contraseña, id_rol):
    connection = get_connection()
    if connection is None: return None

    try:
        # Forzamos el cursor de diccionario para que no falle el acceso por nombre
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # 1. Verificar si el usuario ya existe
        cursor.execute("SELECT id_usuario FROM Usuario WHERE correo = %s", (correo,))
        if cursor.fetchone():
            print("El correo ya existe.")
            return None

        # 2. Buscar el Rol
        cursor.execute("SELECT id_rol, nombre_rol FROM Rol WHERE id_rol = %s", (id_rol,))
        rol_data = cursor.fetchone()
        
        if not rol_data:
            print(f"El rol {id_rol} no existe.")
            return None
        
        # Como usamos RealDictCursor, esto ahora sí funciona:
        objeto_rol = Rol(rol_data['id_rol'], rol_data['nombre_rol'])

        # 3. Insertar
        hashed_password = generate_password_hash(contraseña)
        cursor.execute(
            """
            INSERT INTO Usuario (nombre, apellido, correo, contrasena, id_rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario
            """,
            (nombre, apellido, correo, hashed_password, id_rol)
        )

        # RETURNING devuelve una fila con el ID
        row = cursor.fetchone()
        user_id = row['id_usuario']
        
        connection.commit()
        return User(user_id, nombre, apellido, correo, hashed_password, objeto_rol)

    except Exception as e:
        if connection: connection.rollback()
        print(f"DEBUG ERROR: {e}")
        return None
    
    
def login_user(correo, password_plana):
    connection = get_connection()
    if connection is None: return None

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Buscamos al usuario y traemos también los datos de su rol (JOIN)
        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.correo = %s
        """
        cursor.execute(query, (correo,))
        user_data = cursor.fetchone()

        # Si no existe el usuario o la contraseña no coincide
        if not user_data or not check_password_hash(user_data['contrasena'], password_plana):
            print("Correo o contraseña incorrectos")
            return None

        # Creamos los objetos para retornar
        objeto_rol = Rol(user_data['id_rol'], user_data['nombre_rol'])
        user = User(
            user_data['id_usuario'], 
            user_data['nombre'], 
            user_data['apellido'], 
            user_data['correo'], 
            user_data['contrasena'], 
            objeto_rol
        )
        
        return user

    except Exception as e:
        print(f"Error en login_user: {e}")
        return None
    
def get_all_users():
    connection = get_connection()
    if connection is None: return []

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
        """
        cursor.execute(query)
        users_data = cursor.fetchall()

        users = []
        for user_data in users_data:
            objeto_rol = Rol(user_data['id_rol'], user_data['nombre_rol'])
            user = User(
                user_data['id_usuario'], 
                user_data['nombre'], 
                user_data['apellido'], 
                user_data['correo'], 
                user_data['contrasena'], 
                objeto_rol
            )
            users.append(user)

        return users

    except Exception as e:
        print(f"Error en get_all_users: {e}")
        return []
    
def get_user_by_id(user_id):
    connection = get_connection()
    if connection is None: return None
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            print(f"Usuario con ID {user_id} no encontrado")
            return None

        objeto_rol = Rol(user_data['id_rol'], user_data['nombre_rol'])
        user = User(
            user_data['id_usuario'], 
            user_data['nombre'], 
            user_data['apellido'], 
            user_data['correo'], 
            user_data['contrasena'], 
            objeto_rol
        )
        
        return user

    except Exception as e:
        print(f"Error en get_user_by_id: {e}")
        return None
    
def get_user_by_email(correo):
    connection = get_connection()
    if connection is None: return None
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT u.*, r.nombre_rol 
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.correo = %s
        """
        cursor.execute(query, (correo,))
        user_data = cursor.fetchone()

        if not user_data:
            print(f"Usuario con correo {correo} no encontrado")
            return None

        objeto_rol = Rol(user_data['id_rol'], user_data['nombre_rol'])
        user = User(
            user_data['id_usuario'], 
            user_data['nombre'], 
            user_data['apellido'], 
            user_data['correo'], 
            user_data['contrasena'], 
            objeto_rol
        )
        
        return user

    except Exception as e:
        print(f"Error en get_user_by_email: {e}")
        return None
    
def update_user(user_id, nombre=None, apellido=None, correo=None, contraseña=None, id_rol=None):
    connection = get_connection()
    if connection is None: return None

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        fields = []
        values = []

        if nombre:
            fields.append("nombre = %s")
            values.append(nombre)
        if apellido:
            fields.append("apellido = %s")
            values.append(apellido)
        if correo:
            fields.append("correo = %s")
            values.append(correo)
        if contraseña:
            hashed_password = generate_password_hash(contraseña)
            fields.append("contrasena = %s")
            values.append(hashed_password)
        if id_rol:
            fields.append("id_rol = %s")
            values.append(id_rol)

        if not fields:
            print("No se proporcionaron campos para actualizar.")
            return None

        values.append(user_id)


        query = f"UPDATE Usuario SET {', '.join(fields)} WHERE id_usuario = %s"
        cursor.execute(query, tuple(values))

        cursor.execute("""
            SELECT u.*, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (user_id,))

        updated_user_data = cursor.fetchone()

        if not updated_user_data:
            return None

        objeto_rol = Rol(updated_user_data['id_rol'], updated_user_data['nombre_rol'])

        updated_user = User(
            updated_user_data['id_usuario'], 
            updated_user_data['nombre'], 
            updated_user_data['apellido'], 
            updated_user_data['correo'], 
            updated_user_data['contrasena'], 
            objeto_rol
        )

        updated_user.estado = updated_user_data['estado']

        connection.commit()
        return updated_user

    except Exception as e:
        if connection: connection.rollback()
        print(f"Error en update_user: {e}")
        return None
    
def toggle_user_status(user_id):
    connection = get_connection()
    if connection is None: return None

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            UPDATE Usuario
            SET estado = NOT estado
            WHERE id_usuario = %s
        """, (user_id,))

        # 🔥 Ahora hacemos SELECT con JOIN (como los demás)
        cursor.execute("""
            SELECT u.*, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (user_id,))

        user_data = cursor.fetchone()

        if not user_data:
            return None

        objeto_rol = Rol(user_data['id_rol'], user_data['nombre_rol'])

        user = User(
            user_data['id_usuario'], 
            user_data['nombre'], 
            user_data['apellido'], 
            user_data['correo'], 
            user_data['contrasena'], 
            objeto_rol
        )

        user.estado = user_data['estado']

        connection.commit()
        return user

    except Exception as e:
        if connection: connection.rollback()
        print(e)
        return None