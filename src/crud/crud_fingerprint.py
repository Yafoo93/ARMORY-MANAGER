from sqlalchemy.orm import Session

from src.models.fingerprint import Fingerprint


def enroll_fingerprint(db: Session, user_id: int, template_data: bytes):
    """Store a fingerprint template for a user."""
    # Fingerprint model column is named `template`
    fingerprint = Fingerprint(user_id=user_id, template=template_data)
    db.add(fingerprint)
    db.commit()
    db.refresh(fingerprint)
    return fingerprint


def get_fingerprint_by_user(db: Session, user_id: int):
    """Retrieve a user's stored fingerprint."""
    return db.query(Fingerprint).filter(Fingerprint.user_id == user_id).first()


def verify_fingerprint(db: Session, scanned_template: bytes):
    """
    Compare scanned fingerprint template with stored templates.
    In production, use SDK’s matching function. This is a placeholder.
    """
    fingerprints = db.query(Fingerprint).all()
    for f in fingerprints:
        if f.template == scanned_template:  # Replace with actual match algorithm
            return f.user_id
    return None
