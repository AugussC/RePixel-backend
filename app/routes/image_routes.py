from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename
import os

from app.services.image_services import upload_image, get_image_by_id, get_images_by_user_service, disable_image_service

image_routes = Blueprint("image_routes", __name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../../uploads"))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@image_routes.route("/images", methods=["POST"])
def upload_image_route():

    if 'file' not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nombre vacío"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)


    file.save(filepath)

    print("GUARDADO EN:", filepath)  #

    image = upload_image(filepath)

    if not image:
        return jsonify({"error": "Error al procesar imagen"}), 500

    return jsonify(image.to_dict()), 201

@image_routes.route("/images/<id>/view", methods=["GET"])
def view_image(id):

    image = get_image_by_id(int(id))

    if not image:
        return jsonify({"error": "Imagen no disponible"}), 404

    return send_file(image.ruta)



@image_routes.route("/images/<id>", methods=["GET"])
def get_image(id):

    image = get_image_by_id(id)

    if not image:
        return jsonify({"error": "No encontrada"}), 404

    return jsonify(image.to_dict()), 200

@image_routes.route("/users/<id_usuario>/images", methods=["GET"])
def get_images_by_user(id_usuario):

    images = get_images_by_user_service(int(id_usuario))

    if not images:
        return jsonify([]), 200

    return jsonify([img.to_dict() for img in images]), 200

@image_routes.route("/images/<id>/disable", methods=["PATCH"])
def disable_image(id):

    success = disable_image_service(int(id))

    if not success:
        return jsonify({"error": "No se pudo desactivar"}), 400

    return jsonify({"message": "Imagen desactivada"}), 200