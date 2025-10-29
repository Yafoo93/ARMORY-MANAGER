import os
import sys

if __package__ is None and not hasattr(sys, "frozen"):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from zoneinfo import ZoneInfo

import bcrypt
from sqlalchemy.exc import IntegrityError

from src.database import SessionLocal
from src.models.duty_point import DutyPoint
from src.models.fingerprint import Fingerprint
from src.models.record import Record
from src.models.shift import Shift
from src.models.user import User
from src.models.weapon import Weapon
from src.services.ammo_service import AmmoService


def hash_password(pw: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw.encode("utf-8"), salt).decode("utf-8")


def get_or_create_user(db_session, service_number, **kwargs) -> User:
    """
    Idempotent user upsert for seeding.
    Accepts optional: name, telephone, role, unit, password
    """
    # Extract password (don’t pass it directly into User constructor)
    plain_password = kwargs.pop("password", None)

    # Normalize role if provided
    if "role" in kwargs and kwargs["role"]:
        kwargs["role"] = kwargs["role"].strip().lower()

    # Look for an existing user with the same service number
    existing_user = db_session.query(User).filter_by(service_number=service_number).first()

    if existing_user:
        # Update only provided fields
        for field_name, field_value in kwargs.items():
            if field_value is not None and hasattr(existing_user, field_name):
                setattr(existing_user, field_name, field_value)

        # Update password if a new one is provided
        if plain_password:
            try:
                existing_user.set_password(plain_password)
            except AttributeError:
                existing_user.hashed_password = hash_password(plain_password)

        return existing_user

    # Create a new user
    new_user = User(service_number=service_number, **kwargs)

    # Set password (either provided or default)
    if plain_password:
        try:
            new_user.set_password(plain_password)
        except AttributeError:
            new_user.hashed_password = hash_password(plain_password)
    else:
        # Fallback default password for seed users
        try:
            new_user.set_password("changeme123")
        except AttributeError:
            new_user.hashed_password = hash_password("changeme123")

    db_session.add(new_user)
    return new_user


def get_or_create_duty_point(db, location, description="") -> DutyPoint:
    dp = db.query(DutyPoint).filter_by(location=location).first()
    if dp:
        return dp
    dp = DutyPoint(location=location, description=description or location)
    db.add(dp)
    return dp


def get_or_create_weapon(db, serial_number, **kwargs) -> Weapon:
    w = db.query(Weapon).filter_by(serial_number=serial_number).first()
    if w:
        # normalize/repair status if needed
        status = kwargs.get("status")
        if status and status not in {"AVAILABLE", "RESERVED", "ISSUED", "MAINTENANCE"}:
            status = "AVAILABLE"
        for k, v in {**kwargs, "status": status or kwargs.get("status")}.items():
            if v is not None and hasattr(w, k):
                setattr(w, k, v)
        return w
    status = kwargs.get("status") or "AVAILABLE"
    if status not in {"AVAILABLE", "RESERVED", "ISSUED", "MAINTENANCE"}:
        status = "AVAILABLE"
    w = Weapon(serial_number=serial_number, **{**kwargs, "status": status})
    db.add(w)
    return w


# -----------------------
# seed starts here
# -----------------------
session = SessionLocal()
ammo = AmmoService(session)

try:

    user1 = get_or_create_user(
        session,
        "GHA123",
        name="John Doe",
        telephone="0541234567",
        role="officer",
        unit="RPID",
        password="officer123",
    )
    user2 = get_or_create_user(
        session,
        "GHA124",
        name="Jane Smith",
        telephone="0547654321",
        role="armorer",
        unit="RPID",
        password="manager123",
    )
    mgr = get_or_create_user(
        session,
        "GP55351",
        name="Kassim Mutawakil",
        telephone="0240286508",
        role="armorer",
        unit="RPID",
        password="admin123",
    )

    # Duty points (idempotent)
    duty1 = get_or_create_duty_point(session, "Patrol Zone A", description="Main patrol duty point")
    duty2 = get_or_create_duty_point(session, "Barrier", description="Internal station security")

    session.flush()  # assign IDs before records

    # Weapons (idempotent + valid statuses)
    # Add optional caliber to help ammo matching downstream
    # Create or fetch weapons first
    w1 = get_or_create_weapon(
        session,
        "WPN001",
        type="Rifle",
        condition="Good",
        location="Armory",
        status="AVAILABLE",
    )
    w2 = get_or_create_weapon(
        session,
        "WPN002",
        type="Pistol",
        condition="Fair",
        location="Armory",
        status="AVAILABLE",
    )

    session.commit()
    session.refresh(w1)
    session.refresh(w2)

    # ✅ Create ammunition stock lines linked to specific weapons
    ammo.get_or_create("Rifle", "AK47 / CZ 809 BREN", "7.62×39mm", weapon_id=w1.id)
    ammo.get_or_create(
        "Pistol/SMG", "SideArm / Škorpion / SMG", "9×19mm Parabellum (9mm Luger)", weapon_id=w2.id
    )
    ammo.get_or_create("Shotgun", "Pump Action - Short Gun", "BB Cartridge", weapon_id=w1.id)
    ammo.get_or_create("Rifle", "G3", "7.62×51mm NATO", weapon_id=w1.id)
    ammo.get_or_create("Rifle", "CZ 805 BREN", "5.56×45mm NATO", weapon_id=w1.id)

    # ✅ Give some starting stock for demo/dev environment
    ammo.add_stock("AK47 / CZ 809 BREN", "7.62×39mm", 1200)
    ammo.add_stock("SideArm / Škorpion / SMG", "9×19mm Parabellum (9mm Luger)", 800)
    ammo.add_stock("Pump Action - Short Gun", "BB Cartridge", 300)
    ammo.add_stock("G3", "7.62×51mm NATO", 500)  # 👈 removed extra parenthesis here
    ammo.add_stock("CZ 805 BREN", "5.56×45mm NATO", 900)

    # Dummy fingerprints (idempotent-ish; only add if none exist for user)
    if not session.query(Fingerprint).filter_by(user_id=user1.id).first():
        session.add(Fingerprint(template=b"fingerprint_data_1", user_id=user1.id))
    if not session.query(Fingerprint).filter_by(user_id=user2.id).first():
        session.add(Fingerprint(template=b"fingerprint_data_2", user_id=user2.id))

    # Create one active shift for the armorer (so booking works immediately)
    active = session.query(Shift).filter(Shift.active.is_(True)).first()
    if not active:
        session.add(Shift(armorer_id=user2.id, active=True))

    # Example Records (idempotent check by (officer, weapon, time_booked) is brittle;
    # skip if any records exist)
    if session.query(Record).count() == 0:
        now_gh = datetime.now(ZoneInfo("Africa/Accra"))
        session.add_all(
            [
                Record(
                    officer_id=user1.id,
                    weapon_id=w1.id,
                    duty_point_id=duty1.id,
                    ammo_issued=30,
                    time_booked=now_gh,
                ),
                Record(
                    officer_id=user2.id,
                    weapon_id=w2.id,
                    duty_point_id=duty2.id,
                    ammo_issued=15,
                    time_booked=now_gh,
                ),
            ]
        )

    session.commit()
    print("✅ Seed completed (idempotent).")

except IntegrityError as e:
    session.rollback()
    print("❌ IntegrityError during seed:", e)

finally:
    session.close()
