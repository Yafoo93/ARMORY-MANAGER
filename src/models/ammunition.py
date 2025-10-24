from sqlalchemy import Column, DateTime, Index, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from src.database import Base


class Ammunition(Base):
    __tablename__ = "ammunition"

    id = Column(Integer, primary_key=True)

    # High-level grouping (e.g., "Rifle", "Pistol/SMG", "Shotgun")
    category = Column(String, nullable=False)  # e.g., "Rifle", "Pistol/SMG", "Shotgun"

    # Platform/model family label for clarity in reports
    platform = Column(String, nullable=False)  # e.g., "AK47 / CZ 809 BREN"

    # Caliber designation stored *exactly as used operationally*
    caliber = Column(String, nullable=False)  # e.g., "7.62×39mm"

    # Current on-hand inventory
    count = Column(Integer, nullable=False, default=0)

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
