from sqlalchemy.orm import Session
from src.models.ammunition import Ammunition

# Create new ammunition entry
def create_ammunition(db: Session, weapon_id: int, count: int):
    new_ammunition = Ammunition(weapon_id=weapon_id, count=count)
    db.add(new_ammunition)
    db.commit()
    db.refresh(new_ammunition)
    return new_ammunition

# Get ammunition by ID
def get_ammunition(db: Session, ammo_id: int):
    return db.query(Ammunition).filter(Ammunition.id == ammo_id).first()

# Get all ammunition
def get_all_ammunition(db: Session):
    return db.query(Ammunition).all()

# Update ammunition count
def update_ammunition(db: Session, ammo_id: int, count: int):
    ammo = db.query(Ammunition).filter(Ammunition.id == ammo_id).first()
    if ammo:
        ammo.count = count
        db.commit()
        db.refresh(ammo)
    return ammo

# Delete ammunition entry
def delete_ammunition(db: Session, ammo_id: int):
    ammo = db.query(Ammunition).filter(Ammunition.id == ammo_id).first()
    if ammo:
        db.delete(ammo)
        db.commit()
    return ammo
