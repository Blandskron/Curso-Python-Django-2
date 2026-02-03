BEGIN;

CREATE OR REPLACE FUNCTION trg_log_order_created()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO order_status_history (order_id, from_status, to_status, changed_at, note)
  VALUES (NEW.order_id, NULL, NEW.status, NOW(), 'Order created');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_orders_created_history ON orders;
CREATE TRIGGER trg_orders_created_history
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION trg_log_order_created();

COMMIT;
