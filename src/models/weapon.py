from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Weapon(Base):  
    __tablename__ = "weapons"  # Define the table name

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    serial_number = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False, default="in-stock")

    records = relationship("Record", back_populates="weapon", cascade="all, delete-orphan")
    ammunition = relationship("Ammunition", back_populates="weapon", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Weapon(id={self.id}, serial_number={self.serial_number}, type={self.type}, status={self.status})"

    def to_dict(self):
        return {
            "id": self.id,
            "serial_number": self.serial_number,
            "type": self.type,
            "condition": self.condition,
            "location": self.location,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            serial_number=data["serial_number"],
            type=data["type"],
            condition=data["condition"],
            location=data["location"],
            status=data.get("status", "in-stock"),
        )
