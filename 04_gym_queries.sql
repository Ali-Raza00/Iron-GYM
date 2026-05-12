-- ============================================================
-- Project : IRON GYM MANAGEMENT SYSTEM (V3)
-- Script  : 04_gym_queries.sql
-- Purpose : Phase 2D - DML Queries (Select, Join, Aggregate, Subqueries)
-- ============================================================

-- 1. SELECT with WHERE (Min 5)
SELECT * FROM MEMBER WHERE gender = 'M';
SELECT * FROM STAFF WHERE role = 'Trainer' AND salary > 40000;
SELECT * FROM EQUIPMENT WHERE status = 'Working' ORDER BY purchase_date DESC;
SELECT * FROM PAYMENT WHERE amount >= 6000;
SELECT first_name, email FROM MEMBER WHERE join_date > SYSDATE - 30;

-- 2. AGGREGATE with GROUP BY (Min 3)
SELECT role, COUNT(*) as staff_count, AVG(salary) as avg_salary 
FROM STAFF GROUP BY role;

SELECT method, SUM(amount) as total_collected 
FROM PAYMENT GROUP BY method;

SELECT status, COUNT(*) as equip_count 
FROM EQUIPMENT GROUP BY status;

-- 3. SUBQUERIES (Min 3)
-- Nested Subquery: Members who have made payments above average
SELECT first_name, last_name FROM MEMBER 
WHERE member_id IN (SELECT member_id FROM PAYMENT WHERE amount > (SELECT AVG(amount) FROM PAYMENT));

-- Correlated Subquery: Staff with salary higher than the average for their role
SELECT s.first_name, s.role, s.salary FROM STAFF s 
WHERE s.salary > (SELECT AVG(salary) FROM STAFF WHERE role = s.role);

-- Scalar Subquery: List members with their total payment amount
SELECT m.first_name, (SELECT SUM(amount) FROM PAYMENT p WHERE p.member_id = m.member_id) as total_paid
FROM MEMBER m;

-- 4. JOIN QUERIES (Min 4)
-- INNER JOIN: Members with their payments
SELECT m.first_name, p.amount, p.payment_date 
FROM MEMBER m INNER JOIN PAYMENT p ON m.member_id = p.member_id;

-- LEFT OUTER JOIN: All classes and their trainers (even if no trainer)
SELECT c.class_name, s.first_name as trainer_name 
FROM GYM_CLASS c LEFT JOIN STAFF s ON c.trainer_id = s.staff_id;

-- Multi-table JOIN (3+ tables): Members, their attendance, and the class info (simulated logic)
SELECT m.first_name, a.att_date, a.status 
FROM MEMBER m 
JOIN ATTENDANCE a ON m.member_id = a.member_id 
ORDER BY a.att_date DESC;

-- Multi-table JOIN: Staff, Classes, and Members (conceptual list)
SELECT s.first_name as trainer, c.class_name, m.first_name as member
FROM STAFF s 
JOIN GYM_CLASS c ON s.staff_id = c.trainer_id
LEFT JOIN ATTENDANCE a ON c.class_id = 1 -- Example join
JOIN MEMBER m ON m.member_id = a.member_id
WHERE ROWNUM <= 5;

-- 5. UPDATE and DELETE (Min 2 each)
UPDATE STAFF SET salary = salary * 1.1 WHERE role = 'Admin';
UPDATE EQUIPMENT SET status = 'Maintenance' WHERE purchase_date < SYSDATE - 365;

DELETE FROM PAYMENT WHERE amount < 1000;
DELETE FROM AUDIT_LOG WHERE action_date < SYSDATE - 30;

-- 6. DCL Demonstration
-- Note: Requires appropriate privileges to run successfully
-- GRANT SELECT ON MEMBER TO PUBLIC;
-- REVOKE SELECT ON MEMBER FROM PUBLIC;

COMMIT;
