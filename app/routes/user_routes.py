from flask import Blueprint, jsonify

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/users", methods=["GET"]) # Endpoint para obtener todos los usuarios

@user_routes.route("/users/<id>", methods=["GET"]) # Endpoint para obtener un usuario por su ID

@user_routes.route("/users/<id>", methods=["PUT"]) # Endpoint para actualizar un usuario por su ID

@user_routes.route("/users/<id>/status", methods=["PATCH"]) # Endpoint para actualizar parcialmente un usuario por su ID
def update_user_status(id):
    # Aquí puedes implementar la lógica para actualizar el estado del usuario, como activar o desactivar su cuenta
    return jsonify({"message": f"Estado del usuario con ID {id} actualizado exitosamente"}), 200