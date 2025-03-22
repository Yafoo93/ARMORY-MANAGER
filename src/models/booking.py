from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    weapon_id = Column(Integer, ForeignKey('weapons.id'))
    status = Column(String, nullable=False)  # e.g., "Booked Out", "Due Return"
    created_at = Column(DateTime, default=datetime.utcnow)

    weapon = relationship("Weapon", back_populates="bookings")
