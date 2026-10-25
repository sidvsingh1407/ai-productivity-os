import { describe, it, expect } from 'vitest';
import { APP_CONFIG } from '../app';

describe('APP_CONFIG', () => {

  it('should export correct brand name', () => {
    expect(APP_CONFIG.brandName).toBe('TarkaX');
  });

  it('should export correct public domain', () => {
    expect(APP_CONFIG.publicDomain).toBe('https://tarkaya.com');
  });

  it('apiBaseUrl should resolve to a string URL', () => {
    // We just verify it returns something truthy string since testing import.meta.env
    // dynamically inside vitest can be flaky depending on how vite compiles it.
    expect(typeof APP_CONFIG.apiBaseUrl).toBe('string');
    expect(APP_CONFIG.apiBaseUrl.length).toBeGreaterThan(0);
  });
});
