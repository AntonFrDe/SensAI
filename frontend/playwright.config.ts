import { defineConfig, devices } from '@playwright/test';

const apiPort = 8791;
const webPort = 5191;

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: { baseURL: `http://127.0.0.1:${webPort}`, trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      command: `../.venv/bin/python e2e/e2e_server.py ${apiPort}`,
      url: `http://127.0.0.1:${apiPort}/api/status`,
      reuseExistingServer: false,
    },
    {
      command: `npx vite --port ${webPort} --strictPort`,
      url: `http://127.0.0.1:${webPort}`,
      env: { SENSAI_API: `http://127.0.0.1:${apiPort}` },
      reuseExistingServer: false,
    },
  ],
});
