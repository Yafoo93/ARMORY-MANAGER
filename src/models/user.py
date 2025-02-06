class User:
    def __init__(self, service_number: str, name: str, telephone: str, role: str, fingerprint_id: int = None):
        self.service_number = service_number
        self.name = name
        self.telephone = telephone
        self.role = role
        self.fingerprint_id = fingerprint_id

    def __repr__(self):
        return f"User(service_number={self.service_number}, name={self.name}, role={self.role})"

    def to_dict(self):
        return {
            "service_number": self.service_number,
            "name": self.name,
            "telephone": self.telephone,
            "role": self.role,
            "fingerprint_id": self.fingerprint_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            service_number=data["service_number"],
            name=data["name"],
            telephone=data["telephone"],
            role=data["role"],
            fingerprint_id=data.get("fingerprint_id"),
        )