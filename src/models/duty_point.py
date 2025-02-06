class DutyPoint:
    def __init__(self, location: str, description: str = None):
        self.location = location
        self.description = description

    def __repr__(self):
        return f"DutyPoint(location={self.location})"

    def to_dict(self):
        return {
            "location": self.location,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            location=data["location"],
            description=data.get("description"),
        )