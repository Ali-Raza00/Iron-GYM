# Iron-GYM
# Gym Management System
# Gym Management System

## Project Info
- Course: CL2005 Database Systems Lab
- Domain: Gym Management System
- Database: Oracle
- GUI: Python Tkinter

## Prerequisites
- Oracle Database XE installed and running
- Python 3.8 or above
- Required packages:
  `pip install cx_Oracle matplotlib`

## Setup Instructions (Step by Step)

### Step 1: Database Setup
Open Oracle SQL Developer and run these scripts IN ORDER:
1. Run `setup_database.sql` (cleans and prepares DB)
2. Run `03_DDL.sql` (creates all tables)
3. Run `04_DML_Inserts.sql` (populates data)
4. Run `05_Queries.sql` (runs query demonstrations)
5. Run `06_PLSQL.sql` (creates procedures, triggers, package)

### Step 2: Configure Connection
Open `config.py` and set:
- `DB_USER` = your Oracle username
- `DB_PASSWORD` = your Oracle password
- `DB_SERVICE` = XE (or ORCL depending on your installation)

### Step 3: Run the Application
```bash
python run_project.py
```

### Step 4: Login Credentials
| Role   | Username | Password   |
|--------|----------|------------|
| Admin  | admin    | admin123   |
| Viewer | viewer   | viewer123  |

## File Structure
```
gym_management/
├── setup_database.sql
├── 03_DDL.sql
├── 04_DML_Inserts.sql
├── 05_Queries.sql
├── 06_PLSQL.sql
├── config.py
├── db_connection.py
├── run_project.py
├── login.py
├── main_menu.py
├── members.py
├── subscriptions.py
├── payments.py
├── dashboard.py
├── reports.py
└── README.md
```

## Features
- Role-based login (Admin / Viewer)
- Member CRUD with search
- Subscription management
- Payment tracking
- Live analytics dashboard
- Exportable reports (CSV)
- PL/SQL automation (triggers, procedures, package)

## Database Schema
15 Tables: Staff, Trainer, Admin, Member, MembershipPlan,
Subscription, Payment, Attendance, WorkoutPlan, Exercise,
PlanExercise, Equipment, GymClass, ClassEnrollment, DietPlan

## Application Flow
Login Screen → Main Menu → [Members | Subscriptions | Payments | Dashboard | Reports]

