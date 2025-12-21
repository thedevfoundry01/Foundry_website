import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from 'tailwindcss'; // Correct package
import autoprefixer from 'autoprefixer';

export default defineConfig({
  root: './app/static',
  build: {
    outDir: './dist',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: resolve(__dirname, 'app/static/src/main.js'),
    },
  },
  css: {
    postcss: {
      plugins: [tailwindcss, autoprefixer], // Use the correct plugin
    },
  },
});
