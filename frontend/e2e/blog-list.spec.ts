import { expect, test } from '@playwright/test'

/**
 * Baseline E2E coverage for the blog list route.
 *
 * This exercises the full request path a browser takes in CI: the Vite dev
 * server serves the SPA, then proxies /api/* through to Django.
 */
test.describe('blog list', () => {
  test('renders the articles page shell', async ({ page }) => {
    await page.goto('/blog')

    // Rendered only once the posts request settles, so its presence proves
    // the list finished loading rather than still sitting on a spinner.
    await expect(page.getByRole('heading', { level: 1, name: 'Articles' })).toBeVisible()
    await expect(page.locator('#sort-select')).toBeVisible()
  })

  test('fetches posts through the dev-server proxy', async ({ page }) => {
    const postsResponse = page.waitForResponse(
      (response) => response.url().includes('/api/posts/') && response.request().method() === 'GET'
    )

    await page.goto('/blog')

    const response = await postsResponse
    expect(response.status()).toBe(200)
    expect(response.headers()['content-type']).toContain('application/json')
  })

  test('shows the empty state when there are no articles', async ({ page }) => {
    // CI runs against a freshly migrated database, which has no posts.
    await page.goto('/blog')
    await expect(page.getByText('No articles found.')).toBeVisible()
  })

  test('keeps filter state in the URL', async ({ page }) => {
    await page.goto('/blog')
    await expect(page.getByRole('heading', { level: 1, name: 'Articles' })).toBeVisible()

    await page.goto('/blog?page=1&order=asc')
    await expect(page).toHaveURL(/order=asc/)
    await expect(page.getByRole('heading', { level: 1, name: 'Articles' })).toBeVisible()
  })
})
