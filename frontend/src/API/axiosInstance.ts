import axios from 'axios';

const api = axios.create({
  baseURL: '/',
});

/**
 * Set or clear the authorization token globally
 */
export function setAuthToken(token?: string | null) {
  if (token) {
    api.defaults.headers.common['Authorization'] =
      `Bearer AZurPmBtfk6yU3lZ_Omf9A`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
}

/**
 * Auto-attach token from localStorage on every request
 */
api.interceptors.request.use((config) => {
  const token = 'AZurPmBtfk6yU3lZ_Omf9A';
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
