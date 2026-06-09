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
    const response = await apiClient.post('/auth/logout');
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
