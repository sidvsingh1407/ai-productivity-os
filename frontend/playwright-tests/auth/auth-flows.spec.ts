import { test, expect } from '@playwright/test';

// Make random emails unique across processes if multiple runners execute
const getEmail = (prefix) => `${prefix}_${Date.now()}_${Math.random().toString(36).substring(2,7)}@example.com`;

test.describe('Authentication Flows', () => {

  test('Registration -> Verification Email Generated -> Verify Account -> Login', async ({ page, request }) => {
    await page.goto('http://localhost:5173/register', { waitUntil: 'networkidle' });

    const randomEmail = getEmail('testuser');
    await page.fill('input[id="fullName"]', 'Playwright Test User');
    await page.fill('input[id="companyName"]', 'Playwright Corp');
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/login/, { timeout: 15000 });
    await expect(page.locator('text=Registration successful. Please verify your email.')).toBeVisible();

    // Verify Account programmatically
    const verifyRes = await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);
    expect(verifyRes.status()).toBe(200);

    // Login
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/app\/dashboard/, { timeout: 15000 });
  });

  test('Logout and Protected Route Denied', async ({ page, request }) => {
    // 1. Register & Verify
    const randomEmail = getEmail('logout');
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
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/, { timeout: 15000 });

    // 3. Logout
    await page.click('button:has-text("Log out")'); // Using the Sidebar button text
    await expect(page).toHaveURL(/.*\/login/, { timeout: 15000 });

    // 4. Protected Route Blocked
    await page.goto('http://localhost:5173/app/dashboard', { waitUntil: 'networkidle' });
    await expect(page).toHaveURL(/.*\/login/, { timeout: 15000 });
  });

  test('Refresh Token and Refresh Rotation', async ({ page, request }) => {
    // 1. Register & Verify
    const randomEmail = getEmail('refresh');
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
    const randomEmail = getEmail('reset');
    await request.post('http://localhost:8000/auth/register', {
        data: { email: randomEmail, password: 'StrongPassw0rd!', full_name: 'Reset Tester', org_name: 'Reset Org' }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // Forgot Password
    await page.goto('http://localhost:5173/forgot-password', { waitUntil: 'networkidle' });
    await page.fill('input[type="email"]', randomEmail);
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Check your email')).toBeVisible();

    // Get Reset Token from backend test API
    const tokenRes = await request.get(`http://localhost:8000/test-api/get-reset-token?email=${randomEmail}`);
    expect(tokenRes.status()).toBe(200);
    const { token } = await tokenRes.json();

    // Reset Password
    await page.goto(`http://localhost:5173/reset-password?token=${token}`, { waitUntil: 'networkidle' });
    await page.fill('input[id="password"]', 'NewPassw0rd!');
    await page.fill('input[id="confirm-password"]', 'NewPassw0rd!');
    await page.click('button[type="submit"]');

    // Redirect to login eventually (after success banner)
    await expect(page.locator('text=Password reset successful')).toBeVisible();

    // Wait to be on login page, or just navigate
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'NewPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/, { timeout: 15000 });
  });

  test('Delete Account', async ({ page, request }) => {
    const randomEmail = getEmail('delete');
    await request.post('http://localhost:8000/auth/register', {
        data: { email: randomEmail, password: 'StrongPassw0rd!', full_name: 'Delete Tester', org_name: 'Delete Org' }
    });
    await request.get(`http://localhost:8000/test-api/get-verification-token?email=${randomEmail}`);

    // Login to grab API token for direct API deletion for E2E speed, since delete UI might be deep
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
    await page.fill('input[id="email"]', randomEmail);
    await page.fill('input[id="password"]', 'StrongPassw0rd!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/app\/dashboard/, { timeout: 15000 });

    // Bypass Org Admin requirement
    await request.post('http://localhost:8000/test-api/bypass-org-admin', {
        data: { email: randomEmail }
    });

    // Use page request to delete account (intercept the user session)
    // Here we find the Delete Account button in settings (assumes it exists based on requirements)
    await page.goto('http://localhost:5173/app/settings/danger-zone', { waitUntil: 'networkidle' });
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
    await expect(page).toHaveURL(/.*\//, { timeout: 15000 });

    // User Cannot Access Account
    const loginRes = await request.post('http://localhost:8000/auth/login', {
        data: { email: randomEmail, password: 'StrongPassw0rd!' }
    });
    expect(loginRes.status()).not.toBe(200);
  });
});
