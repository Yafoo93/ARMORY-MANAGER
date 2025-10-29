# src/crud/crud_booking.py
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from src.models.ammunition import Ammunition
from src.models.booking import Booking
from src.models.duty_point import DutyPoint
from src.models.user import User
from src.models.weapon import Weapon


def list_bookings(db):
    """Return all bookings with related data loaded."""
    return (
        db.query(Booking)
        .options(
            joinedload(Booking.officer),
            joinedload(Booking.weapon),
            joinedload(Booking.duty_point),
            joinedload(Booking.ammunition),
        )
        .order_by(Booking.issued_at.desc())
        .all()
    )


def _get_or_fail(db: Session, model, id_: int, label: str):
    obj = db.get(model, id_)
    if not obj:
        raise ValueError(f"{label} not found (id={id_})")
    return obj


def create_booking(
    db: Session,
    *,
    officer_id: int,
    weapon_id: int,
    duty_point_id: int,
    armorer_id: int,
    ammunition_id: Optional[int] = None,
    ammunition_count: int = 0,
    remarks: Optional[str] = None,
) -> Booking:
    """
    Create a booking:
      - Validates officer/weapon/duty_point.
      - If ammunition_count>0 then ammunition_id is required and stock >= count.
      - Deducts stock immediately.
      - Marks weapon status = 'ISSUED' (string status model).
      - Sets issued_at and status='ISSUED'.
    """
    officer = _get_or_fail(db, User, officer_id, "Officer")
    armorer = _get_or_fail(db, User, armorer_id, "Armorer")
    weapon = _get_or_fail(db, Weapon, weapon_id, "Weapon")
    duty_point = _get_or_fail(db, DutyPoint, duty_point_id, "Duty point")

    if weapon.status and weapon.status.upper() in {"ISSUED", "ASSIGNED", "UNAVAILABLE"}:
        raise ValueError(f"Weapon {weapon.serial_number} is not available")

    ammo_obj = None
    if ammunition_count and ammunition_count > 0:
        if ammunition_id is None:
            raise ValueError("Ammunition is required when ammunition_count > 0")
        ammo_obj = _get_or_fail(db, Ammunition, ammunition_id, "Ammunition")
        if ammo_obj.count is None:
            ammo_obj.count = 0
        if ammo_obj.count < ammunition_count:
            raise ValueError(
                f"Insufficient stock for {ammo_obj.platform} {ammo_obj.caliber}: "
                f"have {ammo_obj.count}, need {ammunition_count}"
            )
        # Deduct stock
        ammo_obj.count -= ammunition_count

    # Create booking
    booking = Booking(
        officer_id=officer.id,
        armorer_id=armorer.id,
        weapon_id=weapon.id,
        duty_point_id=duty_point.id,
        ammunition_id=ammo_obj.id if ammo_obj else None,
        ammunition_count=ammunition_count or 0,
        remarks=remarks,
        issued_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        status="ISSUED",
    )

    # Mark weapon out
    weapon.status = "ISSUED"

    db.add(booking)
    db.flush()  # assign id
    db.commit()
    db.refresh(booking)
    return booking


def return_booking(
    db: Session,
    *,
    booking_id: int,
    ammunition_returned: int,
    remarks: Optional[str],
    weapon_status: Optional[str] = None,
) -> Booking:
    """
    Return a booking:
      - Must not already be returned.
      - Restores ammunition stock (if booking had ammunition_id).
      - Remarks are optional.
      - Sets returned_at and status='RETURNED'.
    """
    booking = _get_or_fail(db, Booking, booking_id, "Booking")

    # Normalize status whether Enum or string
    status_text = None
    if booking.status is not None:
        status_text = getattr(booking.status, "value", None)
        if not isinstance(status_text, str):
            status_text = str(booking.status)
        if status_text.startswith("BookingStatus."):
            status_text = status_text.split(".", 1)[1]
    if (status_text or "").upper() == "RETURNED":
        raise ValueError("This booking is already returned")

    if ammunition_returned is None or ammunition_returned < 0:
        raise ValueError("Invalid returned ammunition count")

    # Remarks are optional regardless of mismatch

    # Restore stock if applicable
    if booking.ammunition_id:
        ammo_obj = _get_or_fail(db, Ammunition, booking.ammunition_id, "Ammunition")
        if ammo_obj.count is None:
            ammo_obj.count = 0
        ammo_obj.count += ammunition_returned

    # Close booking
    booking.ammunition_returned = ammunition_returned
    booking.remarks = remarks
    booking.returned_at = datetime.utcnow()
    booking.status = "RETURNED"

    # Free weapon
    weapon = _get_or_fail(db, Weapon, booking.weapon_id, "Weapon")
    # Determine final weapon status
    final_status = (weapon_status or "AVAILABLE").strip().upper()
    allowed_status = {"AVAILABLE", "DAMAGED", "MISSING"}
    if final_status not in allowed_status:
        final_status = "AVAILABLE"
    weapon.status = final_status

    db.commit()
    db.refresh(booking)
    return booking
