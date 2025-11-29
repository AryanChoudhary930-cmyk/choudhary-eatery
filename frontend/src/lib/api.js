import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 3000, // 3 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Menu API
export const getMenuItems = async () => {
  try {
    const response = await api.get('/menu');
    return response.data;
  } catch (error) {
    console.error('Error fetching menu items:', error);
    throw error;
  }
};

// Order API
export const createOrder = async (orderData) => {
  try {
    const response = await api.post('/order', orderData);
    return response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    throw error;
  }
};

// Get Order Status
export const getOrderStatus = async (orderId) => {
  try {
    const response = await api.get(`/order/${orderId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching order status:', error);
    throw error;
  }
};

