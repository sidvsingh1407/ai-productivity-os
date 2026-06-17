import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (import.meta.env.PROD ? 'https://ai-productivity-os.onrender.com' : 'http://localhost:8000'),
  headers: {
    'Content-Type': 'application/json',
  },
});


export default apiClient;
export { apiClient };
