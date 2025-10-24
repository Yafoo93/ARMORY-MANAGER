from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.ammunition import Ammunition


class AmmoService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, category: str, platform: str, caliber: str) -> Ammunition:
        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .first()
        )
        if ammo:
            return ammo
        ammo = Ammunition(category=category, platform=platform, caliber=caliber, count=0)
        self.db.add(ammo)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            ammo = (
                self.db.query(Ammunition)
                .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
                .first()
            )
        return ammo

    def add_stock(self, platform: str, caliber: str, qty: int) -> int:
        if qty <= 0:
            return self.current_stock(platform, caliber)
        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .with_for_update(nowait=False)
            .first()
        )
        if not ammo:
            ammo = self.get_or_create(self.infer_category(caliber), platform, caliber)
        ammo.count += qty
        self.db.commit()
        return ammo.count

    def consume_stock(self, platform: str, caliber: str, qty: int) -> int:
        if qty <= 0:
            return self.current_stock(platform, caliber)
        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .with_for_update(nowait=False)
            .first()
        )
        if not ammo or ammo.count < qty:
            raise ValueError("Insufficient ammunition")
        ammo.count -= qty
        self.db.commit()
        return ammo.count

    def current_stock(self, platform: str, caliber: str) -> int:
        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .first()
        )
        return ammo.count if ammo else 0

    @staticmethod
    def infer_category(caliber: str) -> str:
        # quick heuristic; you can make this explicit in seed instead
        cal = caliber.lower()
        if "bb" in cal or "12" in cal or "shot" in cal:
            return "Shotgun"
        if "9×19" in cal or "9x19" in cal or "9mm" in cal:
            return "Pistol/SMG"
        return "Rifle"
