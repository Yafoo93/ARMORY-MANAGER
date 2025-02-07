from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Ammunition(Base):
    __tablename__ = "ammunition"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)  # Link to Weapons table
    count = Column(Integer, nullable=False)

    # Relationship with Weapon model
    weapon = relationship("Weapon", back_populates="ammunition")

    def __repr__(self):
        return f"Ammunition(id={self.id}, weapon_id={self.weapon_id}, count={self.count})"

    def to_dict(self):
        return {
            "id": self.id,
            "weapon_id": self.weapon_id,
            "count": self.count,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            weapon_id=data["weapon_id"],
            count=data["count"],
        )
