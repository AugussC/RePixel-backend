"""Archivo de inicialización de la base de datos para la aplicación RePixel.""
## 1. Tabla Rol (Padre de Usuario)
CREATE TABLE Rol (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

## 2. Tabla Tipo (Padre de Imagen)
CREATE TABLE Tipo (
    id_tipoImagen SERIAL PRIMARY KEY,
    nombre_tipoImagen VARCHAR(50) NOT NULL
);

## 3. Tabla Usuario (Hija de Rol, Padre de Imagen)
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INTEGER NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

## 4. Tabla Imagen (Hija de Tipo y Usuario, Padre de Procesamiento)
CREATE TABLE Imagen (
    id_imagen SERIAL PRIMARY KEY,
    altura INTEGER NOT NULL,
    ancho INTEGER NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    peso_subida DECIMAL(10, 2), -- Ejemplo: en KB o MB
    fecha_expiracion TIMESTAMP,
    id_tipoImagen INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    CONSTRAINT fk_imagen_tipo FOREIGN KEY (id_tipoImagen) REFERENCES Tipo(id_tipoImagen),
    CONSTRAINT fk_imagen_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

## 5. Tabla Procesamiento (Hija de Imagen)
CREATE TABLE Procesamiento (
    id_procesamiento SERIAL PRIMARY KEY,
    estado VARCHAR(50) NOT NULL,
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_imagen INTEGER NOT NULL,
    CONSTRAINT fk_procesamiento_imagen FOREIGN KEY (id_imagen) REFERENCES Imagen(id_imagen)
);
"""