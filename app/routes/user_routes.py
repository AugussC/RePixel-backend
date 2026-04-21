from flask import Blueprint, jsonify, request
from app.services.user_services import get_all_users, update_user,get_user_by_id,toggle_user_status, get_user_by_email

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/allusers", methods=["GET"]) # Endpoint para obtener todos los usuarios
def get_all_users_route():

    users = get_all_users()

    if not users:
        return jsonify({"message": "No hay usuarios"}), 404

    return jsonify([user.to_dict() for user in users]), 200

@user_routes.route("/users/<id>", methods=["GET"]) # Endpoint para obtener un usuario por su ID
def get_user(id):

    user = get_user_by_id(id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

@user_routes.route("/users/<id>", methods=["PUT"]) # Endpoint para actualizar completamente un usuario por su ID
def update_user_route(id):
    

    data = request.get_json()

    updated_user = update_user(
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
def toggle_user_status_route(id):

    user = toggle_user_status(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

@user_routes.route("/users/email/<correo>", methods=["GET"]) # Endpoint para obtener un usuario por su correo electrónico
def get_user_by_email_route(correo):
    user = get_user_by_email(correo)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

# Este endpoint es solo para pruebas, para verificar que la comunicación entre el frontend y el backend funciona correctamente. 
"""""
@user_routes.route("/boton", methods=["POST"])
def boton_test():
    from flask import request, jsonify

    data = request.get_json()

    print(data)  # opcional para ver en consola

    return jsonify({
        "status": "ok",
        "message": "Botón recibido en el backend 🚀"
    }), 200
"""