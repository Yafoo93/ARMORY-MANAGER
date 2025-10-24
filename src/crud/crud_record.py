from datetime import datetime

from sqlalchemy.orm import Session

from src.models.record import Record


# Create a new record
def create_record(
    db: Session, officer_id: int, weapon_id: int, duty_point_id: int, ammo_issued: int
):
    new_record = Record(
        officer_id=officer_id,
        weapon_id=weapon_id,
        duty_point_id=duty_point_id,
        ammo_issued=ammo_issued,
        time_booked=datetime.utcnow(),
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


# Get a record by ID
def get_record(db: Session, record_id: int):
    return db.query(Record).filter(Record.id == record_id).first()


# Get all records
def get_all_records(db: Session):
    return db.query(Record).all()


# Update a record (returning weapon)
def update_record(db: Session, record_id: int):
    record = db.query(Record).filter(Record.id == record_id).first()
    if record and record.time_returned is None:
        record.time_returned = datetime.utcnow()
        db.commit()
        db.refresh(record)
    return record


# Delete a record
def delete_record(db: Session, record_id: int):
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record
