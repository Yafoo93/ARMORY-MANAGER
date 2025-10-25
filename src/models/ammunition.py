from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index, relationship, ForeignKey
from sqlalchemy.sql import func
from src.database import Base

class Ammunition(Base):
    __tablename__ = "ammunitions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)

    platform = Column(String, nullable=False)
    caliber = Column(String, nullable=False)
    count = Column(Integer, nullable=False, default=0)

    weapon = relationship("Weapon", back_populates="ammunition")
    bookings = relationship("Booking", back_populates="ammunition", cascade="all, delete-orphan")

    reorder_level = Column(Integer, nullable=False, default=0)
    bin_location = Column(String)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("platform", "caliber", name="uq_ammo_platform_caliber"),
        Index("ix_ammo_caliber", "caliber"),
    )

