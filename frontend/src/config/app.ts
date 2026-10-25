export const APP_CONFIG = {
  brandName: 'TarkaX',
  publicDomain: 'https://tarkaya.com',
  get apiBaseUrl() {
    return (
      import.meta.env.VITE_API_URL ||
      (import.meta.env.PROD
        ? 'https://ai-productivity-os.onrender.com'
        : 'http://localhost:8000')
    );
  },
};
