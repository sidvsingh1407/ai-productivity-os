import { test, expect } from '@playwright/test';

const AUTH_STATE = {
  state: {
    user: {
      id: '00000000-0000-0000-0000-000000000000',
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      role: 'member',
      org_id: '11111111-1111-1111-1111-111111111111',
      is_active: true,
      is_superadmin: false,
    },
    org: {
      id: '11111111-1111-1111-1111-111111111111',
      name: 'Test Org',
      api_key: 'test-api-key',
    },
    organization: {
      id: '11111111-1111-1111-1111-111111111111',
      name: 'Test Org',
      api_key: 'test-api-key',
    },
    access_token: 'fake-jwt-token',
    refresh_token: 'fake-refresh-token',
    isAuthenticated: true,
  },
  version: 0,
};

test.describe('Workflow Routing Audit Authenticated', () => {
  test('Navigate to New Workflow, Create Workflow, Validate Detail Route', async ({ page }) => {
    await page.goto('/');
    await page.evaluate((authState) => {
      localStorage.setItem('auth-storage', JSON.stringify(authState));
      window.location.reload();
    }, AUTH_STATE);
    await page.waitForTimeout(500);

    // Mock API
    await page.route('**/users/me', async route => {
      await route.fulfill({ status: 200, json: AUTH_STATE.state.user });
    });
    await page.route('**/organizations/me', async route => {
      await route.fulfill({ status: 200, json: AUTH_STATE.state.org });
    });
    await page.route('**/audits/?limit=100', async route => {
      await route.fulfill({ status: 200, json: { items: [] } });
    });

    // Use proper matching for API routes (note /api/ or no /api/ depending on Vite proxy if it was running, but here we just match **/*)
    await page.route('**/workflows', async route => {
        await route.fulfill({ status: 201, json: { id: 'test-workflow-123', status: 'completed' } });
    });
    await page.route('**/workflows/', async route => {
        await route.fulfill({ status: 201, json: { id: 'test-workflow-123', status: 'completed' } });
    });

    await page.route('**/workflows/test-workflow-123', async route => {
      await route.fulfill({
        status: 200,
        json: {
          id: 'test-workflow-123',
          status: 'completed',
          mode: 'diagnostic',
          input_config: { industry: 'Tech' },
          blueprints: [],
          intelligence: {
            workflow_maturity: 'Level 2',
            workflow_risk_level: 'High',
            executive_summary: { most_critical_bottleneck: 'Testing phase' },
            bottlenecks: []
          }
        }
      });
    });
    await page.route('**/analytics/**', async route => {
      await route.fulfill({ status: 200, json: {} });
    });

    // 1. Visit Dashboard
    await page.goto('/app/dashboard');
    await page.waitForSelector('text=Workflow Diagnostic', { timeout: 10000 });

    await page.click('aside >> text=Workflow Diagnostic');
    await page.waitForURL('**/app/workflows/new');
    expect(page.url()).toContain('/app/workflows/new');

    await page.fill('input[name="industry"]', 'Tech');
    await page.selectOption('select[name="organizationType"]', 'Startup');
    await page.fill('input[name="department"]', 'Engineering');
    await page.fill('input[name="workflowCategory"]', 'CI/CD');
    await page.selectOption('select[name="teamSize"]', '11-50');
    await page.fill('input[name="currentToolsUsed"]', 'GitHub Actions');
    await page.fill('textarea[name="workflowDescription"]', 'Code commit to production deployment');
    await page.fill('textarea[name="currentChallenges"]', 'Flaky tests taking too long');

    await Promise.all([
      page.waitForURL('**/app/workflows/test-workflow-123'),
      page.click('button[type="submit"]')
    ]);

    expect(page.url()).toContain('/app/workflows/test-workflow-123');
  });
});
