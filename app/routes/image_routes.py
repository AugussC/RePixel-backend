from flask import Blueprint, jsonify, request, send_file, session
from werkzeug.utils import secure_filename
import os

from app.services.image_services import subir_imagen, obtener_imagen_por_id, obtener_imagenes_por_usuario, desactivar_imagen
from app.services.user_services import obtener_usuario_por_id
from app.utils.image_utils import guardar_archivo
from app.utils.imagen_validators import validar_archivo_en_request, validar_extension_archivo, validar_nombre_archivo, validar_tamano_archivo
from app.utils.user_validators import validar_usuario_autenticado

image_routes = Blueprint("image_routes", __name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../../uploads"))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@image_routes.route("/images", methods=["POST"])
def subir():
    try:

        # 1. Usuario autenticado
        user_id = validar_usuario_autenticado()
        current_user = obtener_usuario_por_id(user_id)


        # 2. Validaciones archivo
        file = validar_archivo_en_request(request.files)

        validar_nombre_archivo(file)

        id_tipoimagen = validar_extension_archivo(file.filename)

        validar_tamano_archivo(file)

        # 3. Guardar archivo
        filepath = guardar_archivo(file)

        # 4. Subir imagen
        image = subir_imagen(filepath, current_user, id_tipoimagen)

        return jsonify({
            "message": "OK",
            "id": image.id
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception:

        return jsonify({
            "error": "Ocurrió un error al intentar subir la imagen"
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