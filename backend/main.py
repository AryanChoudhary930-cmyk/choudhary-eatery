from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# Enable CORS for the frontend (React) to access this backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store ongoing orders in memory (Session ID -> Order Dict)
inprogress_orders = {}


# --- HEALTH CHECK ENDPOINTS ---
@app.get("/health")
async def health_check():
    """Basic health check to verify the application is running"""
    return {"status": "healthy", "message": "Application is running"}


@app.get("/health/db")
async def database_health_check():
    """Check database connection status"""
    try:
        if db_helper.cnx is None:
            db_helper.cnx = db_helper.get_db_connection()
        
        if db_helper.cnx is None:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "message": "Database connection unavailable"}
            )
        
        # Try to ping the database
        db_helper.cnx.ping(True)
        return {"status": "healthy", "message": "Database connection is active"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": f"Database error: {str(e)}"}
        )



# --- API ENDPOINT: GET MENU ---
# --- API ENDPOINT: GET MENU ---
@app.get("/menu")
async def get_menu():
    """Get all menu items from food_items table for the Frontend Website"""
    try:
        # Check if database connection is available
        if db_helper.cnx is None:
            print("⚠️ Database connection unavailable, attempting to reconnect...")
            db_helper.cnx = db_helper.get_db_connection()
        
        if db_helper.cnx is None:
            print("❌ Database still unavailable, returning empty menu")
            return []
        
        # Use standard cursor to fetch data
        cursor = db_helper.cnx.cursor()
        query = "SELECT item_id, name, price FROM food_items"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        # Convert DB tuples to JSON-friendly list of dictionaries
        items = []
        for row in data:
            items.append({
                "id": row[0],
                "name": row[1],
                # Ensure price is sent as an integer (e.g., 120) not Decimal('120.00')
                "price": int(float(row[2]))
            })

        # Static assets mapping for images and categories
        menu_mapping = {
            'Pav Bhaji': {'description': 'Spicy mashed vegetables with buttered pav, a Mumbai street food favorite',
                          'image_url': '/assets/pav_bhaji.png', 'category': 'Lunch'},
            'Chole Bhature': {'description': 'Spiced chickpeas served with fluffy deep-fried bread',
                              'image_url': '/assets/chole_bhature.png', 'category': 'Breakfast'},
            'Pizza': {'description': 'Delicious Italian-style pizza with fresh toppings',
                      'image_url': '/assets/pizza.png', 'category': 'Lunch'},
            'Mango Lassi': {'description': 'Refreshing yogurt drink with sweet mango, perfect for hot days',
                            'image_url': '/assets/mango_lassi.png', 'category': 'Drinks'},
            'Masala Dosa': {
                'description': 'Crispy rice crepe filled with spiced potatoes, served with sambar and chutney',
                'image_url': '/assets/masala_dosa.png',
                'category': 'Breakfast'},
            'Vegetable Biryani': {'description': 'Fragrant basmati rice cooked with aromatic spices and vegetables',
                                  'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop&q=80',
                                  'category': 'Lunch'},
            'Vada Pav': {'description': 'Mumbai\'s favorite street food - spiced potato fritter in a bun',
                         'image_url': '/assets/vada_pav.png',
                         'category': 'Snacks'},
            'Rava Dosa': {'description': 'Crispy semolina crepe, light and golden, served with coconut chutney',
                          'image_url': '/assets/rava_dosa.png',
                          'category': 'Breakfast'},
            'Samosa': {'description': 'Crispy fried pastry filled with spiced potatoes and peas',
                       'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop&q=80',
                       'category': 'Snacks'},
        }

        # Merge DB data with static asset data
        enriched_items = []
        for item in items:
            item_name = item['name']
            if item_name in menu_mapping:
                item.update(menu_mapping[item_name])
            enriched_items.append(item)

        return enriched_items

    except Exception as e:
        print(f"❌ Error fetching menu: {e}")
        import traceback
        traceback.print_exc()
        return []


