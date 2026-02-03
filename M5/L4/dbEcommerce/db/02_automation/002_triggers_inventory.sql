BEGIN;

CREATE OR REPLACE FUNCTION trg_discount_stock_on_paid()
RETURNS TRIGGER AS $$
DECLARE
  item RECORD;
  available INTEGER;
BEGIN
  IF NEW.status = 'paid' AND OLD.status <> 'paid' THEN
    FOR item IN
      SELECT product_id, quantity
      FROM order_items
      WHERE order_id = NEW.order_id
    LOOP
      available := fn_stock_available(item.product_id);

      IF available < item.quantity THEN
        RAISE EXCEPTION 'Stock insuficiente para producto %', item.product_id;
      END IF;

      INSERT INTO inventory_movements (
        product_id, movement_type, quantity, reference
      ) VALUES (
        item.product_id, 'OUT', item.quantity, 'ORDER:' || NEW.order_id
      );
    END LOOP;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_paid
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION trg_discount_stock_on_paid();

COMMIT;


BEGIN;

CREATE OR REPLACE FUNCTION trg_log_order_status_change()
RETURNS TRIGGER AS $$
BEGIN
  -- Solo cuando cambia el status
  IF TG_OP = 'UPDATE' AND NEW.status IS DISTINCT FROM OLD.status THEN
    INSERT INTO order_status_history (order_id, from_status, to_status, changed_at, note)
    VALUES (NEW.order_id, OLD.status, NEW.status, NOW(), NULL);
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_orders_status_history ON orders;
CREATE TRIGGER trg_orders_status_history
AFTER UPDATE OF status ON orders
FOR EACH ROW
EXECUTE FUNCTION trg_log_order_status_change();

COMMIT;
