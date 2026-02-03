BEGIN;

CREATE TABLE orders (
  order_id      BIGSERIAL PRIMARY KEY,
  customer_id   BIGINT NOT NULL,
  status        VARCHAR(30) NOT NULL CHECK (status IN ('pending','paid','cancelled')),
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
  order_item_id BIGSERIAL PRIMARY KEY,
  order_id      BIGINT NOT NULL,
  product_id    BIGINT NOT NULL,
  quantity      INTEGER NOT NULL CHECK (quantity > 0),
  unit_price    NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0)
);

COMMIT;

BEGIN;

CREATE TABLE order_status_history (
  history_id   BIGSERIAL PRIMARY KEY,
  order_id     BIGINT NOT NULL,
  from_status  VARCHAR(30),
  to_status    VARCHAR(30) NOT NULL,
  changed_at   TIMESTAMP NOT NULL DEFAULT NOW(),
  note         TEXT
);

COMMIT;
