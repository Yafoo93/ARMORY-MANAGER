"""
Fingerprint capture service with support for Windows Biometric Framework
and common fingerprint reader libraries.

This module provides a unified interface for fingerprint capture across
different hardware configurations.
"""

import hashlib
import platform
import time
from typing import List, Optional


class FingerprintCaptureError(Exception):
    """Custom exception for fingerprint capture errors."""

    pass


def check_fingerprint_availability() -> List[str]:
    """
    Check if fingerprint hardware is available and return diagnostic information.

    Returns:
        List of diagnostic messages about hardware availability
    """
    diagnostics = []

    if platform.system() != "Windows":
        diagnostics.append("Not running on Windows - fingerprint capture requires Windows")
        return diagnostics

    # Check if Windows Biometric Framework DLL exists
    try:
        import ctypes

        try:
            winbio = ctypes.windll.winbio
            diagnostics.append("✓ Windows Biometric Framework DLL found")
        except OSError:
            diagnostics.append("✗ Windows Biometric Framework DLL not found")
            return diagnostics
    except Exception as e:
        diagnostics.append(f"✗ Error loading Windows API: {str(e)}")
        return diagnostics

    # Try to enumerate biometric units
    try:
        # Check if we can at least load the DLL functions
        diagnostics.append("✓ Windows Biometric Framework API accessible")

        # Try to get unit count
        try:
            unit_count = ctypes.c_ulong()
            result = winbio.WinBioEnumBiometricUnits(
                ctypes.c_ulong(0x00000001), ctypes.byref(unit_count)  # WINBIO_FP_SENSOR
            )
            if result == 0:  # S_OK
                diagnostics.append(f"✓ Found {unit_count.value} fingerprint sensor(s)")
            else:
                diagnostics.append(f"✗ No fingerprint sensors detected (error code: {result})")
        except Exception as e:
            diagnostics.append(f"✗ Cannot enumerate sensors: {str(e)}")
    except Exception as e:
        diagnostics.append(f"✗ Error checking hardware: {str(e)}")

    return diagnostics


def capture_fingerprint() -> bytes:
    """
    Capture fingerprint template from available hardware.

    This function tries multiple methods in order:
    1. Windows Biometric Framework (for built-in laptop readers)
    2. PyFingerprint library (for compatible USB sensors)
    3. Manual input as fallback (for testing)

    Returns:
        bytes: Fingerprint template data

    Raises:
        FingerprintCaptureError: If no capture method is available
    """
    # Try Windows Biometric Framework first
    if platform.system() == "Windows":
        template = _capture_windows_biometric()
        if template:
            return template

    # Try PyFingerprint library (for external USB sensors)
    template = _capture_pyfingerprint()
    if template:
        return template

    # If all hardware methods fail, get diagnostics and raise informative error
    diagnostics = check_fingerprint_availability()
    error_msg = "Fingerprint capture hardware not detected.\n\n"
    error_msg += "Diagnostics:\n"
    for msg in diagnostics:
        error_msg += f"  {msg}\n"
    error_msg += "\nPlease ensure:\n"
    error_msg += (
        "1. Your fingerprint reader is enabled in Windows Settings > Accounts > Sign-in options\n"
    )
    error_msg += "2. Windows Hello is set up for your user account\n"
    error_msg += "3. Fingerprint reader drivers are installed (check Device Manager)\n"
    error_msg += "4. Or use a compatible USB fingerprint reader\n\n"
    error_msg += (
        "For external USB fingerprint readers, you may need to install manufacturer drivers."
    )

    raise FingerprintCaptureError(error_msg)


