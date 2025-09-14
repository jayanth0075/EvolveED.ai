// Axios API config placeholder
import axios from 'axios';
import toast from 'react-hot-toast';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api/',
  headers: { 'Content-Type': 'application/json' },
});

// Add auth interceptor
API.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if(token) config.headers['Authorization'] = `Bearer ${token}`;
  return config;
});

// Response interceptor for error handling
API.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    const message = error.response?.data?.message || error.message || 'Something went wrong';
    toast.error(message);

    return Promise.reject(error);
  }
);

export default API;