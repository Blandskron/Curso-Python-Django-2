import argparse
import sys

from app.settings import load_settings
from app.db import DbConfig, get_conn, tx, query_all
from app.migrations import apply_all
from app.repositories.customers_repo import CustomersRepo
from app.repositories.categories_repo import CategoriesRepo
from app.repositories.products_repo import ProductsRepo
from app.repositories.inventory_repo import InventoryRepo
from app.repositories.orders_repo import OrdersRepo
from app.services.order_service import OrderService

def _db_config() -> DbConfig:
    s = load_settings()
    return DbConfig(
        host=s.host, port=s.port, dbname=s.dbname, user=s.user, password=s.password,
        connect_timeout=s.connect_timeout
    )

def cmd_init_db(_args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            apply_all(conn)
    print("OK: DB inicializada (migraciones aplicadas si faltaban).")

def cmd_create_customer(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            repo = CustomersRepo(conn)
            customer_id = repo.create(args.first_name, args.last_name, args.email, args.phone)
    print(f"OK: customer_id={customer_id}")

def cmd_create_category(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            repo = CategoriesRepo(conn)
            category_id = repo.upsert_by_name(args.name)
    print(f"OK: category_id={category_id}")

def cmd_create_product(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            prod = ProductsRepo(conn)
            product_id = prod.create(
                category_id=args.category_id,
                name=args.name,
                description=args.description,
                price=float(args.price),
                is_active=(not args.inactive),
            )
    print(f"OK: product_id={product_id}")

def cmd_stock_in(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            inv = InventoryRepo(conn)
            inv.movement_in(args.product_id, args.quantity, args.reference)
    print("OK: stock IN registrado.")

def cmd_stock_out(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            inv = InventoryRepo(conn)
            inv.movement_out(args.product_id, args.quantity, args.reference)
    print("OK: stock OUT registrado.")

def cmd_visible_products(_args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        rows = query_all(conn, "SELECT * FROM vw_products_visible ORDER BY product_id")
    for r in rows:
        print(f"{r['product_id']} | {r['name']} | price={r['price']} | stock={r['stock_available']}")

def _order_service(conn) -> OrderService:
    orders_repo = OrdersRepo(conn)
    products_repo = ProductsRepo(conn)
    return OrderService(orders_repo, products_repo)

def cmd_create_order(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            orders_repo = OrdersRepo(conn)
            order_id = orders_repo.create_order(args.customer_id, status=args.status)
    print(f"OK: order_id={order_id}")

def cmd_add_item(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        with tx(conn):
            svc = _order_service(conn)
            order_item_id = svc.add_item(args.order_id, args.product_id, args.quantity)
    print(f"OK: order_item_id={order_item_id}")

def cmd_pay_order(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        try:
            with tx(conn):
                svc = _order_service(conn)
                svc.pay(args.order_id)
            print("OK: orden pagada (trigger descontó stock y registró history).")
        except Exception as e:
            print(f"ERROR al pagar: {e}")
            sys.exit(1)

def cmd_cancel_order(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        try:
            with tx(conn):
                svc = _order_service(conn)
                svc.cancel(args.order_id)
            print("OK: orden cancelada (si estaba pagada, trigger restauró stock).")
        except Exception as e:
            print(f"ERROR al cancelar: {e}")
            sys.exit(1)

def cmd_order_info(args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        orders = OrdersRepo(conn)
        o = orders.get_order(args.order_id)
        items = orders.get_items(args.order_id)
        hist = orders.status_history(args.order_id)

    print("ORDER:", o)
    print("ITEMS:")
    for it in items:
        print(" ", it)
    print("HISTORY:")
    for h in hist:
        print(" ", h)

def cmd_sales_summary(_args):
    cfg = _db_config()
    with get_conn(cfg) as conn:
        orders = OrdersRepo(conn)
        rows = orders.sales_summary()
    for r in rows:
        print(f"{r['sale_date']} | orders={r['orders_count']} | total={r['total_sales']}")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ecommerce", description="Ecommerce DB updater (Python + psycopg2)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init-db", help="Crea tablas, funciones, triggers y views (solo si faltan).")
    s.set_defaults(func=cmd_init_db)

    s = sub.add_parser("create-customer")
    s.add_argument("--first-name", required=True)
    s.add_argument("--last-name", required=True)
    s.add_argument("--email", default=None)
    s.add_argument("--phone", default=None)
    s.set_defaults(func=cmd_create_customer)

    s = sub.add_parser("create-category")
    s.add_argument("--name", required=True)
    s.set_defaults(func=cmd_create_category)

    s = sub.add_parser("create-product")
    s.add_argument("--category-id", type=int, required=True)
    s.add_argument("--name", required=True)
    s.add_argument("--description", default=None)
    s.add_argument("--price", required=True)
    s.add_argument("--inactive", action="store_true")
    s.set_defaults(func=cmd_create_product)

    s = sub.add_parser("stock-in")
    s.add_argument("--product-id", type=int, required=True)
    s.add_argument("--quantity", type=int, required=True)
    s.add_argument("--reference", default=None)
    s.set_defaults(func=cmd_stock_in)

    s = sub.add_parser("stock-out")
    s.add_argument("--product-id", type=int, required=True)
    s.add_argument("--quantity", type=int, required=True)
    s.add_argument("--reference", default=None)
    s.set_defaults(func=cmd_stock_out)

    s = sub.add_parser("visible-products")
    s.set_defaults(func=cmd_visible_products)

    s = sub.add_parser("create-order")
    s.add_argument("--customer-id", type=int, required=True)
    s.add_argument("--status", default="pending", choices=["pending", "paid", "cancelled"])
    s.set_defaults(func=cmd_create_order)


    s = sub.add_parser("add-item")
    s.add_argument("--order-id", type=int, required=True)
    s.add_argument("--product-id", type=int, required=True)
    s.add_argument("--quantity", type=int, required=True)
    s.set_defaults(func=cmd_add_item)

    s = sub.add_parser("pay-order")
    s.add_argument("--order-id", type=int, required=True)
    s.set_defaults(func=cmd_pay_order)

    s = sub.add_parser("cancel-order")
    s.add_argument("--order-id", type=int, required=True)
    s.set_defaults(func=cmd_cancel_order)

    s = sub.add_parser("order-info")
    s.add_argument("--order-id", type=int, required=True)
    s.set_defaults(func=cmd_order_info)

    s = sub.add_parser("sales-summary")
    s.set_defaults(func=cmd_sales_summary)

    return p

def run():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
