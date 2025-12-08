import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token
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

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication APIs
export const signup = async (data) => {
  const response = await api.post('/auth/signup', data);
  return response.data;
};

export const login = async (data) => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Dashboard APIs
export const getDashboardData = async () => {
  const response = await api.get('/dashboard/');
  return response.data;
};

// Upload APIs
export const uploadFile = async (file, sheetName) => {
  const formData = new FormData();
  formData.append('file', file);
  if (sheetName) {
    formData.append('sheet_name', sheetName);
  }
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getUploads = async () => {
  const response = await api.get('/upload/history');
  return response.data;
};

// AI Insights APIs
export const getChatResponse = async (message, context) => {
  const response = await api.post('/ai-insights', {
    message,
    context,
  });
  return response.data;
};

export const explainLeakage = async (uploadId) => {
  const response = await api.get(`/ai-insights/explain/${uploadId}`);
  return response.data;
};

// Chatbot APIs
export const sendChatMessage = async (data) => {
  const response = await api.post('/chatbot', data);
  return response.data;
};

export const getChatHistory = async () => {
  const response = await api.get('/chatbot/history');
  return response.data;
};

export const clearChatHistory = async () => {
  const response = await api.delete('/chatbot/history');
  return response.data;
};

export const getChatSuggestions = async () => {
  const response = await api.get('/chatbot/suggestions');
  return response.data;
};

export const getChatTopics = async () => {
  const response = await api.get('/chatbot/topics');
  return response.data;
};

// Alerts APIs
export const getAlerts = async () => {
  const response = await api.get('/alerts/');
  return response.data;
};

export const createAlert = async (data) => {
  const response = await api.post('/alerts/', data);
  return response.data;
};

export const updateAlert = async (id, data) => {
  const response = await api.put(`/alerts/${id}`, data);
  return response.data;
};

export const deleteAlert = async (id) => {
  const response = await api.delete(`/alerts/${id}`);
  return response.data;
};

// Notifications APIs
export const getNotifications = async () => {
  const response = await api.get('/notifications/');
  return response.data;
};

export const markNotificationAsRead = async (id) => {
  const response = await api.put(`/notifications/${id}/read`);
  return response.data;
};

export const getUnreadCount = async () => {
  const response = await api.get('/notifications/unread/count');
  return response.data;
};

// Reports APIs
export const generateReport = async (data) => {
  const response = await api.post('/reports/generate/', data);
  return response.data;
};

export const getReports = async () => {
  const response = await api.get('/reports/');
  return response.data;
};

export const downloadReport = async (id) => {
  const response = await api.get(`/reports/${id}/download`, {
    responseType: 'blob',
  });
  return response.data;
};

// Settings APIs
export const updateProfile = async (data) => {
  const response = await api.put('/settings/profile', data);
  return response.data;
};

export const changePassword = async (data) => {
  const response = await api.put('/settings/password', data);
  return response.data;
};

// Business Analysis APIs
export const analyzeNewBusiness = async (formData) => {
  const response = await api.post('/business/new/analyze', formData);
  return response.data;
};

export const analyzeExistingBusiness = async (formData) => {
  const response = await api.post('/business/existing/analyze', formData);
  return response.data;
};

export const getBusinessAnalysis = async (analysisId) => {
  const response = await api.get(`/business/analysis/${analysisId}`);
  return response.data;
};

export const getAnalysisHistory = async (limit = 10) => {
  const response = await api.get(`/business/history?limit=${limit}`);
  return response.data;
};

export default api;
