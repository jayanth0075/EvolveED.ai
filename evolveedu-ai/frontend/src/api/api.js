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

// Response interceptor for error handling with detailed logging
API.interceptors.response.use(
  response => {
    console.log('API Response:', response.config.url, response.status);
    return response;
  },
  error => {
    // Log error details for debugging
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });

    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    if (error.response?.status === 403) {
      toast.error('You do not have permission to perform this action.');
    }

    if (error.response?.status === 500) {
      toast.error('Server error. Please try again later.');
    }

    const message = error.response?.data?.message || error.response?.data?.detail || error.message || 'Something went wrong';
    toast.error(message);

    return Promise.reject(error);
  }
);

export default API;