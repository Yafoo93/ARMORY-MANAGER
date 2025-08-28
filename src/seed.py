import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import bcrypt
from src.database import SessionLocal, init_db
from src.models.user import User
from src.models.weapon import Weapon
from src.models.ammunition import Ammunition
from src.models.duty_point import DutyPoint
from src.models.record import Record
from src.models.fingerprint import Fingerprint

# Initialize database
init_db()
session = SessionLocal()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


# Insert Sample Users with Hashed Passwords
user1 = User(
    service_number="GHA123",
    name="John Doe",
    telephone="0541234567",
    role="officer"
)
user1.set_password("officer123")

user2 = User(
    service_number="GHA124",
    name="Jane Smith",
    telephone="0547654321",
    role="armorer"
)
user2.set_password("manager123")



# Insert Sample Weapons
weapon1 = Weapon(serial_number="WPN001", type="Rifle", condition="Good", location="Armory")
weapon2 = Weapon(serial_number="WPN002", type="Pistol", condition="Fair", location="Armory")

# Insert Sample Ammunition
ammo1 = Ammunition(weapon_id=1, count=30)
ammo2 = Ammunition(weapon_id=2, count=15)

# ✅ Fix: Ensure duty points are always defined before use
duty1 = session.query(DutyPoint).filter_by(location="Patrol Zone A").first()
if not duty1:
    duty1 = DutyPoint(location="Patrol Zone A", description="Main patrol duty point")
    session.add(duty1)
    
duty2 = session.query(DutyPoint).filter_by(location="Station Security").first()
if not duty2:
    duty2 = DutyPoint(location="Station Security", description="Internal station security")
    session.add(duty2)

# ✅ Commit duty points before using them
session.commit()

# ✅ Ensure duty1 and duty2 exist before using them
weapon1 = Weapon(serial_number="WPN001", type="Rifle", condition="Good", location="Armory", status="Excellent")
weapon2 = Weapon(serial_number="WPN002", type="Pistol", condition="Fair", location="Armory", status="Good")


ghana_tz = ZoneInfo("Africa/Accra")
now_ghana = datetime.now(ghana_tz)
# Insert Sample Records
record1 = Record(officer_id=1, weapon_id=1, duty_point_id=duty1.id, ammo_issued=30, time_booked=now_ghana)
record2 = Record(officer_id=2, weapon_id=2, duty_point_id=duty2.id, ammo_issued=15, time_booked=now_ghana)

# Insert Sample Fingerprints (Dummy data)
fingerprint1 = Fingerprint(template=b"fingerprint_data_1", user_id=1)
fingerprint2 = Fingerprint(template=b"fingerprint_data_2", user_id=2)

# ✅ Add everything and commit
session.add_all([user1, user2, weapon1, weapon2, ammo1, ammo2, record1, record2, fingerprint1, fingerprint2])
session.commit()

print("✅ Sample data inserted successfully!")

# Close session
session.close()
