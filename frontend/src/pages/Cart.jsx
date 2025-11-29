import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus, Minus, Trash2, ShoppingBag, ArrowRight } from 'lucide-react';
import useCartStore from '../store/cartStore';

const Cart = () => {
  const items = useCartStore((state) => state.items);
  const updateQuantity = useCartStore((state) => state.updateQuantity);
  const removeItem = useCartStore((state) => state.removeItem);
  const getTotalPrice = useCartStore((state) => state.getTotalPrice);
  const getTotalItems = useCartStore((state) => state.getTotalItems);

  const totalPrice = getTotalPrice();
  const totalItems = getTotalItems();

  if (items.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <ShoppingBag size={64} className="mx-auto text-gray-300 mb-4" />
          <h2 className="text-3xl font-bold text-secondary mb-4">Your cart is empty</h2>
          <p className="text-gray-600 mb-8">Add some delicious items to get started!</p>
          <Link
            to="/menu"
            className="inline-flex items-center space-x-2 bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-accent transition-colors"
          >
            <span>Browse Menu</span>
            <ArrowRight size={20} />
          </Link>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-secondary mb-8">Shopping Cart</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {items.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white/95 backdrop-blur-subtle rounded-lg shadow-md p-4 flex items-center gap-4"
              >
                {/* Image */}
                <div className="w-20 h-20 rounded-lg overflow-hidden bg-gray-200 flex-shrink-0">
                  {item.image_url ? (
                    <img
                      src={item.image_url}
                      alt={item.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="text-2xl">🍽️</span>
                    </div>
                  )}
                </div>

                {/* Item Info */}
                <div className="flex-grow">
                  <h3 className="font-bold text-secondary mb-1">{item.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">₹{item.price} each</p>
                  
                  {/* Quantity Controls */}
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      className="p-1 text-primary hover:text-accent transition-colors"
                    >
                      <Minus size={18} />
                    </button>
                    <span className="font-semibold text-secondary w-8 text-center">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="p-1 text-primary hover:text-accent transition-colors"
                    >
                      <Plus size={18} />
                    </button>
                  </div>
                </div>

                {/* Price and Remove */}
                <div className="text-right">
                  <p className="font-bold text-primary text-lg mb-2">
                    ₹{item.price * item.quantity}
                  </p>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </motion.div>
            ))}
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
                <div className="flex justify-between text-gray-600">
                  <span>Items ({totalItems})</span>
                  <span>₹{totalPrice}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Delivery</span>
                  <span>Free</span>
                </div>
                <div className="border-t pt-3 flex justify-between text-xl font-bold text-secondary">
                  <span>Total</span>
                  <span className="text-primary">₹{totalPrice}</span>
                </div>
              </div>

              <Link
                to="/checkout"
                className="block w-full bg-primary text-white text-center py-3 rounded-lg font-semibold hover:bg-accent transition-colors"
              >
                Proceed to Checkout
              </Link>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;

