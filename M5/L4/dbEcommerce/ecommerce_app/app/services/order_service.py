from app.repositories.orders_repo import OrdersRepo
from app.repositories.products_repo import ProductsRepo

class OrderService:
    """
    Reglas en Python (mínimas):
    - No permitir pagar si no hay items
    - (Opcional) prevenir pagar si ya está paid/cancelled
    La verificación dura de stock la hace el trigger en DB.
    """
    def __init__(self, orders_repo: OrdersRepo, products_repo: ProductsRepo):
        self.orders = orders_repo
        self.products = products_repo

    def create_order(self, customer_id: int) -> int:
        return self.orders.create_order(customer_id=customer_id, status="pending")

    def add_item(self, order_id: int, product_id: int, quantity: int) -> int:
        product = self.products.get(product_id)
        if not product:
            raise ValueError(f"Producto no existe: {product_id}")

        if not product["is_active"]:
            raise ValueError(f"Producto inactivo: {product_id}")

        if quantity <= 0:
            raise ValueError("quantity debe ser > 0")

        unit_price = float(product["price"])
        return self.orders.add_item(order_id, product_id, quantity, unit_price)

    def pay(self, order_id: int) -> None:
        order = self.orders.get_order(order_id)
        if not order:
            raise ValueError(f"Orden no existe: {order_id}")

        # regla clara y consistente con tu ejemplo SQL
        if order["status"] != "pending":
            raise ValueError(f"Solo se puede pagar una orden en estado 'pending'. Estado actual={order['status']}")

        items = self.orders.get_items(order_id)
        if not items:
            raise ValueError("No se puede pagar una orden sin items")

        # Trigger DB descuenta stock y valida disponible
        self.orders.update_status(order_id, "paid")


    def cancel(self, order_id: int) -> None:
        order = self.orders.get_order(order_id)
        if not order:
            raise ValueError(f"Orden no existe: {order_id}")

        if order["status"] == "cancelled":
            return

        if order["status"] not in ("pending", "paid"):
            raise ValueError(f"No se puede cancelar una orden con status={order['status']}")

        self.orders.update_status(order_id, "cancelled")

