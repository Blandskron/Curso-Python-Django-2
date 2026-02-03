BEGIN;

CREATE OR REPLACE FUNCTION fn_stock_available(p_product_id BIGINT)
RETURNS INTEGER AS $$
DECLARE
  stock_in  INTEGER;
  stock_out INTEGER;
BEGIN
  SELECT COALESCE(SUM(quantity),0)
  INTO stock_in
  FROM inventory_movements
  WHERE product_id = p_product_id AND movement_type = 'IN';

  SELECT COALESCE(SUM(quantity),0)
  INTO stock_out
  FROM inventory_movements
  WHERE product_id = p_product_id AND movement_type = 'OUT';

  RETURN stock_in - stock_out;
END;
$$ LANGUAGE plpgsql;

COMMIT;
