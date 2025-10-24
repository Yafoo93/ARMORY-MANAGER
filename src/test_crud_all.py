import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import after path modification
from src.crud.crud_weapon import create_weapon, get_all_weapons  # noqa: E402
from src.database import SessionLocal  # noqa: E402

db = SessionLocal()

# Create a test weapon
weapon = create_weapon(db, "WPN003", "Shotgun", "Good", "HQ Armory")
print(f"✅ Weapon created: {weapon}")

# Fetch all weapons
weapons = get_all_weapons(db)
print("✅ All Weapons:", weapons)

db.close()
