import { defineConfig } from '@playwright/test';

// Baseline (locator-based) suite. The app dev server is started automatically.
// Run against a UI variant with: APP_VARIANT=v1 npx playwright test
// When the experiment harness sets HARNESS_JSON, also emit machine-readable results.
const reporter: Array<[string] | [string, unknown]> = [['list']];
if (process.env.HARNESS_JSON) reporter.push(['json', { outputFile: process.env.HARNESS_JSON }]);

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  fullyParallel: true,
  reporter,
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
