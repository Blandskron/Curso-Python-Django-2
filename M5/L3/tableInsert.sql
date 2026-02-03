-- PostgreSQL (versión simple) — Tablas necesarias para que funcionen tus INSERT/UPDATE/DELETE

-- 1) CLIENTS
CREATE TABLE IF NOT EXISTS clients (
  client_id   BIGSERIAL PRIMARY KEY,
  name        VARCHAR(200) NOT NULL,
  email       VARCHAR(254) NOT NULL UNIQUE,
  country     CHAR(2) NOT NULL,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2) PRODUCTS
CREATE TABLE IF NOT EXISTS products (
  product_id  BIGSERIAL PRIMARY KEY,
  sku         VARCHAR(64) NOT NULL UNIQUE,
  name        VARCHAR(200) NOT NULL,
  category    VARCHAR(50) NOT NULL,
  price       NUMERIC(12,2) NOT NULL,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT products_price_nonneg CHECK (price >= 0)
);

-- 3) ORDERS
CREATE TABLE IF NOT EXISTS orders (
  order_id    BIGSERIAL PRIMARY KEY,
  client_id   BIGINT NOT NULL REFERENCES clients(client_id),
  order_date  DATE NOT NULL DEFAULT CURRENT_DATE,
  status      VARCHAR(20) NOT NULL DEFAULT 'PENDING',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4) ORDER_ITEMS
CREATE TABLE IF NOT EXISTS order_items (
  order_item_id BIGSERIAL PRIMARY KEY,
  order_id      BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id    BIGINT NOT NULL REFERENCES products(product_id),
  quantity      INT NOT NULL,
  unit_price    NUMERIC(12,2) NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT order_items_qty_pos CHECK (quantity > 0),
  CONSTRAINT order_items_unit_price_nonneg CHECK (unit_price >= 0),
  CONSTRAINT order_items_unique_line UNIQUE (order_id, product_id)
);

-- 5) PAYMENTS
CREATE TABLE IF NOT EXISTS payments (
  payment_id  BIGSERIAL PRIMARY KEY,
  order_id    BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  paid_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  amount      NUMERIC(12,2) NOT NULL,
  method      VARCHAR(20) NOT NULL,
  status      VARCHAR(20) NOT NULL DEFAULT 'APPROVED',
  CONSTRAINT payments_amount_pos CHECK (amount > 0),
  CONSTRAINT payments_method_check CHECK (method IN ('CARD','TRANSFER','CASH')),
  CONSTRAINT payments_status_check CHECK (status IN ('APPROVED','FAILED','PENDING'))
);

-- 6) CART_ITEMS (para tu ejemplo INSERT...SELECT desde “carrito”)
CREATE TABLE IF NOT EXISTS cart_items (
  cart_item_id BIGSERIAL PRIMARY KEY,
  user_id      BIGINT NOT NULL,
  product_id   BIGINT NOT NULL REFERENCES products(product_id),
  quantity     INT NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT cart_items_qty_pos CHECK (quantity > 0),
  CONSTRAINT cart_items_unique_user_product UNIQUE (user_id, product_id)
);

-- 7) PRODUCT_STOCK (para tu UPSERT de stock)
CREATE TABLE IF NOT EXISTS product_stock (
  product_id BIGINT PRIMARY KEY REFERENCES products(product_id) ON DELETE CASCADE,
  stock      INT NOT NULL DEFAULT 0,
  CONSTRAINT product_stock_nonneg CHECK (stock >= 0)
);

-- =========================
-- INSERTS DE EJEMPLO (DML)
-- =========================

-- 1) CLIENTS
INSERT INTO clients (name, email, country)
VALUES ('Acme SpA', 'contacto@acme.cl', 'CL');

INSERT INTO clients (name, email, country)
VALUES ('Nova Ltda', 'hola@nova.cl', 'CL');

INSERT INTO clients (name, email, country)
VALUES ('Andes Corp', 'info@andes.com', 'AR');

-- 2) PRODUCTS
INSERT INTO products (sku, name, category, price, is_active)
VALUES
  ('SKU-100', 'Plan Básico', 'SOFTWARE', 9900, TRUE),
  ('SKU-200', 'Plan Pro', 'SOFTWARE', 19900, TRUE),
  ('SKU-300', 'Soporte Premium', 'SERVICE', 29900, TRUE);

-- 3) ORDERS
INSERT INTO orders (client_id, order_date, status)
VALUES
  (1, CURRENT_DATE, 'PENDING'),
  (1, CURRENT_DATE - INTERVAL '10 days', 'PAID'),
  (3, CURRENT_DATE - INTERVAL '100 days', 'PENDING');

-- 4) ORDER_ITEMS
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
  (1, 1, 1, 9900),
  (1, 2, 1, 19900),
  (2, 2, 2, 19900);

-- 5) PAYMENTS
INSERT INTO payments (order_id, paid_at, amount, method, status)
VALUES
  (2, now(), 39800, 'CARD', 'APPROVED');

-- 6) CART_ITEMS
INSERT INTO cart_items (user_id, product_id, quantity)
VALUES
  (7, 1, 2),
  (7, 2, 1),
  (8, 3, 1);

-- 7) PRODUCT_STOCK
INSERT INTO product_stock (product_id, stock)
VALUES
  (1, 100),
  (2, 50),
  (3, 25);

-- =========================
-- INSERTS AVANZADOS
-- =========================

-- UPSERT CLIENT (evitar duplicado por email)
INSERT INTO clients (email, name, country)
VALUES ('contacto@acme.cl', 'Acme SpA Actualizado', 'CL')
ON CONFLICT (email)
DO UPDATE SET
  name = EXCLUDED.name,
  country = EXCLUDED.country;

-- INSERT … SELECT (crear pedidos para clientes de Chile)
INSERT INTO orders (client_id, order_date, status)
SELECT client_id, CURRENT_DATE, 'PENDING'
FROM clients
WHERE country = 'CL';

-- INSERT usando RETURNING (ejemplo conceptual)
INSERT INTO orders (client_id, status)
VALUES (1, 'PENDING')
RETURNING order_id;

-- INSERT de items usando secuencia (misma sesión)
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (
  currval(pg_get_serial_sequence('orders','order_id')),
  1,
  1,
  9900
);

-- UPSERT DE STOCK (incremental)
INSERT INTO product_stock (product_id, stock)
VALUES (1, 5)
ON CONFLICT (product_id)
DO UPDATE SET stock = product_stock.stock + EXCLUDED.stock;



