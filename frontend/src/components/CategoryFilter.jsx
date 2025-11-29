import { motion } from 'framer-motion';

const categories = ['All', 'Breakfast', 'Lunch', 'Snacks', 'Drinks'];

const CategoryFilter = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="flex flex-wrap gap-3 justify-center mb-8">
      {categories.map((category) => (
        <motion.button
          key={category}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onCategoryChange(category)}
          className={`px-6 py-2 rounded-full font-semibold transition-all backdrop-blur-subtle ${
            selectedCategory === category
              ? 'bg-primary text-white shadow-md'
              : 'bg-white/90 text-secondary hover:bg-primary/10 border border-gray-200'
          }`}
        >
          {category}
        </motion.button>
      ))}
    </div>
  );
};

export default CategoryFilter;

