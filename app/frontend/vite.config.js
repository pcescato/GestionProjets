import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // ← important pour que Vite fonctionne dans Docker
    port: 5173,
  },
});
p; ;