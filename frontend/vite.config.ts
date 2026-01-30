import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite'; // Import the plugin
import basicSsl from '@vitejs/plugin-basic-ssl';
import path from 'path';
import browserslist from 'browserslist';
import { browserslistToTargets } from 'lightningcss';
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    basicSsl(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    transformer: 'lightningcss',
    lightningcss: {

      targets: browserslistToTargets(browserslist('>= 0.25%')),
    },
  },
  build: {
    cssMinify: 'lightningcss',
  },
  // server: {
  //   proxy: {
  //     '/api': {
  //       target: 'http://localhost:80/api', // your backend server
  //       changeOrigin: true,
  //       rewrite: (path) => path.replace(/^\/api/, ''),
  //     },
  //   },
  // },
});
