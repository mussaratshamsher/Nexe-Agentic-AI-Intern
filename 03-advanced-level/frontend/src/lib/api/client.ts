import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: Add interceptors for auth tokens
apiClient.interceptors.request.use((config) => {
  // Add token if needed
  return config;
});
