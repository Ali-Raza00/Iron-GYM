import oracledb

# Database Connection Settings
DB_HOST = "localhost" 
DB_PORT = "1521"
DB_SID = "xe" 
DB_USER = "system" 
DB_PASSWORD = "khizer" 

# Create DSN using the Full Descriptor (Most reliable for 11g)
DSN = f"""
(DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = {DB_HOST})(PORT = {DB_PORT}))
    (CONNECT_DATA =
        (SID = {DB_SID})
    )
)"""
