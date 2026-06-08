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

test('App Console Errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', error => {
      errors.push(error.message);
      console.log('Page Error:', error.message);
    });

    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('Console Error:', msg.text());
        errors.push(msg.text());
      }
    });

    await page.goto('http://localhost:5173/app/audits/new');
    await page.waitForTimeout(2000);

    console.log('Total errors on /app/audits/new:', errors.length);
});
