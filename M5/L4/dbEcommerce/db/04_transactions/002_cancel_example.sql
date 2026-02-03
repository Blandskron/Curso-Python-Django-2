BEGIN;

UPDATE orders
SET status = 'cancelled'
WHERE order_id = 10;

-- (en este diseño simple no devolvemos stock,
-- si lo deseas se agrega trigger inverso)

COMMIT;
