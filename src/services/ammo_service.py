from sqlalchemy.orm import Session

from src.models.ammunition import Ammunition


class AmmoService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(
        self, category: str, platform: str, caliber: str, weapon_id: int | None = None
    ) -> Ammunition:
        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .first()
        )
        if ammo:
            return ammo

        if not weapon_id:
            # fallback: assign first weapon id if not provided
            from src.models.weapon import Weapon

            first_weapon = self.db.query(Weapon).first()
            if not first_weapon:
                raise ValueError("No weapon found in DB. Seed weapons first.")
            weapon_id = first_weapon.id

        ammo = Ammunition(
            weapon_id=weapon_id, category=category, platform=platform, caliber=caliber, count=0
        )
        self.db.add(ammo)
        self.db.commit()
        self.db.refresh(ammo)
        return ammo

    def add_stock(self, platform: str, caliber: str, qty: int, category: str = None) -> int:
        """
        Add ammunition to stock. Automatically creates entry if missing.
        """
        if qty <= 0:
            return self.current_stock(platform, caliber)

        ammo = (
            self.db.query(Ammunition)
            .filter(Ammunition.platform == platform, Ammunition.caliber == caliber)
            .with_for_update(nowait=False)
            .first()
        )

        if not ammo:
            # Automatically create new ammo record if missing
            ammo = Ammunition(
                category=category or self.infer_category(caliber),
                platform=platform,
                caliber=caliber,
                count=0,
            )
            self.db.add(ammo)
            self.db.commit()
            self.db.refresh(ammo)

        ammo.count += qty
        self.db.commit()
        self.db.refresh(ammo)
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
        """Infer weapon category by caliber heuristics"""
        cal = caliber.lower()
        if "bb" in cal or "12" in cal or "shot" in cal:
            return "Shotgun"
        if "9×19" in cal or "9x19" in cal or "9mm" in cal:
            return "Pistol/SMG"
        return "Rifle"
