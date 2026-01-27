import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite'; // Import the plugin
import basicSsl from '@vitejs/plugin-basic-ssl';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    basicSsl(), // Add the plugin to the array
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // @ теперь ссылается на папку src
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:88/', // your backend server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
