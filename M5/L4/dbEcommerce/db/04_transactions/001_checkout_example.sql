BEGIN;

-- Crear orden
INSERT INTO orders (customer_id, status)
VALUES (1, 'pending')
RETURNING order_id;

-- Supongamos order_id = 10

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
(10, 1, 2, 19990),
(10, 3, 1, 9990);

-- Confirmar pago (DISPARA DESCUENTO DE STOCK)
UPDATE orders
SET status = 'paid'
WHERE order_id = 10;

COMMIT;
