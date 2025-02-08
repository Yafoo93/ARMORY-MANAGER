from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):  
    __tablename__ = "users"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    fingerprint = relationship("Fingerprint", back_populates="user", uselist=False, foreign_keys="[Fingerprint.user_id]")  # Link to fingerprints table (if used)

    # Relationship (if using a Fingerprint table)
    fingerprint = relationship("Fingerprint", back_populates="user", uselist=False)
    records = relationship("Record", back_populates="officer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, service_number={self.service_number}, name={self.name}, role={self.role})"

    def to_dict(self):
        return {
            "id": self.id,
            "service_number": self.service_number,
            "name": self.name,
            "telephone": self.telephone,
            "role": self.role,
            "fingerprint_id": self.fingerprint_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            service_number=data["service_number"],
            name=data["name"],
            telephone=data["telephone"],
            role=data["role"],
            fingerprint_id=data.get("fingerprint_id"),
        )
