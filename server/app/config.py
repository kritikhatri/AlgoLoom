import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _database_url() -> str:
    # Hosting dashboards make it easy to paste stray spaces or quotes around the value.
    url = os.environ.get("DATABASE_URL", "").strip().strip("'\"").strip()
    # SQLAlchemy needs the driver name. Hosted providers often use the short
    # "postgres://" scheme; both map to psycopg 3.
    for scheme in ("postgresql://", "postgres://"):
        if url.startswith(scheme):
            return "postgresql+psycopg://" + url[len(scheme):]
    return url


DATABASE_URL = _database_url()
JWT_SECRET = os.environ.get("JWT_SECRET", "")
TOKEN_TTL_DAYS = 7
