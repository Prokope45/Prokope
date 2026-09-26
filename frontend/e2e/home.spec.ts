import { expect, test } from '@playwright/test'

/**
 * Baseline E2E coverage for the home page.
 *
 * The index API is backed by a singleton `Index` row that the `post_migrate`
 * signal creates, so this page has real content even against an empty database.
 */
test.describe('home page', () => {
  test('renders the hero IDE simulator', async ({ page }) => {
    await page.goto('/')

    await expect(page).toHaveTitle('Prokope.io')
    await expect(page.locator('#content')).toBeVisible()
    await expect(page.locator('.ide-container')).toBeVisible()
    await expect(page.locator('.ide-titlebar')).toContainText('index.py')
  })

  test('renders the about sections from the index API', async ({ page }) => {
    // The SPA only leaves its loading spinner once /api/index/ resolves, so a
    // successful response is what makes these headings appear at all.
    const indexResponse = page.waitForResponse(
      (response) => response.url().includes('/api/index/') && response.request().method() === 'GET'
    )

    await page.goto('/')
    expect((await indexResponse).status()).toBe(200)

    await expect(page.getByRole('heading', { name: 'Who, and what?' })).toBeVisible()
    await expect(page.getByRole('heading', { name: "What is 'Prokope'" })).toBeVisible()
  })

  test('navigates to the blog from the home page', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('#content')).toBeVisible()

    await page.locator('nav.navbar').getByRole('link', { name: /blog/i }).first().click()

    await expect(page).toHaveURL(/\/blog$/)
    await expect(page.getByRole('heading', { level: 1, name: 'Articles' })).toBeVisible()
  })
})