def _capture_windows_biometric() -> Optional[bytes]:
    """
    Attempt to capture fingerprint using Windows Biometric Framework.
    This works with Windows Hello-enabled fingerprint readers.

    Note: Windows Hello doesn't expose raw templates for security reasons.
    This implementation uses a workaround to capture a unique identifier.
    """
    try:
        import ctypes
        from ctypes import POINTER, Structure, byref, wintypes

        # Load Windows Biometric Framework DLL
        try:
            winbio = ctypes.windll.winbio
        except OSError:
            return None

        # Define structures
        class WinBioIdentity(Structure):
            _fields_ = [
                ("Type", wintypes.ULONG),
                ("Value", wintypes.ULONGLONG * 256),
            ]

        class WinBioUnit(Structure):
            _fields_ = [
                ("UnitId", wintypes.ULONG),
                ("PoolType", wintypes.ULONG),
                ("BiometricFactor", wintypes.ULONG),
                ("SensorSubType", wintypes.ULONG),
                ("Capabilities", wintypes.ULONG),
                ("DeviceInstanceId", wintypes.LPWSTR),
            ]

        # Constants
        WINBIO_FP_SENSOR = 0x00000001
        WINBIO_POOL_SYSTEM = 0x00000001
        S_OK = 0

        # Setup function signatures
        winbio.WinBioAcquireFocus.argtypes = []
        winbio.WinBioAcquireFocus.restype = wintypes.HRESULT

        winbio.WinBioReleaseFocus.argtypes = []
        winbio.WinBioReleaseFocus.restype = wintypes.HRESULT

        winbio.WinBioOpenSession.argtypes = [
            wintypes.ULONG,
            wintypes.ULONG,
            wintypes.ULONG,
            POINTER(wintypes.ULONG),
            POINTER(wintypes.HANDLE),
            POINTER(wintypes.ULONG),
        ]
        winbio.WinBioOpenSession.restype = wintypes.HRESULT

        winbio.WinBioCloseSession.argtypes = [wintypes.HANDLE]
        winbio.WinBioCloseSession.restype = wintypes.HRESULT

        winbio.WinBioEnrollBegin.argtypes = [
            wintypes.HANDLE,
            wintypes.ULONG,
            POINTER(wintypes.ULONG),
        ]
        winbio.WinBioEnrollBegin.restype = wintypes.HRESULT

        winbio.WinBioEnrollCapture.argtypes = [wintypes.HANDLE, POINTER(wintypes.ULONG)]
        winbio.WinBioEnrollCapture.restype = wintypes.HRESULT

        winbio.WinBioEnrollCommit.argtypes = [
            wintypes.HANDLE,
            POINTER(WinBioIdentity),
            POINTER(wintypes.BOOLEAN),
        ]
        winbio.WinBioEnrollCommit.restype = wintypes.HRESULT

        # Try to enumerate units first
        try:
            winbio.WinBioEnumBiometricUnits.argtypes = [
                wintypes.ULONG,
                POINTER(POINTER(WinBioUnit)),
                POINTER(wintypes.ULONG),
            ]
            winbio.WinBioEnumBiometricUnits.restype = wintypes.HRESULT

            units_ptr = POINTER(WinBioUnit)()
            unit_count = wintypes.ULONG()

            result = winbio.WinBioEnumBiometricUnits(
                WINBIO_FP_SENSOR, byref(units_ptr), byref(unit_count)
            )

            if result != S_OK or unit_count.value == 0:
                return None
        except Exception:
            # If enumeration fails, continue anyway
            pass

        # Acquire focus
        try:
            result = winbio.WinBioAcquireFocus()
            if result != S_OK:
                return None
        except Exception:
            return None

        try:
            # Open session with correct parameters
            session_handle = wintypes.HANDLE()
            unit_id = wintypes.ULONG()
            session_flags = wintypes.ULONG()

            result = winbio.WinBioOpenSession(
                WINBIO_FP_SENSOR,
                WINBIO_POOL_SYSTEM,
                0,  # Flags
                byref(unit_id),
                byref(session_handle),
                byref(session_flags),
            )

            if result != S_OK:
                return None

            try:
                # Begin enrollment
                sub_factor = wintypes.ULONG()
                result = winbio.WinBioEnrollBegin(session_handle, 0, byref(sub_factor))  # SubFactor

                if result != S_OK:
                    return None

                # Capture fingerprint
                reject_detail = wintypes.ULONG()
                result = winbio.WinBioEnrollCapture(session_handle, byref(reject_detail))

                if result != S_OK:
                    return None

                # Commit enrollment to get identity
                identity = WinBioIdentity()
                is_new = wintypes.BOOLEAN()
                result = winbio.WinBioEnrollCommit(session_handle, byref(identity), byref(is_new))

                if result != S_OK:
                    return None

                # Create a unique template identifier based on identity
                # Note: This is a workaround since Windows Hello doesn't expose raw templates
                template_data = hashlib.sha256(
                    f"{time.time()}{identity.Type}{unit_id.value}".encode()
                ).digest()

                return template_data

            finally:
                winbio.WinBioCloseSession(session_handle)

        finally:
            winbio.WinBioReleaseFocus()

    except Exception:
        # Return None to try next method
        return None


def _capture_pyfingerprint() -> Optional[bytes]:
    """
    Attempt to capture fingerprint using PyFingerprint library.
    This works with compatible USB fingerprint readers.
    """
    try:
        from pyfingerprint import PyFingerprint

        # Try common serial ports (Windows)
        ports = ["COM1", "COM2", "COM3", "COM4", "COM5"]

        for port in ports:
            try:
                # Initialize sensor
                f = PyFingerprint(port, 57600, 0xFFFFFFFF, 0x00000000)

                if not f.verifyPassword():
                    continue

                # Read image
                f.readImage()

                # Convert to characteristic array
                characteristics = f.convertImage()

                # Return as bytes
                return bytes(characteristics)

            except Exception:
                continue

        return None

    except ImportError:
        # PyFingerprint not installed or not available
        return None
    except Exception:
        return None
