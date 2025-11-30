import MySQLdb
import os

# 1. Load Credentials from Render Environment
# If these variables don't exist (like on your laptop), it falls back to the strings in the second argument
db_host = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
db_user = os.getenv("DB_USER", "4TgBvN87GCAUvSB.app_user")
db_pass = os.getenv("DB_PASSWORD", "StrongPass123!").strip()  # .strip() removes accidental spaces
db_name = os.getenv("DB_NAME", "eatery")

# 2. DEBUGGING: Print masked credentials to logs (Safe way to check)
print(f"DEBUG: Connecting to Host: {db_host}")
print(f"DEBUG: Connecting as User: '{db_user}'")
print(f"DEBUG: Password Length: {len(db_pass)}")


def get_db_connection():
    # SSL Configuration for Render (Linux) vs Local (Windows)
    ssl_config = {}
    if os.path.exists("/etc/ssl/certs/ca-certificates.crt"):
        ssl_config = {"ca": "/etc/ssl/certs/ca-certificates.crt"}
    else:
        ssl_config = None  # Fallback for local testing

    try:
        connection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_pass,
            db=db_name,
            port=4000,
            ssl=ssl_config
        )
        return connection
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return None


# Global connection
cnx = get_db_connection()


def get_total_order_price(order_id):
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0


def get_next_order_id():
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    if result is None or result[0] is None:
        return 1
    else:
        return result[0] + 1


def insert_order_item(food_item, quantity, order_id):
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    try:
        cursor = cnx.cursor()

        # FIX: Use cursor.execute() instead of cursor.callproc()
        # This sends a raw SQL command which works perfectly on TiDB
        cursor.execute("CALL insert_order_item(%s, %s, %s)", (food_item, quantity, order_id))

        cnx.commit()
        cursor.close()
        print(f"Item {food_item} inserted successfully!")
        return 1
    except Exception as e:
        print(f"Error inserting order item: {e}")
        cnx.rollback()
        return -1


def insert_order_tracking(order_id, status):
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    cursor = cnx.cursor()
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()


def get_order_status(order_id):
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    cursor = cnx.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return None