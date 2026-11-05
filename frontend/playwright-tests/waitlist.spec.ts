import { test, expect } from '@playwright/test';

test.describe('Waitlist Flow', () => {
  test('User can join the waitlist via quick form', async ({ page }) => {
    await page.route('**/api/waitlist', async route => {
      const json = { message: 'Success' };
      await route.fulfill({ json, status: 200 });
    });

    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Governance for the AI age.' })).toBeVisible();

    const emailInput = page.getByLabel('Email address').first();
    await emailInput.fill('test.user@example.com');

    const submitBtn = page.getByRole('button', { name: 'Join waitlist' }).first();
    await submitBtn.click();

    await expect(page.getByText('Thank you. Check your email to confirm.').first()).toBeVisible();
  });

  test('User can switch to extended form and join', async ({ page }) => {
    await page.route('**/api/waitlist', async route => {
      const json = { message: 'Success' };
      await route.fulfill({ json, status: 200 });
    });

    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Governance for the AI age.' })).toBeVisible();

    const initialEmailInput = page.getByLabel('Email address').first();
    await initialEmailInput.fill('test.extended@example.com');

    const switchBtn = page.getByRole('button', { name: /Choose products/ }).first();
    await switchBtn.click();

    // In extended mode, the email should be preserved
    const extendedEmailInput = page.getByLabel('Email address').first();
    await expect(extendedEmailInput).toHaveValue('test.extended@example.com');

    // Select a product
    const roadmapCard = page.getByRole('button', { name: /Roadmap/ }).first();
    await roadmapCard.click();

    const submitBtn = page.getByRole('button', { name: 'Join waitlist' }).first();
    await submitBtn.click();

    await expect(page.getByText('Thank you. Check your email to confirm.').first()).toBeVisible();
  });
});
