from flask import Blueprint, jsonify, request, send_file, session
from werkzeug.utils import secure_filename
import os

from app.services.image_services import subir_imagen, obtener_imagen_por_id, obtener_imagenes_por_usuario, desactivar_imagen
from app.services.user_services import obtener_usuario_por_id

image_routes = Blueprint("image_routes", __name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../../uploads"))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@image_routes.route("/images", methods=["POST"])
def subir():
    
    user_id = session.get('user_id') 
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

   
    current_user = obtener_usuario_por_id(user_id)
    
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    
    file = request.files['file']

    if file.filename == "":
        return jsonify({"error": "Nombre de archivo inválido"}), 400

    filename = file.filename.lower()

    tipos = {
        "png": 1,
        "jpg": 2,
        "jpeg": 3
    }

    ext = filename.split('.')[-1]

    if ext not in tipos:
        return jsonify({"error": "La imagen debe tener formato (JPG/PNG/JPEG)"}), 400

    id_tipoimagen = tipos[ext]
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > 5 * 1024 * 1024:
        return jsonify({"error": "Su imagen supera el límite de tamaño de 5MB"}), 400

    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    image = subir_imagen(filepath, current_user, id_tipoimagen)
    
    if image:
         return jsonify({"message": "OK", "id": image.id}), 201
    return jsonify({"error": "Ocurrió un error al intentar subir la imagen"}), 500

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