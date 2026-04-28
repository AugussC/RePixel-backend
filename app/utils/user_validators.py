from flask import session

def validar_usuario_autenticado():

    user_id = session.get('user_id')

    if not user_id:
        raise PermissionError("No autorizado")

    return user_id

def validar_login_data(data):

    correo = data.get("correo")
    password = data.get("contraseña")

    if not correo or not password:
        raise ValueError("Correo y contraseña obligatorios")

    return correo, password


def validar_register_data(data):

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    id_rol = data.get("rol")

    if not all([nombre, apellido, correo, contraseña, id_rol]):
        raise ValueError("Todos los campos son obligatorios")

    return nombre, apellido, correo, contraseña, id_rol

def validar_usuario_autenticado():

    user_id = session.get("user_id")

    if not user_id:
        raise PermissionError("No autorizado")

    return user_id