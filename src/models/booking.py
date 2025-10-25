from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    armorer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)
    duty_point_id = Column(Integer, ForeignKey("duty_points.id"), nullable=False)
    ammunition_id = Column(Integer, ForeignKey("ammunitions.id"), nullable=True)

    ammunition_count = Column(Integer, nullable=True)
    ammunition_returned = Column(Integer, nullable=True)
    remarks = Column(String, nullable=True)

    # 🕓 Add these:
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    status = Column(String, default="issued")

    # Relationships
    officer = relationship("User", foreign_keys=[officer_id])
    armorer = relationship("User", foreign_keys=[armorer_id])
    weapon = relationship("Weapon")
    ammunition = relationship("Ammunition")
    duty_point = relationship("DutyPoint")
