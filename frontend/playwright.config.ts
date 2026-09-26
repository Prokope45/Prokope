import { defineConfig, devices } from '@playwright/test'

const FRONTEND_PORT = Number(process.env.E2E_FRONTEND_PORT ?? 5173)
const BACKEND_PORT = Number(process.env.E2E_BACKEND_PORT ?? 8000)

const FRONTEND_URL = `http://127.0.0.1:${FRONTEND_PORT}`
const BACKEND_URL = `http://127.0.0.1:${BACKEND_PORT}`

/**
 * E2E configuration.
 *
 * The suite drives the real SPA through the Vite dev server, which proxies
 * `/api`, `/admin`, `/static` and `/media` to a locally running Django
 * backend. In CI both processes are started by this config so the test run is
 * fully self-contained and needs no deployed environment.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  timeout: 30_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: FRONTEND_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      // Vite dev server, proxying API calls through to the backend below.
      command: `npm run dev -- --host 127.0.0.1 --port ${FRONTEND_PORT} --strictPort`,
      url: FRONTEND_URL,
      env: {
        // Make the dev-server proxy target explicit rather than relying on the
        // http://localhost:8000 default, so it cannot drift from BACKEND_PORT.
        VITE_PROXY_TARGET: BACKEND_URL,
      },
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
    {
      // Django, served on the loopback interface. Migrations are expected to
      // have already been applied (CI runs `manage.py migrate` as its own
      // command so that a failure surfaces with a clear error).
      command: `uv run python manage.py runserver 127.0.0.1:${BACKEND_PORT} --noreload`,
      cwd: '../backend',
      env: {
        VITE_PROXY_TARGET: BACKEND_URL,
      },
      // The admin login page is a cheap, dependency-free 200 readiness probe.
      url: `${BACKEND_URL}/admin/login/`,
      reuseExistingServer: !process.env.CI,
      timeout: 180_000,
    },
  ],
})
