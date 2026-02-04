import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    connect_timeout: int = 5

def _parse_env_line(line: str) -> tuple[str, str] | None:
    """
    Soporta:
      KEY=value
      KEY="value con espacios"
      KEY='value con #'
    Ignora:
      líneas vacías
      comentarios con #
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    if line.lower().startswith("export "):
        line = line[7:].strip()

    if "=" not in line:
        return None

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # quita comillas si vienen
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return key, value

def load_dotenv(dotenv_path: str | None = None, *, override: bool = False) -> None:
    """
    Carga variables desde un archivo .env al os.environ.
    - override=False: no pisa variables ya existentes.
    - dotenv_path: si no se pasa, busca .env en la raíz del proyecto (junto a main.py).
    """
    if dotenv_path is None:
        # ecommerce_app/.env (mismo nivel que main.py)
        project_root = Path(__file__).resolve().parents[1]
        dotenv_path = str(project_root / ".env")

    path = Path(dotenv_path)
    if not path.exists():
        return

    for raw in path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(raw)
        if not parsed:
            continue
        key, value = parsed
        if not override and key in os.environ:
            continue
        os.environ[key] = value

def load_settings() -> Settings:
    # Cargar .env primero (si existe)
    load_dotenv()

    return Settings(
        host=os.getenv("PGHOST", "127.0.0.1"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "ecommerce"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
        connect_timeout=int(os.getenv("PGCONNECT_TIMEOUT", "5")),
    )
