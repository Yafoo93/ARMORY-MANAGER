from models.user import User
from models.weapon import Weapon
from models.ammunition import Ammunition
from models.duty_point import DutyPoint
from models.record import Record
from models.fingerprint import Fingerprint

def test_models():
    # Test User model
    user = User(service_number="12345", name="John Doe", telephone="0551234567", role="officer")
    user_dict = user.to_dict()
    new_user = User.from_dict(user_dict)
    print("User:", new_user)

    # Test Weapon model
    weapon = Weapon(serial_number="W123", type="firearm", condition="new", location="Armory A")
    weapon_dict = weapon.to_dict()
    new_weapon = Weapon.from_dict(weapon_dict)
    print("Weapon:", new_weapon)

    # Test Ammunition model
    ammo = Ammunition(weapon_id=1, count=50)
    ammo_dict = ammo.to_dict()
    new_ammo = Ammunition.from_dict(ammo_dict)
    print("Ammunition:", new_ammo)

    # Test DutyPoint model
    duty_point = DutyPoint(location="Station A", description="Main duty point")
    duty_point_dict = duty_point.to_dict()
    new_duty_point = DutyPoint.from_dict(duty_point_dict)
    print("DutyPoint:", new_duty_point)

    # Test Record model
    record = Record(officer_id=1, weapon_id=1, duty_point_id=1, ammo_issued=10, time_booked="2023-10-01 08:00:00")
    record_dict = record.to_dict()
    new_record = Record.from_dict(record_dict)
    print("Record:", new_record)

    # Test Fingerprint model
    fingerprint = Fingerprint(template=b"fingerprint_template", user_id=1)
    fingerprint_dict = fingerprint.to_dict()
    new_fingerprint = Fingerprint.from_dict(fingerprint_dict)
    print("Fingerprint:", new_fingerprint)

if __name__ == "__main__":
    test_models()