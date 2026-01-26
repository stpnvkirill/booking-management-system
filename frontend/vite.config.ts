import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite"; // Import the plugin
import basicSsl from "@vitejs/plugin-basic-ssl";


export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    basicSsl(), // Add the plugin to the array
  ],
});
