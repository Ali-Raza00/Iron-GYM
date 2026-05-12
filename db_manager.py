import oracledb
import os

# ==========================================
# 1. ORACLE 11g FIX: ENABLE THICK MODE
# ==========================================
# We must point to your Oracle Client libraries for 11g support
ORACLE_CLIENT_PATH = r"C:\Users\M KHIZER AQEEL\Downloads\instantclient-basiclite-windows.x64-19.30.0.0.0dbru\instantclient_19_30"
try:
    if os.path.exists(ORACLE_CLIENT_PATH):
        oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
        print("✓ Oracle Thick Mode Enabled (11g Support)")
    else:
        print("! Warning: Oracle Client path not found. Connection might fail for 11g.")
except Exception as e:
    print(f"! Notice: {e}")

# ==========================================
# 2. DATABASE CONNECTION SETTINGS
# ==========================================
DB_USER = "system"
DB_PASSWORD = "khizer"
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SID = "xe"

DSN_STR = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={DB_HOST})(PORT={DB_PORT}))(CONNECT_DATA=(SID={DB_SID})))"

class DBManager:
    @staticmethod
    def get_connection():
        """
        Attempts to connect to the Oracle Database.
        """
        try:
            conn = oracledb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=DSN_STR
            )
            return conn
        except Exception as e:
            print(f"Connection Error: {e}")
            return None

    @staticmethod
    def execute_query(query, params=None, commit=False):
        """
        Helper to run queries and return results or status.
        """
        conn = DBManager.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if commit:
            conn.commit()
            return True
        
        # Return results if any, otherwise return None
        try:
            return cursor.fetchall()
        except:
            return None
        finally:
            conn.close()

if __name__ == "__main__":
    # Test the connection when run directly
    print("Testing Oracle Connection...")
    connection = DBManager.get_connection()
    if connection:
        print("Success! Connected to Oracle Database.")
        connection.close()
    else:
        print("Failed! Please check if Oracle Service is running.")
