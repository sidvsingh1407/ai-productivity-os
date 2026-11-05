export const APP_CONFIG = {
  brandName: 'Tarkaya',
  publicDomain: 'https://tarkaya.com',
  get apiBaseUrl() {
    if (!import.meta.env.VITE_API_URL) {
      if (import.meta.env.PROD) {
        throw new Error('VITE_API_URL is not set');
      }
      return 'http://localhost:8000';
    }
    return import.meta.env.VITE_API_URL;
  },
};
