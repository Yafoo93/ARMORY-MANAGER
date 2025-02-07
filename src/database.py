from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the database file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "sqlite.db")

# Initialize SQLAlchemy ORM
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Import models and create database tables."""
    from src.models.weapon import Weapon
    from src.models.user import User
    from src.models.record import Record
    from src.models.ammunition import Ammunition
    from src.models.duty_point import DutyPoint
    from src.models.fingerprint import Fingerprint
    
    # Create tables in the database
    Base.metadata.create_all(bind=engine)
