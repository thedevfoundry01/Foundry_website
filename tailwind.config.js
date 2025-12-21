/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/templates/**/*.html',  // Jinja2 templates
    './app/static/src/**/*.js',   // JavaScript files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
