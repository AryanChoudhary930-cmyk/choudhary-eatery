/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#EA580C', // Orange-600
        secondary: '#1E293B', // Dark slate
        background: '#FFF7ED', // Orange-50
        accent: '#F97316', // Orange-500
        success: '#10B981', // Emerald green
        warning: '#F59E0B', // Amber
        purple: '#8B5CF6', // Purple
        pink: '#EC4899', // Pink
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