async def get_menu():
    """Get all menu items from food_items table for the Frontend Website"""
    try:
        # Use standard cursor to fetch data
        cursor = db_helper.cnx.cursor()
        query = "SELECT item_id, name, price FROM food_items"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        # Convert DB tuples to JSON-friendly list of dictionaries
        items = []
        for row in data:
            items.append({
                "id": row[0],
                "name": row[1],
                # Ensure price is sent as an integer (e.g., 120) not Decimal('120.00')
                "price": int(float(row[2]))
            })

        # Static assets mapping for images and categories
        menu_mapping = {
            'Pav Bhaji': {'description': 'Spicy mashed vegetables with buttered pav, a Mumbai street food favorite',
                          'image_url': '/assets/pav_bhaji.png', 'category': 'Lunch'},
            'Chole Bhature': {'description': 'Spiced chickpeas served with fluffy deep-fried bread',
                              'image_url': '/assets/chole_bhature.png', 'category': 'Breakfast'},
            'Pizza': {'description': 'Delicious Italian-style pizza with fresh toppings',
                      'image_url': '/assets/pizza.png', 'category': 'Lunch'},
            'Mango Lassi': {'description': 'Refreshing yogurt drink with sweet mango, perfect for hot days',
                            'image_url': '/assets/mango_lassi.png', 'category': 'Drinks'},
            'Masala Dosa': {
                'description': 'Crispy rice crepe filled with spiced potatoes, served with sambar and chutney',
                'image_url': '/assets/masala_dosa.png',
                'category': 'Breakfast'},
            'Vegetable Biryani': {'description': 'Fragrant basmati rice cooked with aromatic spices and vegetables',
                                  'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop&q=80',
                                  'category': 'Lunch'},
            'Vada Pav': {'description': 'Mumbai\'s favorite street food - spiced potato fritter in a bun',
                         'image_url': '/assets/vada_pav.png',
                         'category': 'Snacks'},
            'Rava Dosa': {'description': 'Crispy semolina crepe, light and golden, served with coconut chutney',
                          'image_url': '/assets/rava_dosa.png',
                          'category': 'Breakfast'},
            'Samosa': {'description': 'Crispy fried pastry filled with spiced potatoes and peas',
                       'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop&q=80',
                       'category': 'Snacks'},
        }

        # Merge DB data with static asset data
        enriched_items = []
        for item in items:
            item_name = item['name']
            if item_name in menu_mapping:
                item.update(menu_mapping[item_name])
            enriched_items.append(item)

        return enriched_items

    except Exception as e:
        print(f"Error fetching menu: {e}")
        return []


# --- API ENDPOINT: CREATE ORDER (For Frontend Cart) ---
@app.post("/order")
async def create_order(request: Request):
    """Create a new order from the React Frontend Cart"""
    try:
        payload = await request.json()
        items = payload.get("items", [])
        total_price = payload.get("total_price", 0)

        # 1. Get next Order ID
        order_id = db_helper.get_next_order_id()

        # 2. Insert items
        for item in items:
            quantity = item.get("quantity", 1)
            food_item = item.get("name")

            # Use the robust function which calculates price in Python
            rcode = db_helper.insert_order_item(food_item, quantity, order_id)

            if rcode == -1:
                return JSONResponse(status_code=500, content={"error": "Failed to insert order items"})

        # 3. Track the order
        db_helper.insert_order_tracking(order_id, "In progress")

        return JSONResponse(content={
            "order_id": order_id,
            "total_price": total_price,
            "status": "In progress"
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# --- API ENDPOINT: GET ORDER STATUS ---
@app.get("/order/{order_id}")
async def get_order_status_endpoint(order_id: int):
    """Check status of an order via ID"""
    try:
        status = db_helper.get_order_status(order_id)
        if status:
            return {"order_id": order_id, "status": status}
        else:
            return JSONResponse(status_code=404, content={"error": "Order not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# --- DIALOGFLOW WEBHOOK HANDLER ---
@app.post("/")
async def handle_request(request: Request):
    # 1. Retrieve the JSON data from Dialogflow
    payload = await request.json()

    # 2. Extract intent and parameters
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    # 3. Extract Session ID (Robust method)
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    # 4. Route to the correct handler function
    intent_handler_dict = {
        'order.add - context: Ongoing-Order': add_to_order,
        'order.remove - context: Ongoing-Order': remove_from_order,
        'order.complete - context: Ongoing-Order': complete_order,
        'track.order - context: Ongoing-Tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)


# --- HELPER FUNCTIONS FOR DIALOGFLOW ---

def save_to_db(order: dict):
    # Use helper to get ID
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items
    for food_item, quantity in order.items():
        # This function now handles price calculation internally
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    # Insert tracking status
    db_helper.insert_order_tracking(next_order_id, "In progress")

    return next_order_id


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. Please place a new order again"
        else:
            # Use the robust Python calculation function (No SQL Function call)
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id # {order_id}. " \
                               f"Your order total is {order_total} which you can pay at the time of delivery!"

        # Clear session
        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters.get("food-item", [])
    quantities = parameters.get("number", [])

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters: dict, session_id: str):
    # Robustly extract number (Dialogflow sends 'number', fallback to 'order_id')
    try:
        order_id = int(parameters['number'])
    except:
        order_id = int(parameters.get('order_id', 0))

    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })