class Fingerprint:
    def __init__(self, template: bytes, user_id: int):
        self.template = template
        self.user_id = user_id

    def __repr__(self):
        return f"Fingerprint(user_id={self.user_id})"

    def to_dict(self):
        return {
            "template": self.template,
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            template=data["template"],
            user_id=data["user_id"],
        )