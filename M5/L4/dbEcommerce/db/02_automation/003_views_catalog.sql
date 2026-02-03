BEGIN;

CREATE OR REPLACE VIEW vw_products_visible AS
SELECT
  p.product_id,
  p.name,
  p.description,
  p.price,
  fn_stock_available(p.product_id) AS stock_available
FROM products p
WHERE
  p.is_active = TRUE
  AND fn_stock_available(p.product_id) > 0;

COMMIT;
