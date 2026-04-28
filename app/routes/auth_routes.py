from flask import Blueprint, jsonify, request, session
from app.services.user_services import crear_usuario, obtener_usuario_por_id,iniciar_sesion_usuario

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"]) # Endpoint para iniciar sesión
def iniciar_sesion():
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("contraseña")

    user = iniciar_sesion_usuario(correo, password)

    if user:
        session.clear() # Limpiamos cualquier sesión previa
        session["user_id"] = user.id
        session["user_nombre"] = user.nombre
        
        return jsonify({"message": "Login exitoso", "user": user.to_dict()}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401
    
@auth_routes.route("/register", methods=["POST"]) # Endpoint para registrar un nuevo usuario
def registrar():
    # Obtener los datos del usuario desde la solicitud
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    id_rol = data.get("rol")


    if not all([nombre, apellido, correo, contraseña, id_rol]): # Verificar que todos los campos sean proporcionados
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    

    user = crear_usuario(nombre, apellido, correo, contraseña, id_rol)

    # 5. Respuesta
    if user:
        return jsonify(user.to_dict()), 201
    else:
        return jsonify({"error": "Error al registrar el usuario"}), 500

@auth_routes.route("/logout", methods=["POST"]) # Endpoint para cerrar sesión
def deslogear():
    session.clear() # Borra toda la información de la sesión
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

@auth_routes.route('/me', methods=['GET'])
def obtener_usuario_actual():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(None), 200
    user = obtener_usuario_por_id(user_id)
    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "correo": user.correo
    })