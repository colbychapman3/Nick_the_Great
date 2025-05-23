import * as React from "react";

export function ApiClient() {
  // Base API URL - will be replaced with environment variable in production
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';
  console.log('Using API base URL:', baseUrl); // Add this log statement

  /**
   * Make a request to the API
   * @param {string} endpoint - API endpoint
   * @param {string} method - HTTP method
   * @param {object} data - Request data
   * @returns {Promise} - API response
   */
  const request = async (endpoint: string, method: string = 'GET', data: any = null) => {
    const url = `${baseUrl}${endpoint}`;
    console.log('Making request to:', url); // Add this log statement

    // Get token from localStorage
    const token = localStorage.getItem('token');

    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      credentials: 'include' as RequestCredentials // Include cookies for authentication
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);

      // Handle non-JSON responses
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf('application/json') !== -1) {
        const json = await response.json();

        if (!response.ok) {
          throw new Error(json.message || 'API request failed');
        }

        return json;
      } else {
        const text = await response.text();

        if (!response.ok) {
          throw new Error(text || 'API request failed');
        }

        return text;
      }
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  };

  // Agent configuration endpoints
  const getAgentConfig = () => request('/agent/config');
  const updateAgentConfig = (config: any) => request('/agent/config', 'PUT', config);

  // Strategy endpoints
  const getStrategies = () => request('/strategies');
  const getStrategy = (id: string) => request(`/strategies/${id}`);
  const createStrategy = (strategy: any) => request('/strategies', 'POST', strategy);
  const updateStrategy = (id: string, strategy: any) => request(`/strategies/${id}`, 'PUT', strategy);
  const deleteStrategy = (id: string) => request(`/strategies/${id}`, 'DELETE');
  const executeStrategy = (id: string) => request(`/strategies/${id}/execute`, 'POST');

  // Resource endpoints
  const getResources = () => request('/resources');
  const allocateResources = (allocation: any) => request('/resources/allocate', 'POST', allocation);

  // Approval endpoints
  const getApprovals = () => request('/approvals');
  const respondToApproval = (id: string, response: any) => request(`/approvals/${id}/respond`, 'POST', response);

  // Platform endpoints
  const getPlatforms = () => request('/platforms');

  // Recommendation endpoints
  const getRecommendedStrategies = (params: any) => request('/recommendations/strategies', 'POST', params);

  // Simulation endpoints
  const runSimulation = (params: any) => request('/simulation/run', 'POST', params);

  // Debug endpoints
  const validateConfiguration = (config: any) => request('/debug/validate', 'POST', config);
  const getSystemHealth = () => request('/debug/health');

  return {
    getAgentConfig,
    updateAgentConfig,
    getStrategies,
    getStrategy,
    createStrategy,
    updateStrategy,
    deleteStrategy,
    executeStrategy,
    getResources,
    allocateResources,
    getApprovals,
    respondToApproval,
    getPlatforms,
    getRecommendedStrategies,
    runSimulation,
    validateConfiguration,
    getSystemHealth,
    request // Expose the generic request function
  };
}
