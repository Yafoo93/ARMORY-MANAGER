import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "sqlite.db")

# Initialize SQLAlchemy ORM
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def init_db():
# """Import models and create database tables."""
# Import models to register them with SQLAlchemy
# import src.models.ammunition
# import src.models.booking
# import src.models.duty_point
# import src.models.fingerprint
# import src.models.record


# Create tables in the database
# Base.metadata.create_all(bind=engine)
