class Record:
    def __init__(self, officer_id: int, weapon_id: int, duty_point_id: int, ammo_issued: int, time_booked: str, time_returned: str = None):
        self.officer_id = officer_id
        self.weapon_id = weapon_id
        self.duty_point_id = duty_point_id
        self.ammo_issued = ammo_issued
        self.time_booked = time_booked
        self.time_returned = time_returned

    def __repr__(self):
        return f"Record(officer_id={self.officer_id}, weapon_id={self.weapon_id}, time_booked={self.time_booked})"

    def to_dict(self):
        return {
            "officer_id": self.officer_id,
            "weapon_id": self.weapon_id,
            "duty_point_id": self.duty_point_id,
            "ammo_issued": self.ammo_issued,
            "time_booked": self.time_booked,
            "time_returned": self.time_returned,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            officer_id=data["officer_id"],
            weapon_id=data["weapon_id"],
            duty_point_id=data["duty_point_id"],
            ammo_issued=data["ammo_issued"],
            time_booked=data["time_booked"],
            time_returned=data.get("time_returned"),
        )