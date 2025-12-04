/**
 * API service configuration
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Request interceptor - Add auth token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Unauthorized - clear token and redirect to login
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;

// Auth API
export const authAPI = {
    register: (data) => api.post('/api/auth/register', data),
    login: (data) => api.post('/api/auth/login', data),
    getCurrentUser: () => api.get('/api/auth/me')
};

// Expense API
export const expenseAPI = {
    create: (data) => api.post('/api/expenses', data),
    getAll: (month, year) => {
        const params = {};
        if (month) params.month = month;
        if (year) params.year = year;
        return api.get('/api/expenses', { params });
    },
    getById: (id) => api.get(`/api/expenses/${id}`),
    update: (id, data) => api.put(`/api/expenses/${id}`, data),
    delete: (id) => api.delete(`/api/expenses/${id}`)
};

// EMI API
export const emiAPI = {
    create: (data) => api.post('/api/emis', data),
    getAll: () => api.get('/api/emis'),
    getUpcoming: (days = 7) => api.get(`/api/emis/upcoming?days=${days}`),
    getById: (id) => api.get(`/api/emis/${id}`),
    getSchedule: (id) => api.get(`/api/emis/${id}/schedule`),
    update: (id, data) => api.put(`/api/emis/${id}`, data),
    delete: (id) => api.delete(`/api/emis/${id}`)
};

// Analytics API
export const analyticsAPI = {
    getDashboard: () => api.get('/api/analytics/dashboard')
};

// Bank Account API
export const bankAccountAPI = {
    create: (data) => api.post('/api/bank-accounts', data),
    getAll: () => api.get('/api/bank-accounts'),
    getTotalBalance: () => api.get('/api/bank-accounts/total-balance'),
    getById: (id) => api.get(`/api/bank-accounts/${id}`),
    update: (id, data) => api.put(`/api/bank-accounts/${id}`, data),
    delete: (id) => api.delete(`/api/bank-accounts/${id}`)
};

// Asset API
export const assetAPI = {
    create: (data) => api.post('/api/assets', data),
    getAll: () => api.get('/api/assets'),
    getById: (id) => api.get(`/api/assets/${id}`),
    update: (id, data) => api.put(`/api/assets/${id}`, data),
    delete: (id) => api.delete(`/api/assets/${id}`)
};

// Liability API
export const liabilityAPI = {
    create: (data) => api.post('/api/liabilities', data),
    getAll: () => api.get('/api/liabilities'),
    getById: (id) => api.get(`/api/liabilities/${id}`),
    update: (id, data) => api.put(`/api/liabilities/${id}`, data),
    delete: (id) => api.delete(`/api/liabilities/${id}`)
};

// UPI API
export const upiAPI = {
    create: (data) => api.post('/api/upi', data),
    getAll: () => api.get('/api/upi'),
    getById: (id) => api.get(`/api/upi/${id}`),
    delete: (id) => api.delete(`/api/upi/${id}`)
};

// Goal API
export const goalAPI = {
    create: (data) => api.post('/api/goals', data),
    getAll: () => api.get('/api/goals'),
    getById: (id) => api.get(`/api/goals/${id}`),
    update: (id, data) => api.put(`/api/goals/${id}`, data),
    delete: (id) => api.delete(`/api/goals/${id}`)
};
