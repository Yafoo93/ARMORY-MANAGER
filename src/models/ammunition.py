from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class Ammunition(Base):
    __tablename__ = "ammunition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False)

    # Platform/model family label for clarity in reports
    platform = Column(String, nullable=False)  # e.g., "AK47 / CZ 809 BREN"

    # Caliber designation stored *exactly as used operationally*
    caliber = Column(String, nullable=False)  # e.g., "7.62×39mm"

    # Current on-hand inventory
    count = Column(Integer, nullable=False, default=0)

    # Relationship with Weapon model
    weapon = relationship("Weapon", back_populates="ammunition")
    bookings = relationship("Booking", back_populates="ammunition", cascade="all, delete-orphan")

    # Optional — when to alert low stock (UI can use this)
    reorder_level = Column(Integer, nullable=False, default=0)

    # Optional location/bin code in the armory
    bin_location = Column(String)

    # Audit field
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("platform", "caliber", name="uq_ammo_platform_caliber"),
        Index("ix_ammo_caliber", "caliber"),
    )
