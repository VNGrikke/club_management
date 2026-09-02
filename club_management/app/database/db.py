from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

if not database_exists(engine.url):
    create_database(engine.url)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()