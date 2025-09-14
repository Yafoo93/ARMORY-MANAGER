from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.ammunition import Ammunition

def list_ammunition(
    db_session: Session,
    query_text: str = "",
    limit: int = 200,
    offset: int = 0
) -> List[Ammunition]:
    q = db_session.query(Ammunition)
    if query_text:
        like = f"%{query_text.strip()}%"
        q = q.filter(
            or_(
                Ammunition.category.ilike(like),
                Ammunition.platform.ilike(like),
                Ammunition.caliber.ilike(like),
                Ammunition.bin_location.ilike(like),
            )
        )
    q = q.order_by(Ammunition.platform.asc(), Ammunition.caliber.asc())
    if limit:
        q = q.limit(limit)
    if offset:
        q = q.offset(offset)
    return q.all()

def create_ammunition(
    db_session: Session,
    category: str,
    platform: str,
    caliber: str,
    count: int = 0,
    reorder_level: int = 0,
    bin_location: Optional[str] = None,
) -> Ammunition:
    existing = (
        db_session.query(Ammunition)
        .filter(Ammunition.platform == platform.strip(),
                Ammunition.caliber == caliber.strip())
        .first()
    )
    if existing:
        return existing
    ammo = Ammunition(
        category=category.strip(),
        platform=platform.strip(),
        caliber=caliber.strip(),
        count=max(0, int(count or 0)),
        reorder_level=max(0, int(reorder_level or 0)),
        bin_location=(bin_location or "").strip() or None,
    )
    db_session.add(ammo)
    db_session.commit()
    db_session.refresh(ammo)
    return ammo

def update_ammunition(
    db_session: Session,
    ammo_id: int,
    category: Optional[str] = None,
    platform: Optional[str] = None,
    caliber: Optional[str] = None,
    reorder_level: Optional[int] = None,
    bin_location: Optional[str] = None,
) -> Optional[Ammunition]:
    ammo = db_session.query(Ammunition).get(ammo_id)
    if not ammo:
        return None
    if category is not None:
        ammo.category = category.strip()
    if platform is not None:
        ammo.platform = platform.strip()
    if caliber is not None:
        ammo.caliber = caliber.strip()
    if reorder_level is not None:
        ammo.reorder_level = max(0, int(reorder_level))
    if bin_location is not None:
        ammo.bin_location = bin_location.strip() or None
    db_session.commit()
    db_session.refresh(ammo)
    return ammo

def delete_ammunition(db_session: Session, ammo_id: int) -> bool:
    ammo = db_session.query(Ammunition).get(ammo_id)
    if not ammo:
        return False
    db_session.delete(ammo)
    db_session.commit()
    return True

def adjust_stock(db_session: Session, ammo_id: int, delta: int) -> Optional[Ammunition]:
    """Positive delta = add; negative delta = consume (but not below zero)."""
    ammo = db_session.query(Ammunition).get(ammo_id)
    if not ammo:
        return None
    new_count = int(ammo.count or 0) + int(delta)
    if new_count < 0:
        new_count = 0
    ammo.count = new_count
    db_session.commit()
    db_session.refresh(ammo)
    return ammo

def get_ammunition_by_id(db_session: Session, ammo_id: int) -> Optional[Ammunition]:
    return db_session.query(Ammunition).get(ammo_id)
