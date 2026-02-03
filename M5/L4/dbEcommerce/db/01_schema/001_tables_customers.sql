BEGIN;

CREATE TABLE customers (
  customer_id     BIGSERIAL PRIMARY KEY,
  first_name      VARCHAR(100) NOT NULL,
  last_name       VARCHAR(100) NOT NULL,
  email           VARCHAR(150) UNIQUE,
  phone           VARCHAR(50),
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMIT;
