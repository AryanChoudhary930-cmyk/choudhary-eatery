import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-secondary text-white mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About Section */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-primary">Choudhary Eatery</h3>
            <p className="text-gray-300 mb-4">
              Serving authentic Indian flavors with a modern twist. Experience the best of traditional cuisine.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-primary transition-colors">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-primary transition-colors">
                <Instagram size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-primary transition-colors">
                <Twitter size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-primary">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-300 hover:text-primary transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/menu" className="text-gray-300 hover:text-primary transition-colors">
                  Menu
                </Link>
              </li>
              <li>
                <Link to="/cart" className="text-gray-300 hover:text-primary transition-colors">
                  Cart
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-primary">Contact Us</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-center space-x-2">
                <Phone size={18} />
                <span>+91 98765 43210</span>
              </li>
              <li className="flex items-center space-x-2">
                <Mail size={18} />
                <span>info@choudharyeatery.com</span>
              </li>
              <li className="flex items-start space-x-2">
                <MapPin size={18} className="mt-1" />
                <span>123 Food Street, Mumbai, Maharashtra 400001</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Choudhary Eatery. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

