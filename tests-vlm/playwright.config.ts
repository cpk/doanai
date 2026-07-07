import { defineConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

// VLM-based suite (Midscene.js). Requires .env with MIDSCENE_MODEL_* variables.
// IMPORTANT for the experiment: never enable MIDSCENE_CACHE (it would distort
// flakiness measurements); keep workers=1 so API latency numbers are clean.
export default defineConfig({
  testDir: '.',
  timeout: 180_000,
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['@midscene/web/playwright-reporter', { type: 'merged' }]],
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
