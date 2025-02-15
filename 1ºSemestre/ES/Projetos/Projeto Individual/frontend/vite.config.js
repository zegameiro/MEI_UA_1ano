import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': process.env,
  },
  server: {
    watch: {
      usePolling: true
    },
    hmr: {
      overlay: true,
    },
    host: true,
    strictPort: true,
    port: 3000
  },
  build: {
    sourcemap: true,
  }
})
