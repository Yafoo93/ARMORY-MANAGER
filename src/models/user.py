from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):  
    __tablename__ = "users"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)  # NEW: Stores hashed password

    fingerprint = relationship("Fingerprint", back_populates="user", uselist=False, foreign_keys="[Fingerprint.user_id]")  # Link to fingerprints table (if used)
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
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            service_number=data["service_number"],
            name=data["name"],
            telephone=data["telephone"],
            role=data["role"],
        )

    # ✅ NEW: Hash and verify passwords
    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.hashed_password, password)
