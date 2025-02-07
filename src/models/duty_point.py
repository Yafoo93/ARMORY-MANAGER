from sqlalchemy import Column, Integer, String
from src.database import Base

class DutyPoint(Base):
    __tablename__ = "duty_points"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, unique=True, nullable=False)  # Ensure each duty point location is unique
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"DutyPoint(id={self.id}, location={self.location})"

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            location=data["location"],
            description=data.get("description"),
        )
