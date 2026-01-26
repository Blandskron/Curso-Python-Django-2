SELECT client_id, name
FROM clients
WHERE name ILIKE '%spa%';

-- a% A al principio
-- %a A al final
-- %a% A En cualquier parte