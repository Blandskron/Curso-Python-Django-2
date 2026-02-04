from app.db import query_one, query_all, exec_sql

class OrdersRepo:
    def __init__(self, conn):
        self.conn = conn

    def create_order(self, customer_id: int, status: str = "pending") -> int:
        row = query_one(self.conn, """
            INSERT INTO orders(customer_id, status)
            VALUES(%s, %s)
            RETURNING order_id
        """, (customer_id, status))
        return int(row["order_id"])


    def add_item(self, order_id: int, product_id: int, quantity: int, unit_price: float) -> int:
        row = query_one(self.conn, """
            INSERT INTO order_items(order_id, product_id, quantity, unit_price)
            VALUES(%s,%s,%s,%s)
            RETURNING order_item_id
        """, (order_id, product_id, quantity, unit_price))
        return int(row["order_item_id"])

    def get_order(self, order_id: int):
        return query_one(self.conn, "SELECT * FROM orders WHERE order_id=%s", (order_id,))

    def get_items(self, order_id: int):
        return query_all(self.conn, """
            SELECT oi.*, p.name AS product_name
            FROM order_items oi
            JOIN products p ON p.product_id = oi.product_id
            WHERE oi.order_id=%s
            ORDER BY oi.order_item_id
        """, (order_id,))

    def update_status(self, order_id: int, new_status: str) -> None:
        # OJO: aquí disparan triggers (stock y history) automáticamente
        exec_sql(self.conn, "UPDATE orders SET status=%s WHERE order_id=%s", (new_status, order_id))

    def sales_summary(self):
        return query_all(self.conn, "SELECT * FROM vw_sales_summary ORDER BY sale_date DESC")

    def status_history(self, order_id: int):
        return query_all(self.conn, """
            SELECT *
            FROM order_status_history
            WHERE order_id=%s
            ORDER BY history_id
        """, (order_id,))
