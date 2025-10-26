from datetime import datetime

from sqlalchemy.orm import Session

from src.models.ammunition import Ammunition
from src.models.booking import Booking
from src.models.duty_point import DutyPoint
from src.models.user import User
from src.models.weapon import Weapon


def create_booking(
    db: Session,
    *,
    officer_id: int,
    armorer_id: int,
    weapon_id: int,
    duty_point_id: int,
    ammunition_id: int | None = None,
    ammunition_count: int = 0,
) -> Booking:
    """Create a booking and flip weapon status to ISSUED."""
    weapon = db.query(Weapon).get(weapon_id)
    if not weapon:
        raise ValueError("Selected weapon does not exist.")
    if getattr(weapon, "status", None) != "AVAILABLE":
        raise ValueError("Weapon is not available.")

    dp = db.query(DutyPoint).get(duty_point_id)
    if not dp:
        raise ValueError("Selected duty point does not exist.")

    if ammunition_id is not None:
        ammo = db.query(Ammunition).get(ammunition_id)
        if not ammo:
            raise ValueError("Selected ammunition does not exist.")
        if ammunition_count is None:
            ammunition_count = 0

    booking = Booking(
        officer_id=officer_id,
        armorer_id=armorer_id,
        weapon_id=weapon_id,
        duty_point_id=duty_point_id,
        ammunition_id=ammunition_id,
        ammunition_count=ammunition_count or 0,
        issued_at=datetime.now(),
        status="ISSUED",
    )

    weapon.status = "ISSUED"
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def return_booking(
    db: Session,
    *,
    booking_id: int,
    ammunition_returned: int | None = None,
) -> Booking:
    """Mark booking returned, flip weapon to AVAILABLE."""
    booking = db.query(Booking).get(booking_id)
    if not booking:
        raise ValueError("Booking not found.")
    if booking.status == "RETURNED":
        return booking

    booking.status = "RETURNED"
    booking.returned_at = datetime.now()
    if ammunition_returned is not None:
        booking.ammunition_returned = ammunition_returned

    weapon = db.query(Weapon).get(booking.weapon_id)
    if weapon:
        weapon.status = "AVAILABLE"

    db.commit()
    db.refresh(booking)
    return booking


def list_bookings(db, limit: int = 50):
    """Return all bookings safely even if relationships are missing."""
    return (
        db.query(Booking)
        .outerjoin(User, Booking.officer_id == User.id)
        .outerjoin(Weapon, Booking.weapon_id == Weapon.id)
        .outerjoin(DutyPoint, Booking.duty_point_id == DutyPoint.id)
        .outerjoin(Ammunition, Booking.ammunition_id == Ammunition.id)
        .order_by(Booking.issued_at.desc())
        .limit(limit)
        .all()
    )
