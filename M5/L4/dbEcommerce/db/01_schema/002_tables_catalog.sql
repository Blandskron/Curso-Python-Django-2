BEGIN;

CREATE TABLE categories (
  category_id   BIGSERIAL PRIMARY KEY,
  name          VARCHAR(150) NOT NULL UNIQUE,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
  product_id    BIGSERIAL PRIMARY KEY,
  category_id   BIGINT NOT NULL,
  name          VARCHAR(200) NOT NULL,
  description   TEXT,
  price         NUMERIC(12,2) NOT NULL CHECK (price >= 0),
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMIT;
