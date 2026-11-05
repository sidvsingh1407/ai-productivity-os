import { test, expect } from '@playwright/test';

test.describe('Waitlist Flow', () => {
  test('User can join the waitlist from the home page', async ({ page }) => {
    // Mock the backend API response to succeed
    await page.route('**/api/waitlist', async route => {
      const json = { message: 'Success' };
      await route.fulfill({ json, status: 200 });
    });

    await page.goto('/');

    // Wait for hero element to confirm page loaded
    await expect(page.getByRole('heading', { name: 'Governance for the AI age.' })).toBeVisible();

    // Fill in the first waitlist form in the hero section
    const emailInput = page.getByLabel('Email address').first();
    await emailInput.fill('test.user@example.com');

    const productDropdown = page.getByLabel('What are you most interested in?').first();
    await productDropdown.selectOption('Roadmap');

    const submitBtn = page.getByRole('button', { name: 'Join waitlist' }).first();
    await submitBtn.click();

    // Verify success message
    await expect(page.getByText('Thank you. Check your email to confirm.').first()).toBeVisible();
  });
});
