BEGIN;

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_inventory_product ON inventory_movements(product_id);

COMMIT;

BEGIN;

CREATE INDEX idx_order_status_history_order ON order_status_history(order_id);
CREATE INDEX idx_order_status_history_changed_at ON order_status_history(changed_at);

COMMIT;
