import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite"; // Import the plugin
// import basicSsl from "@vitejs/plugin-basic-ssl";


export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    // basicSsl(), // Add the plugin to the array
  ],

// server: {
//     proxy: {
//       // Все запросы, начинающиеся с /api, полетят на бэкенд
//       '/api': {
//         target: 'http://localhost:80', // АДРЕС ТВОЕГО БЭКЕНДА
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/api/, '/api') // оставляем /api в пути
//       }
//     }
//   }


});

//curl -X GET http://localhost/api/bookings/all \ -H 'Accept: application/json' \ -H 'Authorization: Bearer AzurPmBtfk6yU31ZOF9A'