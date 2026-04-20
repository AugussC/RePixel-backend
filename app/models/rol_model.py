from app.models.entidadBase import EntidadBase


class Rol(EntidadBase):
    def __init__(self, id_rol, nombre):
        super().__init__(id_rol)
        self.nombre = nombre
        
        
    def to_dict(self):
        return {
            'id_rol': self.id,
            'nombre': self.nombre
        }