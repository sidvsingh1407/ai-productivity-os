import { test, expect } from '@playwright/test';

test.describe('Legal Pages', () => {
  test('Footer navigation correctly links to legal pages', async ({ page }) => {
    await page.goto('/');

    const dpaLink = page.locator('footer a', { hasText: 'Data Processing Agreement' });
    await expect(dpaLink).toHaveAttribute('href', '/dpa');

    const subprocessorsLink = page.locator('footer a', { hasText: 'Subprocessors' });
    await expect(subprocessorsLink).toHaveAttribute('href', '/subprocessors');

    const termsLink = page.locator('footer a', { hasText: 'Terms of Service' });
    await expect(termsLink).toHaveAttribute('href', '/terms');
  });

  test('DPA page renders correctly and displays placeholder warning', async ({ page }) => {
    await page.goto('/dpa');

    // Ensure the page title and placeholder warning are present
    await expect(page.locator('h1', { hasText: 'Data Processing Agreement' })).toBeVisible();
    await expect(page.locator('h2', { hasText: 'Legal Review Required' })).toBeVisible();
    await expect(page.getByText('This page does not represent a finalized, effective legal agreement')).toBeVisible();
  });

  test('Subprocessors page renders correctly and lists all required providers', async ({ page }) => {
    await page.goto('/subprocessors');

    await expect(page.locator('h1', { hasText: 'Subprocessors' })).toBeVisible();

    const providers = ['Supabase', 'Render', 'Vercel', 'Resend', 'Google Gemini'];
    for (const provider of providers) {
      await expect(page.locator('td', { hasText: provider })).toBeVisible();
    }
  });
});
