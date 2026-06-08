import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await expect(page).toHaveTitle(/AI Productivity/);
});

test('journey 1 - AI Audit', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.click('text=AI Audit');
  // Just testing initial routing
  await expect(page).toHaveURL(/.*new-audit/);
});
