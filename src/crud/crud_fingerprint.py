from sqlalchemy.orm import Session
from src.models.fingerprint import Fingerprint

# Create a new fingerprint entry
def create_fingerprint(db: Session, user_id: int, template: bytes):
    new_fingerprint = Fingerprint(user_id=user_id, template=template)
    db.add(new_fingerprint)
    db.commit()
    db.refresh(new_fingerprint)
    return new_fingerprint

# Get a fingerprint by ID
def get_fingerprint(db: Session, fingerprint_id: int):
    return db.query(Fingerprint).filter(Fingerprint.id == fingerprint_id).first()

# Get a fingerprint by User ID
def get_fingerprint_by_user(db: Session, user_id: int):
    return db.query(Fingerprint).filter(Fingerprint.user_id == user_id).first()

# Get all fingerprints
def get_all_fingerprints(db: Session):
    return db.query(Fingerprint).all()

# Update a fingerprint template
def update_fingerprint(db: Session, fingerprint_id: int, template: bytes):
    fingerprint = db.query(Fingerprint).filter(Fingerprint.id == fingerprint_id).first()
    if fingerprint:
        fingerprint.template = template
        db.commit()
        db.refresh(fingerprint)
    return fingerprint

# Delete a fingerprint entry
def delete_fingerprint(db: Session, fingerprint_id: int):
    fingerprint = db.query(Fingerprint).filter(Fingerprint.id == fingerprint_id).first()
    if fingerprint:
        db.delete(fingerprint)
        db.commit()
    return fingerprint
