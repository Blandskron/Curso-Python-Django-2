CREATE TABLE direccion (
    id SERIAL PRIMARY KEY,
    calle VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL
);

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion_id INTEGER NOT NULL,
    CONSTRAINT fk_direccion
        FOREIGN KEY (direccion_id)
        REFERENCES direccion(id)
        ON DELETE RESTRICT
);

"""
TABLA DIRECCION
-------------------------------------
CALLE                   | CIUDAD
-------------------------------------
EVERGREEN TERRACE 742   | SPRINGFIELD
SIEMPRE VIVA 123        | SPRINGFIELD
"""