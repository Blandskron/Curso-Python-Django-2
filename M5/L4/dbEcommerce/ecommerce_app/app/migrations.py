from dataclasses import dataclass
from app.db import run_script, exec_sql, query_one

# =========================
# 1) TU ESQUEMA (TABLAS/FK/INDEX)
# =========================
SCHEMA_SQL = r"""
BEGIN;

CREATE TABLE IF NOT EXISTS public.categories
(
    category_id bigserial NOT NULL,
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT categories_pkey PRIMARY KEY (category_id),
    CONSTRAINT categories_name_key UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.customers
(
    customer_id bigserial NOT NULL,
    first_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(150) COLLATE pg_catalog."default",
    phone character varying(50) COLLATE pg_catalog."default",
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id),
    CONSTRAINT customers_email_key UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.inventory_movements
(
    movement_id bigserial NOT NULL,
    product_id bigint NOT NULL,
    movement_type character varying(10) COLLATE pg_catalog."default" NOT NULL,
    quantity integer NOT NULL,
    reference character varying(100) COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT inventory_movements_pkey PRIMARY KEY (movement_id)
);

CREATE TABLE IF NOT EXISTS public.order_items
(
    order_item_id bigserial NOT NULL,
    order_id bigint NOT NULL,
    product_id bigint NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(12, 2) NOT NULL,
    CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id)
);

CREATE TABLE IF NOT EXISTS public.order_status_history
(
    history_id bigserial NOT NULL,
    order_id bigint NOT NULL,
    from_status character varying(30) COLLATE pg_catalog."default",
    to_status character varying(30) COLLATE pg_catalog."default" NOT NULL,
    changed_at timestamp without time zone NOT NULL DEFAULT now(),
    note text COLLATE pg_catalog."default",
    CONSTRAINT order_status_history_pkey PRIMARY KEY (history_id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    order_id bigserial NOT NULL,
    customer_id bigint NOT NULL,
    status character varying(30) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT orders_pkey PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS public.products
(
    product_id bigserial NOT NULL,
    category_id bigint NOT NULL,
    name character varying(200) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    price numeric(12, 2) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
);

ALTER TABLE IF EXISTS public.inventory_movements
    ADD CONSTRAINT fk_inventory_product FOREIGN KEY (product_id)
    REFERENCES public.products (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_inventory_product
    ON public.inventory_movements(product_id);

ALTER TABLE IF EXISTS public.order_items
    ADD CONSTRAINT fk_items_order FOREIGN KEY (order_id)
    REFERENCES public.orders (order_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_items_order
    ON public.order_items(order_id);

ALTER TABLE IF EXISTS public.order_items
    ADD CONSTRAINT fk_items_product FOREIGN KEY (product_id)
    REFERENCES public.products (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.order_status_history
    ADD CONSTRAINT fk_order_status_history_order FOREIGN KEY (order_id)
    REFERENCES public.orders (order_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_order_status_history_order
    ON public.order_status_history(order_id);

ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
    REFERENCES public.customers (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_orders_customer
    ON public.orders(customer_id);

ALTER TABLE IF EXISTS public.products
    ADD CONSTRAINT fk_products_category FOREIGN KEY (category_id)
    REFERENCES public.categories (category_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_products_category
    ON public.products(category_id);

COMMIT;
"""

# =========================
# 2) TUS "AUTOMATIZACIONES" (FUNCIONES/TRIGGERS/VIEWS)
#    (Incluye la versión final con restore al cancelar + history al crear/cambiar)
# =========================
AUTOMATIONS_SQL = r"""
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

BEGIN;

-- 1) Descuenta stock al pasar a PAID
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

-- 2) Devuelve stock al pasar de PAID -> CANCELLED (idempotente)
CREATE OR REPLACE FUNCTION trg_restore_stock_on_cancel()
RETURNS TRIGGER AS $$
DECLARE
  item RECORD;
  already_restored BOOLEAN;
BEGIN
  IF NEW.status = 'cancelled' AND OLD.status = 'paid' THEN

    SELECT EXISTS (
      SELECT 1
      FROM inventory_movements
      WHERE reference = 'CANCEL:' || NEW.order_id
    ) INTO already_restored;

    IF already_restored THEN
      RETURN NEW;
    END IF;

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

BEGIN;

-- Historial: log al crear orden
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

BEGIN;

-- Historial: log al cambiar status
CREATE OR REPLACE FUNCTION trg_log_order_status_change()
RETURNS TRIGGER AS $$
BEGIN
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

BEGIN;

-- Vista productos visibles (activos y con stock > 0)
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

BEGIN;

-- Vista resumen ventas por fecha (status paid)
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
"""

MIGRATIONS = [
    ("001_schema", SCHEMA_SQL),
    ("002_automations", AUTOMATIONS_SQL),
]

def ensure_migrations_table(conn):
    exec_sql(conn, """
    CREATE TABLE IF NOT EXISTS public.schema_migrations (
        version varchar(50) PRIMARY KEY,
        applied_at timestamp without time zone NOT NULL DEFAULT now()
    );
    """)

def is_applied(conn, version: str) -> bool:
    row = query_one(conn, "SELECT version FROM public.schema_migrations WHERE version=%s", (version,))
    return row is not None

def mark_applied(conn, version: str):
    exec_sql(conn, "INSERT INTO public.schema_migrations(version) VALUES(%s)", (version,))

def apply_all(conn):
    """
    Aplica migraciones UNA SOLA VEZ.
    Si ya están aplicadas, no hace nada.
    """
    ensure_migrations_table(conn)

    for version, sql in MIGRATIONS:
        if is_applied(conn, version):
            continue
        run_script(conn, sql)
        mark_applied(conn, version)
