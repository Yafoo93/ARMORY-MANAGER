from src.database import Base
from src.models.weapon import Weapon
from src.models.user import User
from src.models.record import Record
from src.models.ammunition import Ammunition
from src.models.duty_point import DutyPoint
from src.models.fingerprint import Fingerprint
from src.database import init_db
from .booking import Booking 

init_db()
