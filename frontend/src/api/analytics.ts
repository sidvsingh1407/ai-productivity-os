import apiClient from './client';

export const analyticsApi = {
  getScoreTrend: async () => {
    const response = await apiClient.get('/analytics/score-trend');
    return response.data;
  },
  getComplianceRate: async () => {
    const response = await apiClient.get('/analytics/compliance-rate');
    return response.data;
  },
  getAuditVolume: async () => {
    const response = await apiClient.get('/analytics/audit-volume');
    return response.data;
  },
  getDashboardStats: async () => {
    // A helper method combining stats, or relying on a dedicated backend endpoint
    const response = await apiClient.get('/analytics/dashboard');
    return response.data;
  }
};
