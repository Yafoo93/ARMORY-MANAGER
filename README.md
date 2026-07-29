# Armory Management System

A secure offline desktop application developed to modernize weapon and ammunition management within the Ghana Police Service.

---

## Overview

The **Armory Management System** is a stand-alone desktop application designed to replace the traditional manual weapon register used in police armories. The system provides a secure, efficient, and accountable way of managing weapons, ammunition, armory personnel, and daily weapon issuance and returns.

Unlike paper-based record keeping, the system digitizes armory operations, improves accountability, reduces human error, and provides real-time visibility into weapon inventory and officer transactions.

The application is designed to operate completely **offline**, ensuring that sensitive police armory information is never exposed to the Internet.

---

# Academic Background

This project was developed as the final-year Bachelor of Technology (B.Tech.) project at **Tamale Technical University**.

**Project Information**

* Institution: Tamale Technical University
* Programme: Bachelor of Technology in Information Technology
* Project Grade: A
* Dissertation Length: 98 Pages
* Team Size: Two
* Role: Team Leader & Lead Software Developer
* Dissertation Author: Kassim Mutawakil
* Supervisor: Dr. Zakaria Abukari

---

# Problem Statement

Many police armories still rely on handwritten registers to record the issuance and return of firearms and ammunition.

This manual process presents several operational challenges, including:

* Slow weapon booking and return processes
* Difficulty tracking weapon availability
* Poor accountability
* Delayed report generation
* Inaccurate ammunition stock management
* Difficulty identifying overdue weapons
* Limited audit capability
* High risk of human error

The Armory Management System was developed to address these challenges by providing a secure digital platform for managing armory operations.

---

# Objectives

The system aims to:

* Digitize armory operations
* Improve accountability in weapon management
* Maintain accurate weapon and ammunition inventories
* Record all weapon bookings and returns
* Generate management reports
* Monitor overdue weapons
* Improve security through controlled user access
* Reduce paperwork and manual errors

---

# Key Features

## Weapon Inventory Management

* Register weapons
* Update weapon information
* Track weapon availability
* Search weapons
* Categorize weapons by type

---

## Ammunition Management

* Maintain ammunition inventory
* Record ammunition issued
* Record ammunition returned
* Automatically update stock balances

---

## Officer Management

Maintain records of:

* Police officers
* Service numbers
* Telephone numbers
* Assigned stations
* Assigned weapons

---

## Weapon Booking & Returns

Record:

* Officer details
* Weapon issued
* Weapon type
* Quantity of ammunition issued
* Duty point
* Booking time
* Expected return time
* Actual return time
* Armory officer responsible

---

## Duty Point Management

Maintain a database of duty points including:

* Patrol duties
* Escort duties
* Guard duties
* Operational deployments

---

## User Management

* Secure login
* Role-based permissions
* Password authentication
* User activity tracking

---

## Audit Trail

Maintain logs of:

* Logins
* Weapon bookings
* Weapon returns
* Inventory updates
* User activities

---

## Reporting

Generate reports including:

* Current weapon inventory
* Weapons issued
* Weapons returned
* Outstanding weapons
* Ammunition stock
* Daily transactions
* Monthly reports
* Officer activity reports

---

## Alerts

Automatically notify users when:

* A weapon has exceeded its expected return time
* Ammunition stock is low
* Inventory inconsistencies are detected

---

# Security Design

Security is one of the primary design considerations of this project.

The system incorporates:

* Offline deployment
* Role-Based Access Control (RBAC)
* User authentication
* Audit logging
* Secure local database
* Controlled access to administrative functions

Because the application is intended for law enforcement environments, it is designed to operate without Internet connectivity, significantly reducing external attack surfaces.

---

# System Architecture

The application follows a modular desktop architecture consisting of:

* Presentation Layer (Graphical User Interface)
* Business Logic Layer
* Database Layer
* Authentication Module
* Reporting Module
* Audit Module

This modular design improves maintainability, scalability, and security.

---

# Technology Stack

### Programming Language

* Python

### GUI

* CustomTkinter

### Database

* SQLite

### ORM

* SQLAlchemy

### Database Migration

* Alembic

### Version Control

* Git
* GitHub

---

# User Roles

### System Administrator

* Manage users
* Configure the system
* View all reports

### Armory Officer

* Book weapons
* Receive returned weapons
* Manage inventory
* Generate reports

---

# Database Design

The system manages information through relational tables including:

* Users
* Officers
* Weapons
* Ammunition
* Bookings
* Returns
* Duty Points
* Audit Logs

---

# Testing

The system was tested using realistic operational workflows based on procedures used at the Tamale Regional Police Armory.

Testing covered:

* User authentication
* Weapon booking
* Weapon returns
* Inventory updates
* Ammunition calculations
* Report generation
* Audit logging

---

# Current Limitations

Current limitations include:

* Desktop-only deployment
* Single-station implementation
* Offline operation only
* Fingerprint authentication not yet implemented
* Limited interoperability with other police information systems

---

# Future Enhancements

Future versions may include:

* Fingerprint authentication
* Smart card authentication
* Barcode or QR code weapon identification
* Automated email or SMS notifications
* Multi-station synchronization
* Digital signature support
* Dashboard analytics
* Integration with the Ghana Police Service information systems
* Advanced inventory forecasting
* Cloud synchronization for approved environments

---

# Screenshots

*(Add screenshots of the Dashboard, Login Page, Weapon Management, Booking Interface, Reports, and User Management pages here.)*

---

# Research Contribution

This project demonstrates how secure software engineering can be applied to improve accountability, inventory management, and operational efficiency within law enforcement agencies.

The experience gained during this project also laid the foundation for subsequent research into Artificial Intelligence-assisted decision-support systems for criminal investigations, including the development of **CIDman AI**.

---

# License

This project is released under the MIT License.

---

# Author

**Kassim Mutawakil**

Cybercrime Investigator | AI Researcher | Software Engineer

GitHub: https://github.com/Yafoo93

LinkedIn: https://linkedin.com/in/mutawakil-kassim-159a7178
