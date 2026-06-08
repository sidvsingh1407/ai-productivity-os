import { test, expect } from '@playwright/test';

test('Journey 4 - Contact Submission', async ({ page }) => {
    await page.goto('http://localhost:5173/contact');
    await page.waitForTimeout(1000);

    // Using the exact selectors that are likely in the form
    await page.fill('input[name="name"]', 'Test Lead');
    await page.fill('input[name="email"]', 'lead@example.com');
    await page.fill('textarea[name="message"]', 'This is a test lead');

    // Listen for requests to capture API failures
    page.on('response', response => {
      if (response.url().includes('/api') || response.url().includes('/contact')) {
        console.log('API Response:', response.url(), response.status());
      }
    });

    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'contact_submit_result.png' });
});
