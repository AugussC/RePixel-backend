from flask import Blueprint, jsonify

from app.database.repositories.tipo_imagen_repository import (obtener_tipo_imagen_disponible)

tipo_imagen_routes = Blueprint("tipo_imagen_routes",__name__)

@tipo_imagen_routes.route("/images/tipos-imagen",methods=["GET"])
def obtener_tipos_imagen():
    tipos = obtener_tipo_imagen_disponible()
    return jsonify(tipos), 200

