# src/crud/crud_duty_point.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models.duty_point import DutyPoint

def create_duty_point(db: Session, location: str, description: str | None = None):
    dp = DutyPoint(location=location.strip(), description=(description or "").strip() or None)
    db.add(dp)
    try:
        db.commit()
        db.refresh(dp)
        return dp, None
    except IntegrityError as e:
        db.rollback()
        return None, "Duty point with this location already exists."
    except Exception as e:
        db.rollback()
        return None, str(e)

def get_all_duty_points(db: Session):
    return db.query(DutyPoint).order_by(DutyPoint.location.asc()).all()

def delete_duty_point(db: Session, dp_id: int) -> tuple[bool, str | None]:
    dp = db.query(DutyPoint).filter(DutyPoint.id == dp_id).first()
    if not dp:
        return False, "Not found."
    try:
        db.delete(dp)
        db.commit()
        return True, None
    except Exception as e:
        db.rollback()
        return False, str(e)
