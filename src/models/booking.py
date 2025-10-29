from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.database import Base
from src.models.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    armorer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)
    duty_point_id = Column(Integer, ForeignKey("duty_points.id"), nullable=False)
    ammunition_id = Column(Integer, ForeignKey("ammunitions.id"), nullable=True)

    # Ammunition info
    ammunition_count = Column(Integer, nullable=True)
    ammunition_returned = Column(Integer, nullable=True)
    remarks = Column(String, nullable=True)

    # Status + Timestamps
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expected_return_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    officer = relationship("User", foreign_keys=[officer_id], back_populates="bookings_as_officer")
    armorer = relationship("User", foreign_keys=[armorer_id], back_populates="bookings_as_armorer")
    weapon = relationship("Weapon", back_populates="bookings")
    duty_point = relationship("DutyPoint", back_populates="bookings")
    ammunition = relationship("Ammunition", back_populates="bookings")

    def __repr__(self):
        def __repr__(self):
            return (
                f"<Booking id={self.id} "
                f"weapon={self.weapon_id} "
                f"officer={self.officer_id} "
                f"status={self.status.name}>"
            )
