CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name      VARCHAR(150) NOT NULL,
    email     VARCHAR(150) NOT NULL,
    country   CHAR(2)      NOT NULL
);

INSERT INTO clients (name, email, country)
VALUES ('Acme SpA', 'contacto@acme.cl', 'CL');
