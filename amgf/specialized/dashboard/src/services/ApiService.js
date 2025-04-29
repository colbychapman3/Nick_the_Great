import axios from 'axios';
import AuthService from './AuthService';

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor to add API key to all requests
api.interceptors.request.use(
  (config) => {
    const apiKey = AuthService.getApiKey();
    if (apiKey) {
      config.headers['X-API-Key'] = apiKey;
    }
    
    const token = AuthService.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      AuthService.logout();
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

const ApiService = {
  // Authentication
  login: (credentials) => {
    return api.post('/auth/login', credentials);
  },
  
  createApiKey: () => {
    return api.post('/auth/api-key');
  },
  
  // Opportunities
  getOpportunities: (params) => {
    return api.get('/opportunities', { params });
  },
  
  getTopOpportunities: (limit = 10) => {
    return api.get('/opportunities/top', { params: { limit } });
  },
  
  triggerScan: () => {
    return api.post('/opportunities/scan');
  },
  
  // Predictions
  predictOpportunity: (opportunity) => {
    return api.post('/predict', opportunity);
  },
  
  predictBatch: (opportunities) => {
    return api.post('/predict/batch', opportunities);
  },
  
  // Resource Allocation
  getAllocation: () => {
    return api.get('/allocation');
  },
  
  getAllocationHistory: (limit = 10) => {
    return api.get('/allocation/history', { params: { limit } });
  },
  
  triggerAllocation: () => {
    return api.post('/allocate');
  },
  
  adjustStrategyWeights: (weights) => {
    return api.post('/strategy/weights', weights);
  },
  
  adjustRiskTolerance: (riskTolerance) => {
    return api.post('/risk/tolerance', { risk_tolerance: riskTolerance });
  },
  
  reinvestProfits: (profits) => {
    return api.post('/reinvest', { profits });
  },
  
  // System
  getSystemStatus: () => {
    return api.get('/system/status');
  },
  
  runSystem: () => {
    return api.post('/system/run');
  },
  
  // Performance
  getPerformanceData: (timeframe = '24h') => {
    return api.get('/performance', { params: { timeframe } });
  },
  
  getPerformanceMetrics: () => {
    return api.get('/performance/metrics');
  },
  
  // Execution
  executeService: (serviceId, params) => {
    return api.post(`/execute/service/${serviceId}`, params);
  },
  
  executeContent: (contentId, params) => {
    return api.post(`/execute/content/${contentId}`, params);
  },
  
  executeArbitrage: (arbitrageId, params) => {
    return api.post(`/execute/arbitrage/${arbitrageId}`, params);
  },
  
  // Settings
  updateSettings: (settings) => {
    return api.post('/settings', settings);
  },
  
  getSettings: () => {
    return api.get('/settings');
  }
};

export default ApiService;