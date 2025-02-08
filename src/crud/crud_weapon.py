from sqlalchemy.orm import Session
from src.models.weapon import Weapon

# Create a new weapon
def create_weapon(db: Session, serial_number: str, type: str, condition: str, location: str, status: str = "in-stock"):
    new_weapon = Weapon(serial_number=serial_number, type=type, condition=condition, location=location, status=status)
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)
    return new_weapon

# Get a weapon by ID
def get_weapon(db: Session, weapon_id: int):
    return db.query(Weapon).filter(Weapon.id == weapon_id).first()

# Get all weapons
def get_all_weapons(db: Session):
    return db.query(Weapon).all()

# Update a weapon
def update_weapon(db: Session, weapon_id: int, condition: str = None, location: str = None, status: str = None):
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        if condition:
            weapon.condition = condition
        if location:
            weapon.location = location
        if status:
            weapon.status = status
        db.commit()
        db.refresh(weapon)
    return weapon

# Delete a weapon
def delete_weapon(db: Session, weapon_id: int):
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        db.delete(weapon)
        db.commit()
    return weapon
