from contextlib import contextmanager
from dataclasses import dataclass
import psycopg2
import psycopg2.extras

@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    connect_timeout: int = 5

def make_dsn(cfg: DbConfig) -> str:
    return (
        f"host={cfg.host} port={cfg.port} dbname={cfg.dbname} "
        f"user={cfg.user} password={cfg.password} connect_timeout={cfg.connect_timeout}"
    )

@contextmanager
def get_conn(cfg: DbConfig):
    conn = psycopg2.connect(make_dsn(cfg))
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def tx(conn):
    """
    Transacción segura: commit si OK, rollback si error.
    """
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def fetch_one(cur):
    row = cur.fetchone()
    return row

def fetch_all(cur):
    return cur.fetchall()

def exec_sql(conn, sql: str, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.rowcount

def query_one(conn, sql: str, params=None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

def query_all(conn, sql: str, params=None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()

def run_script(conn, script: str):
    """
    Ejecuta un script SQL grande.
    Ojo: psycopg2 permite múltiples sentencias en execute.
    """
    with conn.cursor() as cur:
        cur.execute(script)
