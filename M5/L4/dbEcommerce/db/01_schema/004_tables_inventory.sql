BEGIN;

CREATE TABLE inventory_movements (
  movement_id   BIGSERIAL PRIMARY KEY,
  product_id    BIGINT NOT NULL,
  movement_type VARCHAR(10) NOT NULL CHECK (movement_type IN ('IN','OUT')),
  quantity      INTEGER NOT NULL CHECK (quantity > 0),
  reference     VARCHAR(100),
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMIT;
