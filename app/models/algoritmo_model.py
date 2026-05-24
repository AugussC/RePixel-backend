from app.models.entidadBase import EntidadBase


class Algoritmo(EntidadBase):

    def __init__(self, id_algoritmo, nombre):

        super().__init__(id_algoritmo)
        self.nombre = nombre
        
    def to_dict(self):
        return {
            'id_algoritmo': self.id,
            'nombre': self.nombre,
            'estado': self.estado
        }