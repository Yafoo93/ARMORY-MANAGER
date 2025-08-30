
import enum
from enum import Enum

class BookingStatus(enum.Enum):
    REQUESTED = "REQUESTED"
    APPROVED  = "APPROVED"
    ISSUED    = "ISSUED"
    RETURNED  = "RETURNED"
    CANCELLED = "CANCELLED"
    REJECTED  = "REJECTED"
    OVERDUE   = "OVERDUE"
    

class WeaponStatus(enum.Enum):
    AVAILABLE   = "AVAILABLE"
    RESERVED    = "RESERVED"
    ISSUED      = "ISSUED"
    MAINTENANCE = "MAINTENANCE"

class BiometricAction(enum.Enum):
    LOGIN_ARMORER  = "LOGIN_ARMORER"
    ISSUE_ARMORER  = "ISSUE_ARMORER"
    ISSUE_OFFICER  = "ISSUE_OFFICER"
    RETURN_ARMORER = "RETURN_ARMORER"
    RETURN_OFFICER = "RETURN_OFFICER"
    
    
