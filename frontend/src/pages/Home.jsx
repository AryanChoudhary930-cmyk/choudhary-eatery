import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, UtensilsCrossed, Clock, Star } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Banner */}
      <section className="relative py-20 px-4 overflow-hidden">
        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1513104890138-7c749659a591?w=1920&q=80)',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-primary/40 via-accent/30 to-secondary/50" />
        </div>

        {/* Content without blur backdrop */}
        <div className="relative max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center p-8 md:p-12"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white" style={{
                textShadow: '2px 2px 4px rgba(0,0,0,0.5), 0 0 10px rgba(0,0,0,0.3)',
                letterSpacing: '0.5px'
              }}>
                Welcome to{' '}
              </span>
              <span className="text-white font-extrabold block mt-2" style={{
                fontFamily: '"Playfair Display", serif',
                letterSpacing: '0.5px',
                textTransform: 'uppercase',
                fontSize: 'clamp(2.5rem, 8vw, 5rem)',
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
              }}>
                Choudhary Eatery
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-white/95 mb-8 max-w-2xl mx-auto drop-shadow-md">
              Experience authentic Indian flavors with a modern twist. Fresh ingredients, traditional recipes, and exceptional taste.
            </p>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                to="/menu"
                className="inline-flex items-center space-x-2 bg-primary text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-accent transition-all shadow-lg"
              >
                <span>Explore Menu</span>
                <ArrowRight size={20} />
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-secondary mb-12">
            Why Choose Us?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <UtensilsCrossed size={48} />,
                title: 'Authentic Recipes',
                description: 'Traditional recipes passed down through generations, prepared with love and care.',
              },
              {
                icon: <Clock size={48} />,
                title: 'Fast Delivery',
                description: 'Quick and reliable delivery service to bring delicious food to your doorstep.',
              },
              {
                icon: <Star size={48} />,
                title: 'Quality Ingredients',
                description: 'We use only the freshest and finest ingredients in every dish we prepare.',
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                className="text-center p-6 rounded-lg bg-background/80 backdrop-blur-subtle hover:shadow-lg hover:bg-background/90 transition-all"
              >
                <div className="text-primary mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-secondary mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-16 px-4 bg-primary overflow-hidden">
        <div className="relative max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Order?
            </h2>
            <p className="text-xl text-white/90 mb-8">
              Browse our delicious menu and place your order now!
            </p>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                to="/menu"
                className="inline-flex items-center space-x-2 bg-white text-primary px-8 py-4 rounded-lg text-lg font-semibold hover:bg-background transition-colors shadow-lg"
              >
                <span>View Menu</span>
                <ArrowRight size={20} />
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;
