from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from sqlalchemy.orm import relationship
from src.database import Base




class Weapon(Base):  
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    location = Column(String, nullable=True)  
    status = Column(String, nullable=False)
    last_service = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    records = relationship("Record", back_populates="weapon", cascade="all, delete-orphan")
    ammunition = relationship("Ammunition", back_populates="weapon", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="weapon", cascade="all, delete-orphan")
    

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
            location=data.get("location"),
            status=data["status"],
        )
