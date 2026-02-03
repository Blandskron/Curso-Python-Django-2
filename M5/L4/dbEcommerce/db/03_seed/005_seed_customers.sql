BEGIN;

INSERT INTO customers (first_name, last_name, email, phone) VALUES
('Juan', 'Pérez', 'juan.perez@gmail.com', '+56911112222'),
('María', 'González', 'maria.gonzalez@gmail.com', '+56922223333'),
('Carlos', 'Ramírez', 'carlos.ramirez@gmail.com', '+56933334444'),
('Ana', 'Torres', 'ana.torres@gmail.com', '+56944445555'),
('Pedro', 'Muñoz', 'pedro.munoz@gmail.com', '+56955556666'),
('Laura', 'Fernández', 'laura.fernandez@gmail.com', '+56966667777'),
('Diego', 'Rojas', 'diego.rojas@gmail.com', '+56977778888'),
('Camila', 'Soto', 'camila.soto@gmail.com', '+56988889999');

COMMIT;
