// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}', // Ensures TSX files are covered
    './node_modules/flyonui/dist/js/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('flyonui'), require('flyonui/plugin')],
};
