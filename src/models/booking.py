from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duty_point_id = Column(Integer, ForeignKey("duty_points.id"), nullable=False)

    status = Column(Text, nullable=False, default="REQUESTED")
    requested_at = Column(DateTime, server_default=func.now(), nullable=False)
    issued_at = Column(DateTime)
    returned_at = Column(DateTime)
    notes = Column(Text)

    weapon = relationship("Weapon", back_populates="bookings")
