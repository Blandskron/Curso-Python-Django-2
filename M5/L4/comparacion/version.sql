-- Crear tabla
CREATE TABLE persona (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    edad INTEGER NOT NULL
);

-- Insertar 3 personas (objetos en SQL)
INSERT INTO persona (id, nombre, apellido, edad) VALUES
(1, 'Juan', 'Perez', 30),
(2, 'Maria', 'Gonzalez', 25),
(3, 'Carlos', 'Rojas', 40);

"""
persona
id | nombre | apellido  | edad
1 | Juan   | Perez     | 30
2 | Maria  | Gonzalez  | 25
3 | Carlos | Rojas     | 40
"""
