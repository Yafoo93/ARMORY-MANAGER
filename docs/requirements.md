## ARMORY MANAGEMENT SYSTEM PROJECT REQUIREMENT
# 1System Overview
Name: Armory Management System

Description: A standalone desktop application to manage weapon inventory, bookings, and returns at the Ghana Police Service armoury which will not require internet to function.

Purpose: To streamline the management of weapons, ammunition, and personnel records while ensuring security and accountability.

# 2 Core Features
       2.1 Weapon Inventory Management
        Purpose: Track and manage all weapons in the armoury.
        Description:
        -Add, update, and delete weapons from the inventory.
        -Track weapon details (e.g., serial number, type, condition, location).
        -Categorize weapons by type (e.g., firearms, non-lethal weapons).
        -Monitor weapon availability and status (e.g., in-stock, booked, under maintenance).

       2.2 Ammunition Management
       Purpose: Track ammunition stock and usage.
       Description:
        -Record the number of ammunition in stock.
        -Automatically update ammunition count when weapons are booked or returned.
        -Generate alerts when ammunition stock is low.

       2.3 Booking and Returning System
        Purpose: Manage weapon bookings and returns by officers.
        Description:
        -Officers can request weapons for duty using fingerprint authentication.
        -Armoury Manager can approve or reject requests.
        -Track weapon return status and condition.
        -Generate booking and return receipts.

       2.4 Personnel and Duty Point Management
        Purpose: Manage records of officers and duty points.
        Description:
        -Store details of officers (e.g., service number, name, telephone number).
        -Record duty points within the station.
        -Link weapon bookings to specific duty points.

       2.5 Reporting and Analytics
        Purpose: Provide insights into weapon usage and inventory.
        Description:
        -Generate periodic reports on:
         >Number of weapons in stock.
         >Number of weapons booked and returned.
         >Number of weapons booked but not yet returned.
         >Number of ammunition in stock.
        -Armoury officers on duty during a specific period.

       2.6 Notifications and Alerts
        Purpose: Notify users about important updates.
        Description:
        -Notify officers and managers about overdue returns or pending approvals.
        -Send reminders for weapon maintenance schedules.
        -Alert when a booked weapon exceeds its expected return time.

       2.7 Audit Trail
        Purpose: Maintain accountability for all actions.
        Description:
        -Log all actions (e.g., weapon issued, returned, updated).
        -Track user activity (e.g., login attempts, report generation).
        -Export reports in PDF or Excel format.

# 3. User Management
       3.1 User Roles
        Admin: Full access to the system (e.g., manage users, view reports).
        Armoury Manager: Manage weapon inventory, approve bookings, and generate reports.
        Officer: Request weapons, view booking status, and return weapons.
       3.2 Authentication and Authorization
        Purpose: Secure access to the system.
        Description:
        -Fingerprint authentication for officers booking weapons.
        -Shift-based login system for Armoury Managers (sign in/out at the start and end of shifts).
        -Role-based access control (RBAC) to restrict access based on user roles.
       3.3 Activity History Tracking
        Purpose: Track user activity for accountability.
        Description:
        -Maintain a log of all user actions (e.g., weapon bookings, report generation).
        -Allow admins to view and export activity logs.

# 4. Security and Compliance
       4.1 Data Encryption
        Purpose: Protect sensitive information.
        Description:
        -Encrypt sensitive data (e.g., user credentials, weapon details) using AES-256 encryption.
        -Store encrypted data locally on the system.

       4.2 Audit Trails
        Purpose: Ensure accountability and compliance.
        Description:
        -Log all system interactions (e.g., weapon bookings, report generation).
        -Allow admins to view and export audit logs.

       4.3 Backup System
       Purpose: Safeguard data integrity.
       Description:
        -Automatically back up data daily to a local external drive or network-attached storage (NAS).
        -Ensure backups are encrypted for security.

# 5. Technical Details
       5.1 Development Stack
        Frontend:
        Framework: PyQt or Tkinter (for desktop GUI development in Python).
        UI Components: Custom-designed for a professional look.

        Backend:
        Language: Python

        Database: SQLite (lightweight, file-based database for local storage).

        Encryption: cryptography library for AES-256 encryption.

       5.2 Fingerprint Authentication
        Purpose: Secure weapon bookings.
        Description:
        -Integrate a fingerprint scanner (e.g., Futronic FS80 or SecuGen Hamster Pro).
        -Use a Python library like PyFingerprint or fprint for fingerprint recognition.
        -Store fingerprint templates securely using encryption.

       5.3 Shift-Based Login System
        Purpose: Track Armoury Manager shifts.
        Description:
        -Armoury Managers must sign in at the start of their shift and sign out at the end.
        -Log shift timings for accountability.

       5.4 Local Storage
        Purpose: Ensure data is stored locally for security.
        Description:
        -Use SQLite for database storage.
        -Store encrypted backups on a local external drive or NAS.

# 6. Functional Requirements
       6.1 Weapon Booking
        Inputs:
        -Officer details (e.g., service number, name, telephone number).
        -Weapon details (e.g., serial number, type).
        -Number of ammunition issued.
        -Duty details (e.g., duty point, expected return time).
        -Fingerprint scan for authentication.
       Processing:
        -Validate booking request.
        -Update weapon and ammunition status in the database.
       Outputs:
        -Booking receipt.
        -Confirmation message (e.g., "Weapon booked successfully").

        6.2 Weapon Returning
       Inputs:
        -Officer details (e.g., service number).
        -Weapon details (e.g., serial number).
        -Fingerprint scan for authentication.
       Processing:
        -Validate return request.
        -Update weapon and ammunition status in the database.
       Outputs:
        -Return receipt.
        -Confirmation message (e.g., "Weapon returned successfully").

       6.3 Reporting
       Inputs:
        -Report type (e.g., inventory, bookings).
        -Date range (e.g., daily, weekly).
       Processing:
        -Query database for relevant data.
        -Generate report in desired format (e.g., PDF, Excel).
       Outputs:
        -Generated report.
        -Download link for the report.

# 7. Additional Features
       7.1 Weapon Maintenance Tracking
       Purpose: Track weapon maintenance schedules.
       Description:
        -Schedule and log maintenance activities for weapons.
        -Notify Armoury Managers when maintenance is due.

       7.2 Multi-User Support
       Purpose: Allow multiple users to access the system simultaneously.
       Description:
        -Support concurrent access by Armoury Managers and Officers.
        -Ensure data consistency with database locking mechanisms.

       7.3 Data Import/Export
       Purpose: Facilitate data migration and sharing.
       Description:
        -Import weapon inventory from Excel or CSV files.
        -Export reports and logs to Excel or PDF format.

# 8. Hardware Requirements
       8.1 Fingerprint Scanner
        -Model: Futronic FS80 or SecuGen Hamster Pro.
        -Integration: Use Python libraries like PyFingerprint or fprint.

       8.2 Local Storage
        -Primary Storage: Internal hard drive (minimum 500GB).
        -Backup Storage: External hard drive or NAS (minimum 1TB).
