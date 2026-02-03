BEGIN;

ALTER TABLE products
  ADD CONSTRAINT fk_products_category
  FOREIGN KEY (category_id) REFERENCES categories(category_id);

ALTER TABLE orders
  ADD CONSTRAINT fk_orders_customer
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE order_items
  ADD CONSTRAINT fk_items_order
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
  ON DELETE CASCADE;

ALTER TABLE order_items
  ADD CONSTRAINT fk_items_product
  FOREIGN KEY (product_id) REFERENCES products(product_id);

ALTER TABLE inventory_movements
  ADD CONSTRAINT fk_inventory_product
  FOREIGN KEY (product_id) REFERENCES products(product_id);

COMMIT;

BEGIN;

ALTER TABLE order_status_history
  ADD CONSTRAINT fk_order_status_history_order
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
  ON DELETE CASCADE;

COMMIT;
