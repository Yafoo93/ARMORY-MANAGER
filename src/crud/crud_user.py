from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.user import User


# Create a new user (hashes password with User.set_password)
def create_user(
    db: Session,
    service_number: str,
    name: str,
    telephone: str,
    unit: str,
    role: str,
    password: str,
) -> bool:
    user = User(
        service_number=service_number.strip(),
        name=name.strip(),
        telephone=telephone.strip(),
        unit=(unit or "").strip(),
        role=(role or "officer").strip().lower(),
    )
    user.set_password(password)

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return True
    except IntegrityError:
        db.rollback()
        return False


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.desc()).all()


def update_user(
    db: Session,
    user_id: int,
    name: str | None = None,
    telephone: str | None = None,
    role: str | None = None,
    unit: str | None = None,
) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if name:
        user.name = name.strip()
    if telephone:
        user.telephone = telephone.strip()
    if unit is not None:
        user.unit = unit.strip()
    if role:
        user.role = role.strip().lower()

    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
    """Reset/change a user's password using bcrypt via model helper."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    user.set_password(new_password)
    db.commit()
    return True


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
