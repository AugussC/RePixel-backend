# app/utils/user_utils.py

from app.utils.security import hash_password

def construir_campos_actualizacion(nombre, apellido, correo, contraseña, id_rol):
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
        fields.append("contrasena = %s")
        values.append(hash_password(contraseña))

    if id_rol:
        fields.append("id_rol = %s")
        values.append(id_rol)

    if not fields:
        raise ValueError("No se proporcionaron campos para actualizar")

    return fields, values