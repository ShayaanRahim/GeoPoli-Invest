import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine.url import make_url
from .models import Base

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///geopoli_news.db")
IS_SQLITE = DB_URL.startswith("sqlite")

# Connection pooling for PostgreSQL, simple for SQLite
engine = create_engine(
    DB_URL,
    poolclass=QueuePool if not IS_SQLITE else None,
    pool_size=10 if not IS_SQLITE else None,
    max_overflow=20 if not IS_SQLITE else None,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
    echo=False
)
SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_health_check():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except OperationalError:
        return False

# Retry logic for connection
def wait_for_db(max_retries=5, delay=2):
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except OperationalError:
            time.sleep(delay)
    return False 