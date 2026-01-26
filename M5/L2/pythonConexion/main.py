#!/usr/bin/env python3
import os
import sys
import csv
from typing import List

import psycopg2


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def die(msg: str, code: int = 1) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def read_env(name: str, default: str = "") -> str:
    val = os.environ.get(name, default)
    if val == "":
        die(f"Falta variable de entorno: {name}")
    return val


def load_dotenv(path: str = ".env") -> None:
    """Carga un .env simple (KEY=VALUE). No pisa variables existentes."""
    if not os.path.isfile(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def build_copy_sql(schema: str, table: str, columns: List[str]) -> str:
    """
    COPY schema.table (col1,col2,...) FROM STDIN WITH CSV HEADER
    """
    cols = ", ".join(columns)
    full_table = f"{schema}.{table}" if schema else table
    return f"COPY {full_table} ({cols}) FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"');"


def validate_csv_header(csv_path: str, columns: List[str]) -> None:
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            die("CSV vacío")

        header_set = {h.strip() for h in header}
        missing = [c for c in columns if c not in header_set]
        if missing:
            die(f"CSV no contiene estas columnas requeridas: {missing}")


def connect_pg():
    host = read_env("PGHOST")
    port = read_env("PGPORT")
    dbname = read_env("PGDATABASE")
    user = read_env("PGUSER")
    password = os.environ.get("PGPASSWORD", "")
    sslmode = os.environ.get("PGSSLMODE", "disable")  # por defecto disable

    # psycopg2 acepta sslmode como parámetro
    try:
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            dbname=dbname,
            user=user,
            password=password,
            sslmode=sslmode,
        )
        return conn
    except Exception as e:
        die(
            "No pude conectar a PostgreSQL.\n"
            f"Host: {host}  Port: {port}  DB: {dbname}  User: {user}  sslmode={sslmode}\n"
            f"Detalle: {e}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main() -> None:
    load_dotenv()

    # Uso:
    # python3 main.py <csv_path> <schema> <table> <col1,col2,...>
    if len(sys.argv) != 5:
        die("Uso: python3 main.py <csv_path> <schema> <table> <col1,col2,...>")

    csv_path = sys.argv[1]
    schema = sys.argv[2]
    table = sys.argv[3]
    columns = [c.strip() for c in sys.argv[4].split(",") if c.strip()]

    if not os.path.isfile(csv_path):
        die(f"No existe el archivo CSV: {csv_path}")

    if not columns:
        die("Debes indicar al menos 1 columna")

    validate_csv_header(csv_path, columns)

    copy_sql = build_copy_sql(schema, table, columns)

    conn = connect_pg()
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            # COPY FROM STDIN: le pasamos el archivo completo
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                cur.copy_expert(copy_sql, f)

        conn.commit()
        print(f"[OK] Carga masiva completada → {schema}.{table} desde {csv_path}")
    except Exception as e:
        conn.rollback()
        die(f"Falló la carga masiva (rollback aplicado). Detalle: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
