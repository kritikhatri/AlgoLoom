from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DATABASE_URL


class Base(DeclarativeBase):
    pass


def _make_engine():
    if not DATABASE_URL:
        return None
    try:
        return create_engine(DATABASE_URL, pool_pre_ping=True)
    except ArgumentError as error:
        # Never print the URL itself: it contains the database password.
        raise RuntimeError(
            "DATABASE_URL is not a valid database address. It should look like "
            "postgresql://USER:PASSWORD@HOST:5432/DBNAME with no quotes or spaces."
        ) from error


engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
