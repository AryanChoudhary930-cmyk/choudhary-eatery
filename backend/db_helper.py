import mysql.connector
import os

db_host = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
db_user = os.getenv("DB_USER", "4TgBvN87GCAUvSB.root")
db_pass = os.getenv("DB_PASSWORD", "8pRDXrkFUQvKpFTC").strip()
db_name = os.getenv("DB_NAME", "eatery")

print("------------------------------------------------")
print(f"DEBUG: Connecting to DB Host: {db_host}")
print(f"DEBUG: Connecting as User: {db_user}")
print(f"DEBUG: Password Length: {len(db_pass)} characters")
print("------------------------------------------------")

try:
    cnx = mysql.connector.connect(
        host=db_host,
        port=4000,
        user=db_user,
        password=db_pass,
        database=db_name,

        ssl_verify_cert=False,
        use_pure=True
    )
except mysql.connector.Error as err:
    print(f"❌ DATABASE CONNECTION ERROR: {err}")
    # We do not raise the error here to prevent immediate crash,
    # but subsequent functions will fail if cnx is not defined.

def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def get_next_order_id():
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
    try:
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()
        print(f"Item {food_item} inserted successfully!")
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()

def get_order_status(order_id):
    cursor = cnx.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return None