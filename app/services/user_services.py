from app.database.repositories.user_repository import actualizar_usuario_db, cambiar_estado_usuario_db, insertar_usuario_db, obtener_rol_por_id_db, obtener_todos_los_usuarios_db, obtener_usuario_por_correo_db, obtener_usuario_por_id_db
from app.models.rol_model import Rol  # Asegurate de tener este modelo importado
from app.models.user_model import User
from app.database.connection import abrir_conexion
from app.utils.security import hash_password, verify_password
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from app.utils.user_utils import construir_campos_actualizacion

 

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
    
    
def iniciar_sesion_usuario(correo, password_plana):

    user_data = obtener_usuario_por_correo_db(correo)
    if not user_data:
        return None

    if not verify_password(user_data['contraseña'], password_plana):
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
    
def obtener_todos_los_usuarios():

    users_data = obtener_todos_los_usuarios_db()
    
    users = []

    for user_data in users_data:
        rol = Rol(user_data['id_rol'], user_data['nombre_rol'])

        user = User(
            user_data['id_usuario'],
            user_data['nombre'],
            user_data['apellido'],
            user_data['correo'],
            user_data['contraseña'],
            rol,
        )
        user.estado = user_data['estado']
        users.append(user)

    return users
    
def obtener_usuario_por_id(user_id):

    user_data = obtener_usuario_por_id_db(user_id)

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

def actualizar_usuario(user_id, nombre=None, apellido=None, correo=None, contraseña=None, id_rol=None):

    # 1. Construir campos (validaciones incluidas)
    fields, values = construir_campos_actualizacion(
        nombre, apellido, correo, contraseña, id_rol
    )

    # 2. Ejecutar update
    updated_user_data = actualizar_usuario_db(user_id, fields, values)

    if not updated_user_data:
        return None

    # 3. Mapear resultado
    rol = Rol(updated_user_data['id_rol'], updated_user_data['nombre_rol'])

    user = User(
        updated_user_data['id_usuario'],
        updated_user_data['nombre'],
        updated_user_data['apellido'],
        updated_user_data['correo'],
        updated_user_data['contraseña'],
        rol
    )

    user.estado = updated_user_data['estado']

    return user
    
def cambio_estado(user_id):

    # 1. Ejecutar cambio
    user_data = cambiar_estado_usuario_db(user_id)

    if not user_data:
        return None

    # 2. Mapear
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