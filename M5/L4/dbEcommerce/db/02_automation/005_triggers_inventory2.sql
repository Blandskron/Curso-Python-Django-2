BEGIN;

-- 1) Descuenta stock al pasar a PAID (igual que antes)
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
        RAISE EXCEPTION 'Stock insuficiente para producto % (disponible %, requerido %)',
          item.product_id, available, item.quantity;
      END IF;

      INSERT INTO inventory_movements (product_id, movement_type, quantity, reference)
      VALUES (item.product_id, 'OUT', item.quantity, 'ORDER:' || NEW.order_id);
    END LOOP;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- 2) Devuelve stock al pasar de PAID -> CANCELLED
CREATE OR REPLACE FUNCTION trg_restore_stock_on_cancel()
RETURNS TRIGGER AS $$
DECLARE
  item RECORD;
  already_restored BOOLEAN;
BEGIN
  IF NEW.status = 'cancelled' AND OLD.status = 'paid' THEN

    -- Evita doble restauración (idempotencia)
    SELECT EXISTS (
      SELECT 1
      FROM inventory_movements
      WHERE reference = 'CANCEL:' || NEW.order_id
    ) INTO already_restored;

    IF already_restored THEN
      RETURN NEW;
    END IF;

    -- Devuelve exactamente lo vendido en esa orden
    FOR item IN
      SELECT product_id, quantity
      FROM order_items
      WHERE order_id = NEW.order_id
    LOOP
      INSERT INTO inventory_movements (product_id, movement_type, quantity, reference)
      VALUES (item.product_id, 'IN', item.quantity, 'CANCEL:' || NEW.order_id);
    END LOOP;

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Trigger 1: descuento al pagar
DROP TRIGGER IF EXISTS trg_orders_paid ON orders;
CREATE TRIGGER trg_orders_paid
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION trg_discount_stock_on_paid();


-- Trigger 2: devolución al cancelar
DROP TRIGGER IF EXISTS trg_orders_cancelled ON orders;
CREATE TRIGGER trg_orders_cancelled
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION trg_restore_stock_on_cancel();

COMMIT;
