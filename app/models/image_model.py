from datetime import timedelta

from app.models.entidadBase import EntidadBase

class Image(EntidadBase):

    def __init__(self, id_image, altura, ancho, fecha_creacion,fecha_expiracion, peso_subida, ruta, id_tipoImagen, usuario):
        super().__init__(id_image)
        self.altura = altura
        self.ancho = ancho
        self.fecha_subida = fecha_creacion
        self.fecha_expiracion = fecha_expiracion
        self.peso_subida = peso_subida
        self.ruta = ruta
        self.id_tipoImagen = id_tipoImagen
        self.usuario = usuario

    def to_dict(self):
        return {
            'id_image': self.id,
            'altura': self.altura,
            'ancho': self.ancho,
            'fecha_subida': self.fecha_subida,
            'peso_subida': self.peso_subida,
            'ruta': self.ruta,
            'fecha_expiracion': self.fecha_expiracion,
            'id_tipoImagen': self.id_tipoImagen,
            'usuario': self.usuario.to_dict() if self.usuario else None,
            'estado': self.estado
        }