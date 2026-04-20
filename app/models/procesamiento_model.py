
from app.models.entidadBase import EntidadBase


class Procesamiento(EntidadBase):
    def __init__(self, id_procesamiento, estado, fecha_procesamiento, Imagen):
        super().__init__(id_procesamiento)
        self.estado = estado
        self.fecha_procesamiento = fecha_procesamiento
        self.Imagen = Imagen
        
    def to_dict(self):
        return {
            "id_procesamiento": self.id,
            "estado": self.estado,
            "fecha_procesamiento": self.fecha_procesamiento,
            "Imagen": self.Imagen.to_dict() if self.Imagen else None
        }
        