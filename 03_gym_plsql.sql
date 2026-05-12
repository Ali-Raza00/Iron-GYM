-- ============================================================
-- Project : IRON GYM MANAGEMENT SYSTEM (V4 - SYNCED)
-- Script  : 03_gym_plsql.sql
-- Purpose : PL/SQL - Triggers, Procedures, Functions, and Packages
-- ============================================================

SET SERVEROUTPUT ON;

-- 1. TRIGGER: Auto-ID for Member
CREATE OR REPLACE TRIGGER TRG_MEMBER_BI
BEFORE INSERT ON MEMBER
FOR EACH ROW
BEGIN
    IF :NEW.MEMBERID IS NULL THEN
        SELECT SEQ_MEMBER_ID.NEXTVAL INTO :NEW.MEMBERID FROM DUAL;
    END IF;
END;
/

-- 2. TRIGGER: Audit Log for Payments
CREATE OR REPLACE TRIGGER TRG_PAYMENT_AI
AFTER INSERT ON PAYMENT
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOG (LOGID, ACTION_NAME, ACTION_DATE, USER_NAME)
    VALUES (SEQ_LOG_ID.NEXTVAL, 'NEW PAYMENT: ' || :NEW.AMOUNT, SYSDATE, USER);
END;
/

-- 3. PACKAGE: Gym Management
CREATE OR REPLACE PACKAGE pkg_gym_mgmt AS
    PROCEDURE add_attendance(p_mid NUMBER, p_status VARCHAR2);
    FUNCTION get_total_revenue RETURN NUMBER;
END pkg_gym_mgmt;
/

CREATE OR REPLACE PACKAGE BODY pkg_gym_mgmt AS
    PROCEDURE add_attendance(p_mid NUMBER, p_status VARCHAR2) IS
    BEGIN
        INSERT INTO ATTENDANCE (MEMBERID, ATTENDANCE_DATE, STATUS)
        VALUES (p_mid, TRUNC(SYSDATE), p_status);
    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            UPDATE ATTENDANCE SET STATUS = p_status 
            WHERE MEMBERID = p_mid AND ATTENDANCE_DATE = TRUNC(SYSDATE);
    END;

    FUNCTION get_total_revenue RETURN NUMBER IS
        v_total NUMBER;
    BEGIN
        SELECT SUM(AMOUNT) INTO v_total FROM PAYMENT;
        RETURN NVL(v_total, 0);
    END;
END pkg_gym_mgmt;
/

COMMIT;
