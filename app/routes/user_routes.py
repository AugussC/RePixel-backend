from flask import Blueprint, jsonify, request
from app.services.user_services import obtener_usuario_por_email, obtener_usuario_por_id

user_routes = Blueprint("user_routes", __name__)



@user_routes.route("/users/<id>", methods=["GET"]) # Endpoint para obtener un usuario por su ID
def obtener_usuario_por_id_route(id):

    user = obtener_usuario_por_id(id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200


@user_routes.route("/users/email/<correo>", methods=["GET"]) # Endpoint para obtener un usuario por su correo electrónico
def obtener_usuario_por_email_route(correo):
    user = obtener_usuario_por_email(correo)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

