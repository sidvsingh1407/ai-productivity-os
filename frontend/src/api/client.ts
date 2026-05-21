import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach token
apiClient.interceptors.request.use(
  (config) => {
    const { access_token } = useAuthStore.getState();
    if (access_token && config.headers) {
      config.headers.Authorization = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401s and refresh token
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Avoid infinite loops
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const { refresh_token, clearAuth, setAuth, user, org } = useAuthStore.getState();

      if (refresh_token) {
        try {
          // Attempt to refresh
          const response = await axios.post(`${apiClient.defaults.baseURL}/auth/refresh`, {
            refresh_token,
          });

          const { access_token: new_access_token, refresh_token: new_refresh_token } = response.data;

          // Note: Assuming the backend returns new tokens.
          // In a real app we'd need user/org payload here too if not persisted,
          // but we can reuse the existing user/org from state if they are still valid.
          if (user && org) {
             setAuth(user, org, new_access_token, new_refresh_token || refresh_token);
          }

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${new_access_token}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Refresh failed
          clearAuth();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        clearAuth();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
export { apiClient };
