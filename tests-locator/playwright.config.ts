import { defineConfig } from '@playwright/test';

// Baseline (locator-based) suite. The app dev server is started automatically.
// Run against a UI variant with: APP_VARIANT=v1 npx playwright test
export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  fullyParallel: true,
  reporter: [['list']],
  use: {
    baseURL: 'http://localhost:5173',
    viewport: { width: 1280, height: 800 },
  },
  webServer: {
    command: 'npm run dev',
    cwd: '../app',
    url: 'http://localhost:5173',
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
