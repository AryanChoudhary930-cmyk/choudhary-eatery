import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CreditCard } from 'lucide-react';
import { Link } from 'react-router-dom';
import useCartStore from '../store/cartStore';
import { createOrder } from '../lib/api';

const Checkout = () => {
  const navigate = useNavigate();
  const items = useCartStore((state) => state.items);
  const getTotalPrice = useCartStore((state) => state.getTotalPrice);
  const clearCart = useCartStore((state) => state.clearCart);

  const [formData, setFormData] = useState({
    customer_name: '',
    customer_phone: '',
    customer_address: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const totalPrice = getTotalPrice();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!formData.customer_name.trim()) {
      setError('Please enter your name');
      return;
    }
    if (!formData.customer_phone.trim()) {
      setError('Please enter your phone number');
      return;
    }
    if (!formData.customer_address.trim()) {
      setError('Please enter your address');
      return;
    }

    setLoading(true);

    try {
      const orderData = {
        items: items.map((item) => ({
          id: item.id,
          quantity: item.quantity,
        })),
        total_price: totalPrice,
        customer_name: formData.customer_name,
        customer_phone: formData.customer_phone,
        customer_address: formData.customer_address,
      };

      const response = await createOrder(orderData);
      clearCart();
      navigate(`/success?orderId=${response.id || response.order_id || 'N/A'}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to place order. Please try again.');
      console.error('Order error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="text-gray-600 text-xl mb-4">Your cart is empty</p>
          <Link
            to="/menu"
            className="text-primary hover:text-accent transition-colors"
          >
            Go to Menu
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <Link
          to="/cart"
          className="inline-flex items-center space-x-2 text-secondary hover:text-primary mb-6 transition-colors"
        >
          <ArrowLeft size={20} />
          <span>Back to Cart</span>
        </Link>

        <h1 className="text-4xl font-bold text-secondary mb-8">Checkout</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Checkout Form */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/95 backdrop-blur-subtle rounded-lg shadow-md p-6"
            >
              <h2 className="text-2xl font-bold text-secondary mb-6 flex items-center space-x-2">
                <CreditCard size={24} />
                <span>Delivery Information</span>
              </h2>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-secondary mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    name="customer_name"
                    value={formData.customer_name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="Enter your full name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-secondary mb-2">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    name="customer_phone"
                    value={formData.customer_phone}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="Enter your phone number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-secondary mb-2">
                    Delivery Address *
                  </label>
                  <textarea
                    name="customer_address"
                    value={formData.customer_address}
                    onChange={handleChange}
                    required
                    rows={4}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                    placeholder="Enter your complete delivery address"
                  />
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-accent transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Placing Order...' : 'Place Order'}
                </button>
              </form>
            </motion.div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white/95 backdrop-blur-subtle rounded-lg shadow-md p-6 sticky top-24"
            >
              <h2 className="text-2xl font-bold text-secondary mb-4">Order Summary</h2>
              
              <div className="space-y-3 mb-6">
                {items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.name} x {item.quantity}
                    </span>
                    <span className="font-semibold">₹{item.price * item.quantity}</span>
                  </div>
                ))}
                <div className="border-t pt-3 flex justify-between text-xl font-bold text-secondary">
                  <span>Total</span>
                  <span className="text-primary">₹{totalPrice}</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;

