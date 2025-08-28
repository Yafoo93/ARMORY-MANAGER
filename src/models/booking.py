from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime
from .enums import BookingStatus
from src.database import Base
from sqlalchemy.sql import func


class Booking(Base):
    __tablename__ = 'bookings'

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
