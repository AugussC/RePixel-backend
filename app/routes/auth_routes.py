from flask import Blueprint, jsonify, request, session
from app.services.auth_services import login_usuario, registrar_usuario, obtener_usuario_actual
from app.utils.user_utils import crear_sesion_usuario, cerrar_sesion
from app.utils.user_validators import validar_login_data, validar_register_data

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"]) # Endpoint para iniciar sesión
def iniciar_sesion():
    try:
        data = request.get_json()
        correo, password = validar_login_data(data)
    
        user = login_usuario(correo, password) 
        if not user:
            return jsonify({
                "error": "Credenciales inválidas"
            }), 401

        crear_sesion_usuario(user) 

        return jsonify({
            "message": "Login exitoso",
            "user": user.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception:

        return jsonify({
            "error": "Error interno del servidor"
        }), 500

    
@auth_routes.route("/register", methods=["POST"]) # Endpoint para registrar un nuevo usuario
def registrar():
    try:
        data = request.get_json()
        nombre, apellido, correo, contraseña, id_rol = validar_register_data(data)

        user = registrar_usuario(
            nombre,
            apellido,
            correo,
            contraseña,
            id_rol
        )

        if not user:
            return jsonify({
                "error": "Error al registrar el usuario"
            }), 500

        return jsonify(user.to_dict()), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception:

        return jsonify({
            "error": "Error interno del servidor"
        }), 500


@auth_routes.route("/logout", methods=["POST"]) # Endpoint para cerrar sesión
def deslogear():

    cerrar_sesion()

    return jsonify({
        "message": "Sesión cerrada exitosamente"
    }), 200

@auth_routes.route('/me', methods=['GET'])
def obtener_usuario_actual():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify(None), 200

    user = obtener_usuario_actual(user_id)

    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "correo": user.correo
    })