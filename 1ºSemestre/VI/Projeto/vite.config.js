import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/VI_Project/',
  plugins: [react()],
  base: "/",
  build: {
    outDir: "dist",
  },
  server: {
    port: 3000
  }
})