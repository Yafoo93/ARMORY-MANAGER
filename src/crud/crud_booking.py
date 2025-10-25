from datetime import datetime

from sqlalchemy.orm import Session

from src.models.ammunition import Ammunition
from src.models.booking import Booking


def create_booking(
    db: Session,
    officer_id: int,
    armorer_id: int,
    weapon_id: int | None,
    ammunition_id: int | None,
    ammunition_count: int | None,
    duty_point_id: int | None,
):
    """
    Creates a new booking record.
    Deducts ammunition from stock if applicable.
    """
    new_booking = Booking(
        officer_id=officer_id,
        armorer_id=armorer_id,
        weapon_id=weapon_id,
        ammunition_id=ammunition_id,
        ammunition_count=ammunition_count,
        duty_point_id=duty_point_id,
        status="active",
        issued_at=datetime.now(),
    )

    # Deduct ammo stock
    if ammunition_id and ammunition_count:
        ammo = db.query(Ammunition).get(ammunition_id)
        if not ammo:
            raise ValueError("Ammunition not found.")
        if ammo.count < ammunition_count:
            raise ValueError("Insufficient ammunition in stock.")
        ammo.count -= ammunition_count

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def return_booking(
    db: Session,
    booking_id: int,
    ammunition_returned: int | None = None,
    remarks: str | None = None,
):
    """
    Marks a booking as returned.
    Updates ammo stock and logs remarks for missing ammo.
    """
    booking = db.query(Booking).get(booking_id)
    if not booking:
        raise ValueError("Booking not found.")

    booking.returned_at = datetime.now()
    booking.status = "returned"
    booking.ammunition_returned = ammunition_returned

    # Adjust ammo stock
    if booking.ammunition_id and ammunition_returned is not None:
        ammo = db.query(Ammunition).get(booking.ammunition_id)
        if ammo:
            ammo.count += ammunition_returned
        if booking.ammunition_count is not None and ammunition_returned < booking.ammunition_count:
            diff = booking.ammunition_count - ammunition_returned
            booking.remarks = f"{remarks or ''} (Missing {diff} rounds)"

    db.commit()
    db.refresh(booking)
    return booking


def list_bookings(db: Session, limit: int = 100):
    """
    Returns the most recent bookings.
    """
    return db.query(Booking).order_by(Booking.issued_at.desc()).limit(limit).all()
