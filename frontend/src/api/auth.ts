import apiClient from './client';

export const authApi = {
  login: async (data: any) => {
    const response = await apiClient.post('/auth/login', data);
    return response.data;
  },
  register: async (data: any) => {
    const response = await apiClient.post('/auth/register', data);
    return response.data;
  },
  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  },
  logout: async () => {
    // Optionally we can get refresh_token from state here if not passed in, but the apiClient handles interceptors.
    // Best is to retrieve it directly from store.
    const { useAuthStore } = await import('../store/authStore');
    const state = useAuthStore.getState();
    const response = await apiClient.post('/auth/logout', { refresh_token: state.refresh_token });
    return response.data;
  },
  forgotPassword: async (data: { email: string }) => {
    const response = await apiClient.post('/auth/forgot-password', data);
    return response.data;
  },
  resetPassword: async (data: { token: string; new_password: string }) => {
    const response = await apiClient.post('/auth/reset-password', data);
    return response.data;
  },
  verifyEmail: async (data: { token: string }) => {
    const response = await apiClient.post('/auth/verify-email', data);
    return response.data;
  },
  resendVerification: async (data: { email: string }) => {
    const response = await apiClient.post('/auth/resend-verification', data);
    return response.data;
  },
  changePassword: async (data: { current_password: string; new_password: string }) => {
    const response = await apiClient.post('/auth/change-password', data);
    return response.data;
  }
};
