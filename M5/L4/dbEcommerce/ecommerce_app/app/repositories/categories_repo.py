from app.db import query_one, exec_sql

class CategoriesRepo:
    def __init__(self, conn):
        self.conn = conn

    def upsert_by_name(self, name: str) -> int:
        row = query_one(self.conn, """
            INSERT INTO categories(name)
            VALUES(%s)
            ON CONFLICT(name) DO UPDATE SET name=EXCLUDED.name
            RETURNING category_id
        """, (name,))
        return int(row["category_id"])
