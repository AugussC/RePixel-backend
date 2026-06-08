from app.database.repositories.user_repository import  insertar_usuario_db, obtener_rol_por_id_db,  obtener_usuario_por_correo_db, obtener_usuario_por_id_db
from app.models.rol_model import Rol  
from app.models.user_model import User
from app.utils.security import hash_password, verify_password
from psycopg2.extras import RealDictCursor


 

def crear_usuario(nombre, apellido, correo, contraseña, id_rol):

    # 1. Validar que no exista el correo
    if obtener_usuario_por_correo_db(correo):
        return None  # o podrías lanzar error

    # 2. Obtener rol
    rol_data = obtener_rol_por_id_db(id_rol)
    if not rol_data:
        return None

    rol = Rol(rol_data['id_rol'], rol_data['nombre_rol'])

    # 3. Hash contraseña
    password_hash = hash_password(contraseña)

    # 4. Insertar usuario
    result = insertar_usuario_db(
        nombre, apellido, correo, password_hash, id_rol
    )

    # 5. Retornar objeto
    return User(
        result['id_usuario'],
        nombre,
        apellido,
        correo,
        password_hash,
        rol
    )
    
    
def iniciar_sesion_usuario(correo, contraseña_plana):

    user_data = obtener_usuario_por_correo_db(correo)
    if not user_data:
        return None

    if not verify_password(user_data['contraseña'], contraseña_plana):
        return None

    rol_data = obtener_rol_por_id_db(user_data['id_rol'])

    if not rol_data:
        return None

    rol = Rol(rol_data['id_rol'], rol_data['nombre_rol'])

    user = User(
        user_data['id_usuario'],
        user_data['nombre'],
        user_data['apellido'],
        user_data['correo'],
        user_data['contraseña'],
        rol
    )

    return user
    
    
def obtener_usuario_por_id(id_usuario):

    user_data = obtener_usuario_por_id_db(id_usuario)

    if not user_data:
        return None

    rol = Rol(user_data['id_rol'], user_data['nombre_rol'])

    user = User(
        user_data['id_usuario'],
        user_data['nombre'],
        user_data['apellido'],
        user_data['correo'],
        user_data['contraseña'],
        rol
    )
    user.estado = user_data['estado']

    return user

def obtener_usuario_por_email(correo):

    user_data = obtener_usuario_por_correo_db(correo)

    if not user_data:
        return None
    
    rol_data = obtener_rol_por_id_db(user_data['id_rol'])
    if not rol_data:
        return None
    
    rol = Rol(rol_data['id_rol'], rol_data['nombre_rol'])

    user = User(
        user_data['id_usuario'],
        user_data['nombre'],
        user_data['apellido'],
        user_data['correo'],
        user_data['contraseña'],
        rol
    )
    return user
    
