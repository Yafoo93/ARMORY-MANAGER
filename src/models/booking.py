from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Text, Enum
)
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    armorer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duty_point_id = Column(Integer, ForeignKey("duty_points.id"), nullable=False)
    ammunition_id = Column(Integer, ForeignKey("ammunition.id"), nullable=True)

    # Ammunition tracking
    ammo_issued_count = Column(Integer, default=0)
    ammo_returned_count = Column(Integer, default=0)
    ammo_usage_notes = Column(Text, nullable=True)

    # Booking lifecycle
    status = Column(Enum(BookingStatus), default=BookingStatus.ACTIVE, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expected_return_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    weapon = relationship("Weapon", back_populates="bookings")
    officer = relationship("User", foreign_keys=[officer_id], back_populates="bookings_as_officer")
    armorer = relationship("User", foreign_keys=[armorer_id], back_populates="bookings_as_armorer")
    duty_point = relationship("DutyPoint", back_populates="bookings")
    ammunition = relationship("Ammunition", back_populates="bookings")

    def __repr__(self):
        return f"<Booking id={self.id} weapon={self.weapon_id} officer={self.officer_id} status={self.status.name}>"
