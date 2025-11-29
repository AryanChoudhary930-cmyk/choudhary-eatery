import { useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle, Home, Package } from 'lucide-react';

const Success = () => {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('orderId');

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-16">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-2xl w-full text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
          className="mb-6 flex justify-center"
        >
          <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center">
            <CheckCircle size={48} className="text-green-600" />
          </div>
        </motion.div>

        <h1 className="text-4xl md:text-5xl font-bold text-secondary mb-4">
          Order Placed Successfully!
        </h1>
        
        <p className="text-xl text-gray-600 mb-2">
          Thank you for your order!
        </p>

        {orderId && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-primary/10 border border-primary/20 rounded-lg p-6 mb-8"
          >
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Package size={24} className="text-primary" />
              <span className="text-lg font-semibold text-secondary">Order ID:</span>
            </div>
            <p className="text-2xl font-bold text-primary">{orderId}</p>
          </motion.div>
        )}

        <p className="text-gray-600 mb-8">
          We've received your order and will start preparing it right away. You'll receive a confirmation call shortly.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="inline-flex items-center justify-center space-x-2 bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-accent transition-colors"
          >
            <Home size={20} />
            <span>Back to Home</span>
          </Link>
          <Link
            to="/menu"
            className="inline-flex items-center justify-center space-x-2 bg-white text-primary border-2 border-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary/10 transition-colors"
          >
            <span>Order More</span>
          </Link>
        </div>
      </motion.div>
    </div>
  );
};

export default Success;

