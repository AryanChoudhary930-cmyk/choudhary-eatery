import { motion } from 'framer-motion';
import { Plus, Minus } from 'lucide-react';
import useCartStore from '../store/cartStore';

const FoodCard = ({ item }) => {
  const addItem = useCartStore((state) => state.addItem);
  const updateQuantity = useCartStore((state) => state.updateQuantity);
  const items = useCartStore((state) => state.items);
  
  const cartItem = items.find((i) => i.id === item.id);
  const quantity = cartItem?.quantity || 0;

  const handleAdd = () => {
    addItem(item);
  };

  const handleIncrement = () => {
    updateQuantity(item.id, quantity + 1);
  };

  const handleDecrement = () => {
    updateQuantity(item.id, quantity - 1);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -8 }}
      className="bg-white/95 backdrop-blur-subtle rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all"
    >
      {/* Image */}
      <div className="relative h-48 overflow-hidden bg-gray-200 group">
        {item.image_url ? (
          <motion.img
            src={item.image_url}
            alt={item.name}
            className="w-full h-full object-cover"
            initial={{ scale: 1 }}
            whileHover={{ scale: 1.1 }}
            transition={{ duration: 0.3 }}
            onError={(e) => {
              e.target.src = `https://via.placeholder.com/300x200?text=${encodeURIComponent(item.name)}`;
            }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/20 to-accent/20">
            <span className="text-4xl">🍽️</span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-xl font-bold text-secondary mb-2">{item.name}</h3>
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">{item.description}</p>
        
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-primary">₹{item.price}</span>
          
          {quantity === 0 ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleAdd}
              className="bg-primary text-white px-4 py-2 rounded-lg font-semibold hover:bg-accent transition-colors flex items-center space-x-2"
            >
              <Plus size={18} />
              <span>Add</span>
            </motion.button>
          ) : (
            <div className="flex items-center space-x-3 bg-primary/10 rounded-lg px-3 py-2">
              <button
                onClick={handleDecrement}
                className="text-primary hover:text-accent transition-colors"
              >
                <Minus size={18} />
              </button>
              <span className="font-bold text-secondary w-8 text-center">{quantity}</span>
              <button
                onClick={handleIncrement}
                className="text-primary hover:text-accent transition-colors"
              >
                <Plus size={18} />
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default FoodCard;

