from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

# Ruta de prueba
@api.route("/test", methods=["GET"])
def test():
    return jsonify({
        "status": "ok",
        "message": "Backend funcionando"
    })

# Ruta que recibe el botón
@api.route("/boton", methods=["POST"])
def boton():
    data = request.json

    print("Datos recibidos:", data)

    return jsonify({
        "status": "ok",
        "message": "Botón recibido correctamente"
    })