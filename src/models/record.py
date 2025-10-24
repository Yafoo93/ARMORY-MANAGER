from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Record(Base):
    __tablename__ = "records"  # Define table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to User table
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)  # Link to Weapon table
    duty_point_id = Column(
        Integer, ForeignKey("duty_points.id"), nullable=False
    )  # Link to DutyPoint table
    ammo_issued = Column(Integer, nullable=False)
    time_booked = Column(DateTime, nullable=False, default=datetime.utcnow)  # Store booking time
    time_returned = Column(DateTime, nullable=True)  # Nullable for weapons not yet returned

    # Relationships
    officer = relationship("User", back_populates="records")
    weapon = relationship("Weapon", back_populates="records")
    duty_point = relationship("DutyPoint", back_populates="records")

    def __repr__(self):
        return (
            f"Record(id={self.id}, officer_id={self.officer_id}, "
            f"weapon_id={self.weapon_id}, time_booked={self.time_booked})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "officer_id": self.officer_id,
            "weapon_id": self.weapon_id,
            "duty_point_id": self.duty_point_id,
            "ammo_issued": self.ammo_issued,
            "time_booked": self.time_booked.isoformat() if self.time_booked else None,
            "time_returned": (self.time_returned.isoformat() if self.time_returned else None),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            officer_id=data["officer_id"],
            weapon_id=data["weapon_id"],
            duty_point_id=data["duty_point_id"],
            ammo_issued=data["ammo_issued"],
            time_booked=(
                datetime.fromisoformat(data["time_booked"])
                if data.get("time_booked")
                else datetime.utcnow()
            ),
            time_returned=(
                datetime.fromisoformat(data["time_returned"]) if data.get("time_returned") else None
            ),
        )
