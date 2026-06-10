from flask import Blueprint, jsonify, request, send_file, session
import os
from app.services.image_services import subir_imagen, obtener_imagen_por_id, obtener_imagenes_por_usuario, desactivar_imagen
from app.utils.image_utils import guardar_archivo, validar_imagen

image_routes = Blueprint("image_routes", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../../uploads"))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@image_routes.route("/images", methods=["POST"])
def subir():
    try:

        user_id = session.get("user_id")

        file, id_tipoimagen = validar_imagen(request.files) 

        filepath = guardar_archivo(file)

        image = subir_imagen(filepath, user_id, id_tipoimagen)

        return jsonify({
            "message": "OK",
            "id": image.id
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
        
@image_routes.route("/images/<id>/view")
def ver_imagen(id_imagen):

    image = obtener_imagen_por_id(int(id_imagen))

    print(image)

    if not image:
        return jsonify({
            "error": "Imagen no disponible"
        }), 404

    print("Ruta:", image.ruta)
    print("Ruta BD:", image.ruta)
    print("Existe:", os.path.exists(image.ruta))

    return send_file(image.ruta)



@image_routes.route("/images/<id>", methods=["GET"])
def obtener_imagen(id):

    image = obtener_imagen_por_id(int(id))

    if not image:
        return jsonify({"error": "No encontrada"}), 404

    return jsonify(image.to_dict()), 200

@image_routes.route("/users/<id_usuario>/images", methods=["GET"])
def obtener_imagenes_por_usuario_route(id_usuario):

    images = obtener_imagenes_por_usuario(int(id_usuario))

    if not images:
        return jsonify([]), 200

    return jsonify([img.to_dict() for img in images]), 200

@image_routes.route("/images/<id>/disable", methods=["PATCH"])
def desactivar_imagen_route(id):

    resultado = desactivar_imagen(int(id))

    if resultado == "NO_EXISTE":
        return jsonify({"error": "Imagen no encontrada"}), 404
    if resultado == "YA_DESACTIVADA":
        return jsonify({"error": "Imagen previamente eliminada"}), 409
    if resultado == "OK":
        return jsonify({"message": "Imagen desactivada"}), 200

    return jsonify({"error": "Error desconocido"}), 500


