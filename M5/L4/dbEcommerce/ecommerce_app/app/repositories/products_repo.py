from app.db import query_one, query_all, exec_sql

class ProductsRepo:
    def __init__(self, conn):
        self.conn = conn

    def create(self, category_id: int, name: str, description: str | None, price: float, is_active: bool = True) -> int:
        row = query_one(self.conn, """
            INSERT INTO products(category_id, name, description, price, is_active)
            VALUES(%s,%s,%s,%s,%s)
            RETURNING product_id
        """, (category_id, name, description, price, is_active))
        return int(row["product_id"])

    def get(self, product_id: int):
        return query_one(self.conn, "SELECT * FROM products WHERE product_id=%s", (product_id,))

    def visible(self):
        return query_all(self.conn, "SELECT * FROM vw_products_visible ORDER BY product_id")

    def stock_available(self, product_id: int) -> int:
        row = query_one(self.conn, "SELECT fn_stock_available(%s) AS stock", (product_id,))
        return int(row["stock"])
