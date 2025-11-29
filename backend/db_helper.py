import MySQLdb
import os

# 1. Load Credentials
db_host = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
db_user = os.getenv("DB_USER", "4TgBvN87GCAUvSB.root")
db_pass = os.getenv("DB_PASSWORD", "8pRDXrkFUQvKpFTC").strip()
db_name = os.getenv("DB_NAME", "eatery")

# 2. DEBUGGING: Print what credentials are being used to the logs
print(f"DEBUG: Connecting to Host: {db_host}")
print(f"DEBUG: Connecting as User: '{db_user}'")
print(f"DEBUG: Password: '{db_pass[:2]}...{db_pass[-2:]}' (Length: {len(db_pass)})")


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
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
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