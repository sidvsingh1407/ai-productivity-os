import { test, expect } from '@playwright/test';

test.describe('Authentication Flows', () => {

  test('Registration -> Verification Email Generated -> Verify Account -> Login', async ({ page, request }) => {
    await page.goto('http://localhost:5173/register');

    const randomEmail = `testuser_${Date.now()}@example.com`;
    await page.fill('input[id="fullName"]', 'Playwright Test User');
    await page.fill('input[id="companyName"]', 'Playwright Corp');
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/login/);
    await expect(page.locator('text=Registration successful. Please verify your email.')).toBeVisible();

    // Verify Account programmatically
    const verifyRes = await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);
    expect(verifyRes.status()).toBe(200);

    // Login
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/app\/dashboard/);
  });

  test('Logout and Protected Route Denied', async ({ page, request }) => {
    // 1. Register & Verify
    const randomEmail = `logout_${Date.now()}@example.com`;
    await request.post('http://localhost:8000/auth/register', {
        data: {
            email: randomEmail,
            password: 'StrongPassw0rd!',
            full_name: 'Logout Tester',
            org_name: 'Logout Org'
        }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // 2. Login
    await page.goto('http://localhost:5173/login');
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/);

    // 3. Logout
    await page.click('button:has-text("Log out")'); // Using the Sidebar button text
    await expect(page).toHaveURL(/.*\/login/);

    // 4. Protected Route Blocked
    await page.goto('http://localhost:5173/app/dashboard');
    await expect(page).toHaveURL(/.*\/login/);
  });

  test('Refresh Token and Refresh Rotation', async ({ page, request }) => {
    // 1. Register & Verify
    const randomEmail = `refresh_${Date.now()}@example.com`;
    await request.post('http://localhost:8000/auth/register', {
        data: {
            email: randomEmail,
            password: 'StrongPassw0rd!',
            full_name: 'Refresh Tester',
            org_name: 'Refresh Org'
        }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // 2. Login directly via API to get tokens
    const loginRes = await request.post('http://localhost:8000/auth/login', {
        data: {
            email: randomEmail,
            password: 'StrongPassw0rd!'
        }
    });
    expect(loginRes.status()).toBe(200);
    const body = await loginRes.json();
    const oldRefreshToken = body.refresh_token;

    // 3. Refresh Token
    const refreshRes = await request.post('http://localhost:8000/auth/refresh', {
        data: {
            refresh_token: oldRefreshToken
        }
    });
    expect(refreshRes.status()).toBe(200);
    const newBody = await refreshRes.json();
    const newRefreshToken = newBody.refresh_token;
    expect(newRefreshToken).not.toBe(oldRefreshToken); // Rotation occurred

    // 4. Old refresh fails (it was rotated out)
    const oldRefreshFailsRes = await request.post('http://localhost:8000/auth/refresh', {
        data: { refresh_token: oldRefreshToken }
    });
    expect(oldRefreshFailsRes.status()).toBe(401);

    // 5. Logout
    const logoutRes = await request.post('http://localhost:8000/auth/logout', {
        headers: { Authorization: `Bearer ${newBody.access_token}` },
        data: { refresh_token: newRefreshToken }
    });
    expect(logoutRes.status()).toBe(200);

    // 6. Refresh fails
    const finalRefreshRes = await request.post('http://localhost:8000/auth/refresh', {
        data: { refresh_token: newRefreshToken }
    });
    expect(finalRefreshRes.status()).toBe(401);
  });

  test('Password Reset', async ({ page, request }) => {
    const randomEmail = `reset_${Date.now()}@example.com`;
    await request.post('http://localhost:8000/auth/register', {
        data: { email: randomEmail, password: 'StrongPassw0rd!', full_name: 'Reset Tester', org_name: 'Reset Org' }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // Forgot Password
    await page.goto('http://localhost:5173/forgot-password');
    await page.fill('input[type="email"]', randomEmail);
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Check your email')).toBeVisible();

    // Get Reset Token from backend test API
    const tokenRes = await request.get(`http://localhost:8000/test-api/get-reset-token?email=${randomEmail}`);
    expect(tokenRes.status()).toBe(200);
    const { token } = await tokenRes.json();

    // Reset Password
    await page.goto(`http://localhost:5173/reset-password?token=${token}`);
    await page.fill('input[id="password"]', 'NewPassw0rd!');
    await page.fill('input[id="confirm-password"]', 'NewPassw0rd!');
    await page.click('button[type="submit"]');

    // Redirect to login eventually (after success banner)
    await expect(page.locator('text=Password reset successful')).toBeVisible();

    // Wait to be on login page, or just navigate
    await page.goto('http://localhost:5173/login');
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'NewPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/);
  });

  test('Delete Account', async ({ page, request }) => {
    const randomEmail = `delete_${Date.now()}@example.com`;
    await request.post('http://localhost:8000/auth/register', {
        data: { email: randomEmail, password: 'StrongPassw0rd!', full_name: 'Delete Tester', org_name: 'Delete Org' }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // Login to grab API token for direct API deletion for E2E speed, since delete UI might be deep
    await page.goto('http://localhost:5173/login');
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/);

    // Use page request to delete account (intercept the user session)
    // Here we find the Delete Account button in settings (assumes it exists based on requirements)
    await page.goto('http://localhost:5173/app/settings/danger-zone');
    // Wait for the button
    const deleteBtn = page.locator('button:has-text("Delete Account")').first();
    await deleteBtn.waitFor({ state: 'visible' });
    await deleteBtn.click();

    // Often there is a confirmation modal
    await page.fill('input[placeholder="DELETE"]', 'DELETE');
    await page.click('input[type="checkbox"]');
    // Specifically click the submit button in the modal which appears last or is active
    const modalBtn = page.locator('button:has-text("Delete Account")').last();
    await modalBtn.click();

    // Should be redirected to home first, and if protected it goes to login. Or home directly
    await expect(page).toHaveURL(/.*\//);

    // User Cannot Access Account
    const loginRes = await request.post('http://localhost:8000/auth/login', {
        data: { email: randomEmail, password: 'StrongPassw0rd!' }
    });
    expect(loginRes.status()).not.toBe(200);
  });
});
