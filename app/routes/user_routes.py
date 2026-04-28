from flask import Blueprint, jsonify, request
from app.services.user_services import obtener_todos_los_usuarios, actualizar_usuario,obtener_usuario_por_email,cambio_estado, obtener_usuario_por_id

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/allusers", methods=["GET"]) # Endpoint para obtener todos los usuarios
def obtener_todos_los_usuarios_route():

    users = obtener_todos_los_usuarios()

    if not users:
        return jsonify({"message": "No hay usuarios"}), 404

    return jsonify([user.to_dict() for user in users]), 200

@user_routes.route("/users/<id>", methods=["GET"]) # Endpoint para obtener un usuario por su ID
def obtener_usuario_por_id_route(id):

    user = obtener_usuario_por_id(id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

@user_routes.route("/users/<id>", methods=["PUT"]) # Endpoint para actualizar completamente un usuario por su ID
def update_user_route(id):
    

    data = request.get_json()

    updated_user = actualizar_usuario(
        id,
        nombre=data.get("nombre"),
        apellido=data.get("apellido"),
        correo=data.get("correo"),
        contraseña=data.get("contraseña"),
        id_rol=data.get("id_rol")
    )

    if not updated_user:
        return jsonify({"error": "No se pudo actualizar"}), 400

    return jsonify(updated_user.to_dict()), 200

@user_routes.route("/users/<id>/status", methods=["PATCH"]) # Endpoint para alternar el estado activo/inactivo de un usuario por su ID
def cambio_estado_route(id):

    user = cambio_estado(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

@user_routes.route("/users/email/<correo>", methods=["GET"]) # Endpoint para obtener un usuario por su correo electrónico
def obtener_usuario_por_email_route(correo):
    user = obtener_usuario_por_email(correo)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

