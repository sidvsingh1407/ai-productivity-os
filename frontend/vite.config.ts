import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  if (mode === 'production' && !process.env.VITE_API_URL) {
    throw new Error("VITE_API_URL must be set in production");
  }

  return {
    plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
    },
  };
});
