# Choudhary Eatery - Online Food Ordering System

A modern, full-stack food ordering web application with an integrated AI chatbot for seamless customer interaction.

## Features

### 🍽️ Frontend Features
- **Modern UI/UX**: Clean, responsive design with smooth animations using Framer Motion
- **Orange Theme**: Vibrant orange color scheme with elegant typography
- **Menu System**: Interactive menu with categories (Breakfast, Lunch, Snacks, Drinks)
- **Shopping Cart**: Real-time cart management with order tracking
- **Checkout Process**: Streamlined checkout with order confirmation
- **AI Chatbot**: Integrated Dialogflow Messenger for customer support

### 🤖 Backend Features
- **Flask API**: RESTful API for menu and order management
- **Database Integration**: MySQL database for persistent data storage
- **Order Processing**: Handle new orders and track order status
- **Dialog flow Integration**: Natural language processing for chatbot interactions

## Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS with custom orange theme
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **State Management**: Zustand
- **Routing**: React Router DOM
- **Fonts**: Inter & Playfair Display (Google Fonts)

### Backend
- **Runtime**: Python 3.x
- **Framework**: Flask
- **Database**: MySQL
- **Chatbot**: Google Dialogflow

## Project Structure

```
Food ChatBot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── data/           # Menu data
│   │   ├── store/          # Zustand store
│   │   └── lib/            # Utilities
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── main.py                 # Flask backend server
├── dbhelper.py            # Database helper functions
├── generic_helper.py      # Utility functions
└── README.md              # This file
```

## Installation

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- MySQL Server
- Dialogflow account (for chatbot)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Install Python dependencies:
```bash
pip install flask flask-cors mysql-connector-python
```

2. Configure your MySQL database:
   - Create a database for the application
   - Update database credentials in `dbhelper.py`

3. Run the Flask server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

## Configuration

### Tailwind Theme Colors
The application uses a custom orange theme:
- **Primary**: `#EA580C` (Orange-600)
- **Accent**: `#F97316` (Orange-500)
- **Background**: `#FFF7ED` (Orange-50)
- **Secondary**: `#1E293B` (Dark Slate)

### Dialogflow Setup
1. Create a Dialogflow agent
2. Update the agent ID in `frontend/src/components/Chatbot.jsx`
3. Configure intents for order tracking and menu queries

## Usage

1. **Browse Menu**: Navigate to the home page to view featured items
2. **Add to Cart**: Click on menu items to add them to your cart
3. **Checkout**: Review your cart and proceed to checkout
4. **Track Orders**: Use the chatbot to track your order status
5. **Customer Support**: Ask the chatbot for help with menu items or orders

## API Endpoints

### Menu
- `GET /menu` - Get all menu items
- `GET /menu/:category` - Get items by category

### Orders
- `POST /orders` - Create a new order
- `GET /orders/:id` - Get order status
- `POST /track-order` - Track order via chatbot

## Development

### Build for Production

Frontend:
```bash
cd frontend
npm run build
```

The build files will be in `frontend/dist/`

### Linting
```bash
npm run lint
```

## Features in Detail

### Menu Management
- Dynamic menu loading from database
- Category-based filtering
- Real-time price updates
- High-quality food imagery

### Order System
- Session-based cart management
- Order validation
- Status tracking (In Progress, Completed)
- Order history

### Chatbot Integration
- Natural language understanding
- Order tracking via conversation
- Menu recommendations
- Customer support automation

## Credits

- **Design**: Modern restaurant UI/UX patterns
- **Images**: Unsplash (food photography)
- **Fonts**: Google Fonts (Inter, Playfair Display)
- **Icons**: Lucide React

## License

This project is created for educational and demonstration purposes.

## Contact

For questions or support, please contact via the integrated chatbot on the website.

---

**Built with ❤️ for Choudhary Eatery**
