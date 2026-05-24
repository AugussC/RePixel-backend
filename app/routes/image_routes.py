from flask import Blueprint, jsonify, request, send_file, session
import os
from app.database.repositories.procesamiento_repository import obtener_procesamiento_por_id
from app.database.repositories.procesamiento_repository import obtener_procesamiento_por_id
from app.services.image_services import subir_imagen, obtener_imagen_por_id, obtener_imagenes_por_usuario, desactivar_imagen
from app.database.repositories.image_repository import obtener_tipo_imagen_disponible
from app.utils.image_utils import guardar_archivo, validar_imagen
from app.services.procesarImage_services import procesar_imagen_service

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
        
@image_routes.route("/images/<id>/view", methods=["GET"])
def view_image(id):

    image = obtener_imagen_por_id(int(id))

    if not image:
        return jsonify({"error": "Imagen no disponible"}), 404

    return send_file(image.ruta)



@image_routes.route("/images/<id>", methods=["GET"])
def get_image(id):

    image = obtener_imagen_por_id(int(id))

    if not image:
        return jsonify({"error": "No encontrada"}), 404

    return jsonify(image.to_dict()), 200

@image_routes.route("/users/<id_usuario>/images", methods=["GET"])
def get_images_by_user(id_usuario):

    images = obtener_imagenes_por_usuario(int(id_usuario))

    if not images:
        return jsonify([]), 200

    return jsonify([img.to_dict() for img in images]), 200

@image_routes.route("/images/<id>/disable", methods=["PATCH"])
def disable_image(id):

    success = desactivar_imagen(int(id))

    if not success:
        return jsonify({"error": "No se pudo desactivar"}), 400

    return jsonify({"message": "Imagen desactivada"}), 200

@image_routes.route('/images/tipos-imagen', methods=['GET'])
def obtener_tipos_imagen():
    tipos = obtener_tipo_imagen_disponible()
    return jsonify(tipos), 200

@image_routes.route('/images/procesar-imagen/<id>', methods=['POST'])
def procesar_imagen(id):
    data = request.get_json()

    algoritmo = data.get("algoritmo")

    resultado = procesar_imagen_service(
        id_imagen=id,
        algoritmo=algoritmo
    )

    return jsonify(resultado), 200

@image_routes.route("/images/procesamientos/<id>/view",methods=["GET"])
def ver_procesamiento(id):

    procesamiento = obtener_procesamiento_por_id(id)

    if not procesamiento:
        return jsonify({
            "error": "No encontrado"
        }), 404

    return send_file(procesamiento["ruta_resultado"])