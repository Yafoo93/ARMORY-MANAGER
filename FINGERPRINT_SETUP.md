# Fingerprint Scanner Setup Guide

## Overview

This application supports fingerprint capture and verification for Windows laptops with built-in fingerprint readers. The system uses Windows Biometric Framework (WBF) to interface with compatible fingerprint readers.

## Prerequisites

1. **Windows 10 or Windows 11** with a built-in fingerprint reader
2. **Windows Hello** configured for your user account
3. **Fingerprint reader drivers** installed (usually automatic with Windows)

## Setup Steps

### 1. Configure Windows Hello

1. Open **Windows Settings** (Win + I)
2. Go to **Accounts** → **Sign-in options**
3. Under **Windows Hello Fingerprint**, click **Set up**
4. Follow the on-screen instructions to enroll your fingerprint
5. Complete the setup process

### 2. Verify Fingerprint Reader

1. In **Windows Settings** → **Accounts** → **Sign-in options**
2. Ensure **Windows Hello Fingerprint** shows "Ready" or "Set up"
3. Test by locking your computer (Win + L) and unlocking with fingerprint

### 3. Using the Application

#### Enrolling a Fingerprint

1. Open **Officer Management**
2. Select an officer from the list
3. Click **"Enroll Fingerprint"**
4. In the enrollment dialog, click **"Scan Fingerprint"**
5. Place your finger on the fingerprint reader when prompted
6. Wait for the capture to complete
7. You'll see a success message when enrollment is complete

#### Verifying Fingerprint

1. When booking or returning a weapon, the system will prompt for fingerprint verification
2. Click **"Scan & Verify"** in the verification dialog
3. Place your finger on the fingerprint reader
4. The system will verify against enrolled fingerprints

## Troubleshooting

### "Fingerprint capture hardware not detected"

**Possible causes:**
- Windows Hello is not set up
- Fingerprint reader drivers are not installed
- Fingerprint reader is disabled in Windows Settings

**Solutions:**
1. Set up Windows Hello Fingerprint (see Setup Steps above)
2. Check **Device Manager** → **Biometric devices** for your fingerprint reader
3. Update drivers if needed
4. Restart your computer after setup

### "Fingerprint capture failed"

**Possible causes:**
- Finger not placed correctly on reader
- Fingerprint reader needs cleaning
- Windows Hello needs recalibration

**Solutions:**
1. Ensure your finger is clean and dry
2. Place finger flat on the reader
3. Don't move finger during capture
4. Try recalibrating Windows Hello in Windows Settings

### Fingerprint Reader Not Working

If your fingerprint reader doesn't appear in Windows Settings:

1. **Check Device Manager:**
   - Press Win + X → Device Manager
   - Look under **Biometric devices**
   - If device shows with error, update drivers

2. **Check Manufacturer Support:**
   - Some fingerprint readers require manufacturer-specific drivers
   - Check your laptop manufacturer's website for drivers
   - Common manufacturers: Synaptics, Goodix, Validity, etc.

3. **Alternative: External USB Fingerprint Reader**
   - If built-in reader doesn't work, you can use compatible USB fingerprint readers
   - Supported readers: ZFM-series sensors (via PyFingerprint library)
   - Connect USB reader and install manufacturer drivers

## Technical Notes

### How It Works

1. The application uses **Windows Biometric Framework (WBF)** to access the fingerprint reader
2. When you enroll a fingerprint, the system captures a template and stores it in the database
3. During verification, the system captures a new template and compares it with stored templates

### Limitations

- **Windows Hello Integration:** Windows Hello is designed for system authentication and doesn't expose raw templates. The application uses WBF to access the sensor directly.
- **Template Storage:** Fingerprint templates are stored as binary data in the database. For security, templates are hashed and compared.
- **Hardware Compatibility:** Not all fingerprint readers are fully compatible with WBF. Some may require manufacturer SDKs.

### Security Considerations

- Fingerprint templates are stored securely in the database
- Templates are hashed before comparison
- Never share or expose fingerprint templates
- Consider encrypting the database for additional security

## Support

If you continue to experience issues:

1. Check Windows Event Viewer for biometric-related errors
2. Verify your fingerprint reader model and manufacturer
3. Contact your system administrator or IT support
4. Check the application logs for detailed error messages

## Alternative Solutions

If Windows Biometric Framework doesn't work with your hardware:

1. **Use Manufacturer SDK:** Some fingerprint readers (Synaptics, Goodix, etc.) provide their own SDKs
2. **External USB Reader:** Use a USB fingerprint reader with known Python support
3. **Manual Entry:** For testing, you can temporarily disable fingerprint verification

---

**Note:** This implementation uses Windows Biometric Framework for maximum compatibility. Some advanced features may require manufacturer-specific SDKs.
