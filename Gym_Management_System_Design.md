# Iron Gym - Management System V2
**Architecture & Database Design**

## 1. Overview
A professional-grade desktop application built with Python (CustomTkinter) and Oracle 11g. The system focuses on high performance, data integrity, and a premium user experience.

## 2. Database Schema (Normalized)
- **Staff**: Manages employees and trainers.
- **Member**: Stores client information with auto-increment IDs (1001+).
- **MembershipPlan**: Flexible pricing and duration settings.

## 3. Technical Stack
- **Frontend**: CustomTkinter (Modern Python GUI).
- **Backend**: Oracle 11g XE.
- **Driver**: `python-oracledb` (Thick Mode).
- **Automation**: PL/SQL Triggers and Sequences for auto-increment.

## 4. Connection Protocol
The system uses **Oracle Thick Mode** to bridge the gap between modern Python and older Oracle 11g instances, ensuring 100% compatibility and stability.
