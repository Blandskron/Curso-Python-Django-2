from app.db import query_one, exec_sql

class CustomersRepo:
    def __init__(self, conn):
        self.conn = conn

    def create(self, first_name: str, last_name: str, email: str | None, phone: str | None) -> int:
        row = query_one(self.conn, """
            INSERT INTO customers(first_name, last_name, email, phone)
            VALUES(%s,%s,%s,%s)
            RETURNING customer_id
        """, (first_name, last_name, email, phone))
        return int(row["customer_id"])

    def get_by_id(self, customer_id: int):
        return query_one(self.conn, "SELECT * FROM customers WHERE customer_id=%s", (customer_id,))
