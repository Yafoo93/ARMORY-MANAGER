import enum
from enum import Enum as PyEnum


# Booking Status

class BookingStatus(PyEnum):
    REQUESTED = "REQUESTED"   # Officer requested a weapon
    APPROVED = "APPROVED"     # Armorer approved the request
    ACTIVE = "ACTIVE"         # Weapon + ammo issued
    RETURNED = "RETURNED"     # Weapon returned
    OVERDUE = "OVERDUE"       # Past expected return
    DAMAGED = "DAMAGED"       # Weapon returned damaged
    CANCELLED = "CANCELLED"   # Cancelled before issuance
    REJECTED = "REJECTED"     # Request rejected



#  Weapon Status

class WeaponStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ISSUED = "ISSUED"
    MAINTENANCE = "MAINTENANCE"



# 🧬 Biometric Action Log

class BiometricAction(PyEnum):
    LOGIN_ARMORER = "LOGIN_ARMORER"
    ISSUE_ARMORER = "ISSUE_ARMORER"
    ISSUE_OFFICER = "ISSUE_OFFICER"
    RETURN_ARMORER = "RETURN_ARMORER"
    RETURN_OFFICER = "RETURN_OFFICER"
