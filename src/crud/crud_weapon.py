from sqlalchemy.orm import Session
from src.models.weapon import Weapon

# Create a new weapon
def create_weapon(db: Session, weapon_type: str, serial_number: str, status: str, condition: str):
    """Create a new weapon record"""
    weapon = Weapon(
        type=weapon_type,
        serial_number=serial_number,
        status=status,
        condition=condition
    )
    db.add(weapon)
    db.commit()
    db.refresh(weapon)
    return weapon

# Get a weapon by ID
def get_weapon_by_id(db: Session, weapon_id: int):
    """Get a specific weapon by ID"""
    return db.query(Weapon).filter(Weapon.id == weapon_id).first()

# Get all weapons
def get_all_weapons(db: Session):
    """Retrieve all weapons"""
    return db.query(Weapon).all()

# Update a weapon
def update_weapon(db: Session, weapon_id: int, weapon_type: str, serial_number: str, status: str, condition: str):
    """Update weapon details"""
    weapon = get_weapon_by_id(db, weapon_id)
    if weapon:
        weapon.type = weapon_type
        weapon.serial_number = serial_number
        weapon.status = status
        weapon.condition = condition
        db.commit()
        db.refresh(weapon)
        return weapon
    return None

# Delete a weapon
def delete_weapon(db: Session, weapon_id: int):
    """Delete a weapon"""
    weapon = get_weapon_by_id(db, weapon_id)
    if weapon:
        db.delete(weapon)
        db.commit()
        return True
    return False
