from app.services.user_services import (crear_usuario, iniciar_sesion_usuario, obtener_usuario_por_id)

def iniciar_sesion(correo, password):
    return iniciar_sesion_usuario(correo, password)


def registrar_usuario(nombre, apellido, correo, contraseña, id_rol):

    return crear_usuario(
        nombre,
        apellido,
        correo,
        contraseña,
        id_rol,
    )

def obtener_usuario_actual(user_id):

    return obtener_usuario_por_id(user_id)