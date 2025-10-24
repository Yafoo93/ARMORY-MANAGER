from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
import bcrypt
from src.models.booking import Booking



class User(Base):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    role = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    fingerprint = relationship("Fingerprint", back_populates="user", uselist=False, foreign_keys="[Fingerprint.user_id]")
    records = relationship("Record", back_populates="officer", cascade="all, delete-orphan")
    bookings_as_officer = relationship("Booking", foreign_keys="[Booking.officer_id]", back_populates="officer")
    bookings_as_armorer = relationship("Booking", foreign_keys="[Booking.armorer_id]", back_populates="armorer")

    def __repr__(self):
        return f"User(id={self.id}, service_number={self.service_number}, name={self.name}, role={self.role})"

    def to_dict(self):
        return {
            "id": self.id,
            "service_number": self.service_number,
            "name": self.name,
            "telephone": self.telephone,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            service_number=data["service_number"],
            name=data["name"],
            telephone=data["telephone"],
            role=data["role"],
        )

    def set_password(self, password: str):
        """Hash and set user password using bcrypt."""
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Check the given password against stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password.encode("utf-8"))
    
   



