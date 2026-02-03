BEGIN;

INSERT INTO inventory_movements (product_id, movement_type, quantity, reference) VALUES
(1, 'IN', 50, 'INITIAL_LOAD'),
(2, 'IN', 30, 'INITIAL_LOAD'),
(3, 'IN', 40, 'INITIAL_LOAD'),
(4, 'IN', 100, 'INITIAL_LOAD'),
(5, 'IN', 25, 'INITIAL_LOAD'),
(6, 'IN', 60, 'INITIAL_LOAD'),
(7, 'IN', 20, 'INITIAL_LOAD'),
(8, 'IN', 80, 'INITIAL_LOAD'),
(9, 'IN', 35, 'INITIAL_LOAD'),
(10,'IN', 90, 'INITIAL_LOAD');

COMMIT;
