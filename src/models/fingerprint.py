from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Fingerprint(Base):
    __tablename__ = "fingerprints"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    template = Column(LargeBinary, nullable=False)  # Store fingerprint data as binary
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Each user has one fingerprint

    # Relationship with User model
    user = relationship("User", back_populates="fingerprint")

    def __repr__(self):
        return f"Fingerprint(id={self.id}, user_id={self.user_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "template": self.template,  # Binary data (you may want to encode this before sending in JSON)
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            template=data["template"],
            user_id=data["user_id"],
        )
