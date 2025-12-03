import MySQLdb
import os
import sys

# 1. Load Credentials from Environment Variables
db_host = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
db_user = os.getenv("DB_USER", "4TgBvN87GCAUvSB.app_user")
db_pass = os.getenv("DB_PASSWORD", "StrongPass123!").strip()
db_name = os.getenv("DB_NAME", "eatery")
db_port = int(os.getenv("DB_PORT", "4000"))

# 2. DEBUGGING
print(f"🔍 DEBUG: Connecting to Host: {db_host}")
print(f"🔍 DEBUG: Connecting as User: '{db_user}'")
print(f"🔍 DEBUG: Password Length: {len(db_pass)}")
print(f"🔍 DEBUG: Database Name: {db_name}")
print(f"🔍 DEBUG: Port: {db_port}")


def get_db_connection():
    """Create and return a database connection with proper SSL handling"""
    ssl_config = None
    
    # Check for SSL certificate in common locations
    ssl_cert_paths = [
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/etc/ssl/ca-bundle.pem",
        "/etc/ssl/cert.pem"
    ]
    
    for cert_path in ssl_cert_paths:
        if os.path.exists(cert_path):
            ssl_config = {"ca": cert_path}
            print(f"✅ SSL Certificate found at: {cert_path}")
            break
    
    if ssl_config is None:
        print("⚠️ No SSL certificate found, attempting connection without SSL verification")

    try:
        print("🔌 Attempting database connection...")
        connection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_pass,
            db=db_name,
            port=db_port,
            ssl=ssl_config,
            connect_timeout=10
        )
        print("✅ Database connection successful!")
        return connection
    except MySQLdb.Error as e:
        print(f"❌ MySQL Error during connection: {e}")
        print(f"   Error Code: {e.args[0] if e.args else 'N/A'}")
        return None
    except Exception as e:
        print(f"❌ Unexpected connection error: {type(e).__name__}: {e}")
        return None


# Global connection - Don't crash on startup if DB is unavailable
cnx = None
try:
    cnx = get_db_connection()
    if cnx is None:
        print("⚠️ WARNING: Initial database connection failed. Will retry on first request.")
except Exception as e:
    print(f"⚠️ WARNING: Could not establish initial DB connection: {e}")
    print("   Application will start, but database operations may fail until connection is established.")


def get_total_order_price(order_id):
    global cnx
    try:
        if cnx is None:
            cnx = get_db_connection()
        if cnx:
            cnx.ping(True)
    except:
        cnx = get_db_connection()
    
    if cnx is None:
        print("❌ Database connection unavailable")
        return 0.0

    cursor = cnx.cursor()

    # FIX: Use a raw SQL SELECT SUM() instead of calling a stored function
    # This works universally on all databases
    query = "SELECT SUM(total_price) FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))

    result = cursor.fetchone()
    cursor.close()

    # Handle case where result is None (e.g. order deleted)
    if result and result[0]:
        return float(result[0])  # Convert Decimal to Float
    return 0.0


def get_next_order_id():
    global cnx
    try:
        if cnx is None:
            cnx = get_db_connection()
        if cnx:
            cnx.ping(True)
    except:
        cnx = get_db_connection()
    
    if cnx is None:
        print("❌ Database connection unavailable")
        return 1

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
        if cnx is None:
            cnx = get_db_connection()
        if cnx:
            cnx.ping(True)
    except:
        cnx = get_db_connection()
    
    if cnx is None:
        print("❌ Database connection unavailable")
        return -1

    try:
        cursor = cnx.cursor()

        # 1. Get the Item ID and Price
        cursor.execute("SELECT item_id, price FROM food_items WHERE name = %s", (food_item,))
        result = cursor.fetchone()

        if not result:
            print(f"❌ Item '{food_item}' not found in database!")
            return -1

        item_id = result[0]
        price = result[1]

        # 2. FIX: Convert 'price' to float before multiplying
        total_price = float(price) * float(quantity)

        # 3. Insert the Order
        insert_query = "INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (order_id, item_id, quantity, total_price))

        cnx.commit()
        cursor.close()
        print(f"✅ Item {food_item} inserted successfully!")
        return 1

    except Exception as e:
        print(f"❌ Error inserting order item: {e}")
        cnx.rollback()
        return -1


def insert_order_tracking(order_id, status):
    global cnx
    try:
        if cnx is None:
            cnx = get_db_connection()
        if cnx:
            cnx.ping(True)
    except:
        cnx = get_db_connection()
    
    if cnx is None:
        print("❌ Database connection unavailable")
        return

    cursor = cnx.cursor()
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()


def get_order_status(order_id):
    global cnx
    try:
        if cnx is None:
            cnx = get_db_connection()
        if cnx:
            cnx.ping(True)
    except:
        cnx = get_db_connection()
    
    if cnx is None:
        print("❌ Database connection unavailable")
        return None

    cursor = cnx.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return None