class Ammunition:
    def __init__(self, weapon_id: int, count: int):
        self.weapon_id = weapon_id
        self.count = count

    def __repr__(self):
        return f"Ammunition(weapon_id={self.weapon_id}, count={self.count})"

    def to_dict(self):
        return {
            "weapon_id": self.weapon_id,
            "count": self.count,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            weapon_id=data["weapon_id"],
            count=data["count"],
        )