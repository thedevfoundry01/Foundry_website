module.exports = {
  plugins: [
    require('postcss-import'),
    require('@tailwindcss/postcss'),  // Add this line
    require('autoprefixer'),
  ],
};
