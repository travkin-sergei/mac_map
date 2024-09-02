from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.prod.system.config import settings

engine_sync = create_engine(
    echo=False,
    url=settings.DATABASE_URL_psycopg,
    # pool_size=5,
    max_overflow=20,
)

session_sync = sessionmaker(engine_sync)
