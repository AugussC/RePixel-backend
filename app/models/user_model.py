from app.models.entidadBase import EntidadBase
class User(EntidadBase):
    # Constructor de la clase User, es como mi Get en el frontend, es como mi plantilla para crear un nuevo usuario  
    def __init__(self, id_usuario, nombre, apellido, correo, contraseña, rol):
        super().__init__(id_usuario)
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol
        
    
    # Método para convertir el objeto User a un diccionario, es como mi Set en el frontend, es como mi plantilla para actualizar un usuario
    def to_dict(self):
        return {
            'id_usuario': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'rol': self.rol.to_dict() if self.rol else None
        }