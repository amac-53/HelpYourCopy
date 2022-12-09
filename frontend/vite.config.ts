import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  // Docker環境下でviteを使用するための設定
  server: {
    host: true,
    // 変更反映させるために
    watch: {
      usePolling: true
    }
  }
});
