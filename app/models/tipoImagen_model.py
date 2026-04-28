from app.models.entidadBase import EntidadBase
class TipoImagen(EntidadBase):
    def __init__(self, id_tipo_imagen, nombreTipoImagen):
        super().__init__(id_tipo_imagen)
        self.nombreTipoImagen = nombreTipoImagen

    def to_dict(self):
        return {
            'id_tipo_imagen': self.id,
            'nombreTipoImagen': self.nombreTipoImagen
        }