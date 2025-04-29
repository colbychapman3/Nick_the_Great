import jwt_decode from 'jwt-decode';

const TOKEN_KEY = 'amgf_token';
const API_KEY = 'amgf_api_key';
const USER_KEY = 'amgf_user';

const AuthService = {
  /**
   * Login user and store token
   * @param {string} token - JWT token
   * @param {object} user - User object
   * @returns {object} User object
   */
  login: (token, user) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    return user;
  },

  /**
   * Logout user and remove token
   */
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(API_KEY);
    localStorage.removeItem(USER_KEY);
  },

  /**
   * Check if user is logged in
   * @returns {boolean} True if user is logged in
   */
  isLoggedIn: () => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return false;

    try {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;
      
      // Check if token is expired
      if (decoded.exp < currentTime) {
        AuthService.logout();
        return false;
      }
      
      return true;
    } catch (error) {
      AuthService.logout();
      return false;
    }
  },

  /**
   * Get current user
   * @returns {object|null} User object or null if not logged in
   */
  getCurrentUser: () => {
    if (!AuthService.isLoggedIn()) {
      return null;
    }
    
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch (error) {
      return null;
    }
  },

  /**
   * Get JWT token
   * @returns {string|null} JWT token or null if not logged in
   */
  getToken: () => {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Store API key
   * @param {string} apiKey - API key
   */
  storeApiKey: (apiKey) => {
    localStorage.setItem(API_KEY, apiKey);
  },

  /**
   * Get API key
   * @returns {string|null} API key or null if not set
   */
  getApiKey: () => {
    return localStorage.getItem(API_KEY);
  },

  /**
   * Check if token is valid and not expired
   * @param {string} token - JWT token
   * @returns {boolean} True if token is valid
   */
  isTokenValid: (token) => {
    if (!token) return false;
    
    try {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;
      
      // Check if token is expired
      return decoded.exp >= currentTime;
    } catch (error) {
      return false;
    }
  },

  /**
   * Get user ID from token
   * @returns {string|null} User ID or null if not logged in
   */
  getUserId: () => {
    const token = AuthService.getToken();
    if (!token) return null;
    
    try {
      const decoded = jwt_decode(token);
      return decoded.sub || decoded.user_id;
    } catch (error) {
      return null;
    }
  },

  /**
   * Check if user has required role
   * @param {string|string[]} requiredRoles - Required role(s)
   * @returns {boolean} True if user has required role
   */
  hasRole: (requiredRoles) => {
    const user = AuthService.getCurrentUser();
    if (!user || !user.roles) return false;
    
    if (Array.isArray(requiredRoles)) {
      return requiredRoles.some(role => user.roles.includes(role));
    }
    
    return user.roles.includes(requiredRoles);
  }
};

export default AuthService;