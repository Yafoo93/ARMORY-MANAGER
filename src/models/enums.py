# import enum
from enum import Enum as PyEnum

# Booking Status


class BookingStatus(PyEnum):
    ISSUED = "ISSUED"  # Officer requested a weapon
    PENDING = "PENDING"  # Armorer approved the request
    RETURNED = "RETURNED"  # Weapon returned
    OVERDUE = "OVERDUE"  # Past expected return
    CANCELLED = "CANCELLED"  # Cancelled before issuance


#  Weapon Status


class WeaponStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ISSUED = "ISSUED"
    MISSING = "MISSING"
    DAMAGED = "DAMAGED"


# 🧬 Biometric Action Log


class BiometricAction(PyEnum):
    LOGIN_ARMORER = "LOGIN_ARMORER"
    ISSUE_ARMORER = "ISSUE_ARMORER"
    ISSUE_OFFICER = "ISSUE_OFFICER"
    RETURN_ARMORER = "RETURN_ARMORER"
    RETURN_OFFICER = "RETURN_OFFICER"
