from sqlalchemy.orm import Session
from src.models.duty_point import DutyPoint

# Create a new duty point
def create_duty_point(db: Session, location: str, description: str = None):
    new_duty_point = DutyPoint(location=location, description=description)
    db.add(new_duty_point)
    db.commit()
    db.refresh(new_duty_point)
    return new_duty_point

# Get a duty point by ID
def get_duty_point(db: Session, duty_point_id: int):
    return db.query(DutyPoint).filter(DutyPoint.id == duty_point_id).first()

# Get all duty points
def get_all_duty_points(db: Session):
    return db.query(DutyPoint).all()

# Update a duty point
def update_duty_point(db: Session, duty_point_id: int, location: str = None, description: str = None):
    duty_point = db.query(DutyPoint).filter(DutyPoint.id == duty_point_id).first()
    if duty_point:
        if location:
            duty_point.location = location
        if description:
            duty_point.description = description
        db.commit()
        db.refresh(duty_point)
    return duty_point

# Delete a duty point
def delete_duty_point(db: Session, duty_point_id: int):
    duty_point = db.query(DutyPoint).filter(DutyPoint.id == duty_point_id).first()
    if duty_point:
        db.delete(duty_point)
        db.commit()
    return duty_point
