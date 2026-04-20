from flask import Blueprint, jsonify, request, session
# from app.services.auth_services import login_user, register_user
from app.services.user_services import create_user, login_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"]) # Endpoint para iniciar sesión
def login():
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("contraseña")

    user = login_user(correo, password)

    if user:
        # GUARDAMOS EN LA SESIÓN
        session.clear() # Limpiamos cualquier sesión previa
        session["user_id"] = user.id
        session["user_nombre"] = user.nombre
        
        return jsonify({"message": "Login exitoso", "user": user.to_dict()}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401
    
@auth_routes.route("/register", methods=["POST"]) # Endpoint para registrar un nuevo usuario
def register():
    # Obtener los datos del usuario desde la solicitud
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    id_rol = data.get("rol")


    if not all([nombre, apellido, correo, contraseña, id_rol]): # Verificar que todos los campos sean proporcionados
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    

    user = create_user(nombre, apellido, correo, contraseña, id_rol)

    # 5. Respuesta
    if user:
        return jsonify(user.to_dict()), 201
    else:
        return jsonify({"error": "Error al registrar el usuario"}), 500

@auth_routes.route("/logout", methods=["POST"]) # Endpoint para cerrar sesión
def logout():
    session.clear() # Borra toda la información de la sesión
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200