import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem('auth-storage', JSON.stringify({
      state: {
        token: 'fake-jwt-token',
        user: {
          id: 'test-user-id',
          email: 'test@example.com',
          name: 'Test User',
          role: 'admin',
          org_id: 'test-org-123'
        },
        isAuthenticated: true,
        organization: {
            id: 'test-org-123',
            name: 'Test Org'
        }
      },
      version: 0
    }));
  });
});

test.describe('Launch Readiness Audit', () => {

  test('Journey 1 - AI Audit', async ({ page }) => {
    // Navigate directly to the app
    await page.goto('http://localhost:5173/app/audits/new');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'audit_flow_new.png' });

    // Check if form elements exist
    const formsExist = await page.locator('form').count();
    console.log('Forms on New Audit:', formsExist);
  });

  test('Journey 4 - Contact & Leads', async ({ page }) => {
    await page.goto('http://localhost:5173/contact');
    await page.waitForTimeout(2000);

    const formsExist = await page.locator('form').count();
    console.log('Forms on Contact Page:', formsExist);
    await page.screenshot({ path: 'contact_page.png' });
  });

  test('Analytics Audit', async ({ page }) => {
    await page.goto('http://localhost:5173');
    // Just looking for signs of vercel or google analytics in the DOM or scripts
    const html = await page.content();
    console.log('Has Vercel Analytics:', html.includes('@vercel/analytics') || html.includes('va.vercel-scripts.com'));
    console.log('Has Google Analytics:', html.includes('googletagmanager.com') || html.includes('gtag'));
  });

});
