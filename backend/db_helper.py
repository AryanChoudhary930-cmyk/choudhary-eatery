import MySQLdb
import os

# Get credentials
db_host = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
db_user = os.getenv("DB_USER", "4TgBvN87GCAUvSB.root")
db_pass = os.getenv("DB_PASSWORD", "8pRDXrkFUQvKpFTC").strip()
db_name = os.getenv("DB_NAME", "eatery")


def get_db_connection():
    # Define SSL settings based on the environment
    ssl_config = {}

    # Check if we are on Render (Linux) where this file exists
    if os.path.exists("/etc/ssl/certs/ca-certificates.crt"):
        ssl_config = {"ca": "/etc/ssl/certs/ca-certificates.crt"}
    else:
        # Fallback for local Windows (TiDB requires SSL, but might accept default system stores)
        # If this fails locally, we might need to download a CA cert,
        # but this logic prioritizes getting the DEPLOYMENT working.
        ssl_config = None

    try:
        connection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_pass,
            db=db_name,
            port=4000,
            ssl=ssl_config  # This forces SSL using the system certificate
        )
        return connection
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return None


# Global connection
cnx = get_db_connection()


def get_total_order_price(order_id):
    # Re-connect if connection was lost (Robustness fix)
    global cnx
    try:
        cnx.ping(True)
    except:
        cnx = get_db_connection()

    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    # MySQLdb returns tuples, so fetchone() returns (price,)
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
        # MySQLdb syntax for calling procedures
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