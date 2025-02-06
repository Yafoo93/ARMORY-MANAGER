class Weapon:
    def __init__(self, serial_number: str, type: str, condition: str, location: str, status: str = "in-stock"):
        self.serial_number = serial_number
        self.type = type
        self.condition = condition
        self.location = location
        self.status = status

    def __repr__(self):
        return f"Weapon(serial_number={self.serial_number}, type={self.type}, status={self.status})"

    def to_dict(self):
        return {
            "serial_number": self.serial_number,
            "type": self.type,
            "condition": self.condition,
            "location": self.location,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            serial_number=data["serial_number"],
            type=data["type"],
            condition=data["condition"],
            location=data["location"],
            status=data.get("status", "in-stock"),  # Default status is "in-stock"
        )