from flask import Blueprint, jsonify, request, send_file
from app.database.repositories.procesamiento_repository import obtener_procesamiento_por_id
from app.services.procesarImage_services import procesar_imagen_service

procesamiento_routes = Blueprint("procesamiento_routes", __name__)

@procesamiento_routes.route('/images/procesar-imagen/<id>', methods=['POST'])
def procesar_imagen(id):

    try:
        data = request.get_json()
        algoritmo = data.get("algoritmo")
        id_imagen = int(id)
        
        resultado = procesar_imagen_service(id_imagen, algoritmo)
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({
            "Ocurrio un error al procesar": str(e)
        }), 400

@procesamiento_routes.route("/images/procesamientos/<id>/view", methods=["GET"])
def ver_procesamiento(id):
    try:
        procesamiento = obtener_procesamiento_por_id(int(id))
        
        if not procesamiento:
            return jsonify({
                "error": "No encontrado"
            }), 404

        return send_file(procesamiento["ruta_resultado"])
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
