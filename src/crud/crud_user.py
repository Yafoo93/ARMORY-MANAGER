from sqlalchemy.orm import Session
from src.models.user import User

# Create a new user
def create_user(db: Session, service_number: str, name: str, telephone: str, role: str):
    new_user = User(service_number=service_number, name=name, telephone=telephone, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Get all users
def get_all_users(db: Session):
    return db.query(User).all()

# Update a user
def update_user(db: Session, user_id: int, name: str = None, telephone: str = None, role: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if name:
            user.name = name
        if telephone:
            user.telephone = telephone
        if role:
            user.role = role
        db.commit()
        db.refresh(user)
    return user

# Delete a user
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
