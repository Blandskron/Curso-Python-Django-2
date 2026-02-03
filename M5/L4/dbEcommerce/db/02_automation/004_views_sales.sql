BEGIN;

CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
  DATE(o.created_at) AS sale_date,
  COUNT(DISTINCT o.order_id) AS orders_count,
  SUM(oi.quantity * oi.unit_price) AS total_sales
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY DATE(o.created_at);

COMMIT;
