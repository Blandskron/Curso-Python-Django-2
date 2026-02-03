BEGIN;

INSERT INTO products (category_id, name, description, price) VALUES
-- Electrónica
(1, 'Auriculares Bluetooth Pro X', 'Auriculares inalámbricos con cancelación de ruido y estuche de carga', 49990),
(1, 'Smartwatch Fit Pulse', 'Reloj inteligente con monitor de ritmo cardíaco y oxígeno en sangre', 69990),
(1, 'Teclado Mecánico RGB', 'Teclado mecánico switches blue con iluminación RGB', 45990),

-- Ropa
(2, 'Polera Algodón Premium', 'Polera 100% algodón, corte regular', 14990),
(2, 'Chaqueta Impermeable Urbana', 'Chaqueta resistente al agua para uso diario', 59990),

-- Hogar
(3, 'Lámpara LED de Escritorio', 'Lámpara LED con brillo regulable y puerto USB', 29990),
(3, 'Set de Sartenes Antiadherentes', 'Set de 3 sartenes con recubrimiento antiadherente', 74990),

-- Libros
(4, 'Introducción a la Programación', 'Libro básico para aprender programación desde cero', 19990),
(4, 'Diseño de Sistemas Modernos', 'Arquitectura de software y sistemas escalables', 34990),
(4, 'Hábitos Atómicos', 'Guía práctica para construir hábitos positivos', 17990);

COMMIT;
