from app.db import exec_sql, query_all

class InventoryRepo:
    def __init__(self, conn):
        self.conn = conn

    def movement_in(self, product_id: int, quantity: int, reference: str | None = None) -> None:
        exec_sql(self.conn, """
            INSERT INTO inventory_movements(product_id, movement_type, quantity, reference)
            VALUES(%s, 'IN', %s, %s)
        """, (product_id, quantity, reference))

    def movement_out(self, product_id: int, quantity: int, reference: str | None = None) -> None:
        exec_sql(self.conn, """
            INSERT INTO inventory_movements(product_id, movement_type, quantity, reference)
            VALUES(%s, 'OUT', %s, %s)
        """, (product_id, quantity, reference))

    def list_by_product(self, product_id: int):
        return query_all(self.conn, """
            SELECT *
            FROM inventory_movements
            WHERE product_id=%s
            ORDER BY movement_id DESC
        """, (product_id,))
