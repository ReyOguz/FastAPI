from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DB_URL = f'{settings.DATABASE_TYPE}://{settings.DATABASE_USER_NAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_URL}:{settings.DATABASE_PORT_NUMBER}/{settings.DATABASE_NAME}'

# Create an engine that is going to connect to and talk to our database
engine = create_engine(SQLALCHEMY_DB_URL) 

# Create a session that is going to use our engine to talk to our database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base model that all of our python/pydantic models/tables will inherit from.
Base = declarative_base()

# Dependancy
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()