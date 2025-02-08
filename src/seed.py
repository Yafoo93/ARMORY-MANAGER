import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import SessionLocal, init_db
from src.models.user import User
from src.models.weapon import Weapon
from src.models.ammunition import Ammunition
from src.models.duty_point import DutyPoint
from src.models.record import Record
from src.models.fingerprint import Fingerprint
from datetime import datetime

# Initialize database
init_db()

# Create a database session
session = SessionLocal()

# Insert Sample Users
user1 = User(service_number="GHA123", name="John Doe", telephone="0541234567", role="officer")
user2 = User(service_number="GHA124", name="Jane Smith", telephone="0547654321", role="armory_manager")

# Insert Sample Weapons
weapon1 = Weapon(serial_number="WPN001", type="Rifle", condition="Good", location="Armory")
weapon2 = Weapon(serial_number="WPN002", type="Pistol", condition="Fair", location="Armory")

# Insert Sample Ammunition
ammo1 = Ammunition(weapon_id=1, count=30)
ammo2 = Ammunition(weapon_id=2, count=15)

# Insert Sample Duty Points
duty1 = DutyPoint(location="Patrol Zone A", description="Main patrol duty point")
duty2 = DutyPoint(location="Station Security", description="Internal station security")

# Insert Sample Records
record1 = Record(officer_id=1, weapon_id=1, duty_point_id=1, ammo_issued=30, time_booked=datetime.utcnow())
record2 = Record(officer_id=2, weapon_id=2, duty_point_id=2, ammo_issued=15, time_booked=datetime.utcnow())

# Insert Sample Fingerprints (Dummy data)
fingerprint1 = Fingerprint(template=b"fingerprint_data_1", user_id=1)
fingerprint2 = Fingerprint(template=b"fingerprint_data_2", user_id=2)

# Add and commit data to the database
session.add_all([user1, user2, weapon1, weapon2, ammo1, ammo2, duty1, duty2, record1, record2, fingerprint1, fingerprint2])
session.commit()

print("✅ Sample data inserted successfully!")

# Close session
session.close()
