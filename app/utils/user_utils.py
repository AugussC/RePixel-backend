# app/utils/user_utils.py

from flask import session

def crear_sesion_usuario(user):

    session.clear()

    session["user_id"] = user.id
    session["user_nombre"] = user.nombre


def cerrar_sesion():

    session.clear()