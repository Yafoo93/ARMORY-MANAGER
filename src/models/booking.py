from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    # Foreign keys
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    armorer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duty_point_id = Column(Integer, ForeignKey("duty_points.id"), nullable=False)

    status = Column(Text, nullable=False, default="REQUESTED")
    requested_at = Column(DateTime, server_default=func.now(), nullable=False)
    issued_at = Column(DateTime)
    returned_at = Column(DateTime)
    notes = Column(Text)

    weapon = relationship("Weapon", back_populates="bookings")
    officer = relationship("User", foreign_keys=[officer_id], back_populates="bookings_as_officer")
    armorer = relationship("User", foreign_keys=[armorer_id], back_populates="bookings_as_armorer")
    duty_point = relationship("DutyPoint", back_populates="bookings")
    ammunition = relationship("Ammunition", back_populates="bookings")

    def __repr__(self):
        return (
            f"<Booking id={self.id} weapon={self.weapon_id} "
            f"officer={self.officer_id} status={self.status}>"
        )
