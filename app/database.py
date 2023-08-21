from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
