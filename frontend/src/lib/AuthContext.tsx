"use client";

import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';

// Define the user type
interface User {
  id: string;
  name: string;
  email: string;
}

// Define the authentication context interface
interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  devLogin: () => void; // For development bypass
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create a hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Props for the AuthProvider component
interface AuthProviderProps {
  children: ReactNode;
  enableDevMode?: boolean;
}

// Default test user for development
const DEV_USER: User = {
  id: 'dev-user-123',
  name: 'Development User',
  email: 'dev@example.com'
};

// Authentication provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ 
  children,
  enableDevMode = process.env.NODE_ENV === 'development' || true // Enable by default in development
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const checkAuth = () => {
      try {
        const token = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');
        
        if (token && storedUser) {
          // In a real app, you would verify the token with the backend
          setUser(JSON.parse(storedUser));
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error checking authentication', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Auto-login for development mode
  useEffect(() => {
    if (enableDevMode && !isAuthenticated && !loading) {
      console.log('🔧 Development mode enabled - Auto login available');
    }
  }, [enableDevMode, isAuthenticated, loading]);

  // Login function
  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would call your API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api';
      
      try {
        const response = await fetch(`${apiUrl}/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });
        
        if (!response.ok) {
          throw new Error('Login failed');
        }
        
        const data = await response.json();
        
        // Store token and user in localStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        setUser(data.user);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error during login', error);
        throw new Error('Login failed. Please try again.');
      }
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (name: string, email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would call your API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api';
      
      try {
        const response = await fetch(`${apiUrl}/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, email, password }),
        });
        
        if (!response.ok) {
          throw new Error('Registration failed');
        }
        
        const data = await response.json();
        
        // Store token and user in localStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        setUser(data.user);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error during registration', error);
        throw new Error('Registration failed. Please try again.');
      }
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Development login (bypass authentication)
  const devLogin = () => {
    if (!enableDevMode) {
      console.warn('Development mode is disabled');
      return;
    }
    
    const token = `dev-token-${Date.now()}`;
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(DEV_USER));
    
    setUser(DEV_USER);
    setIsAuthenticated(true);
    setError(null);
    
    console.log('🔑 Development login successful');
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        isAuthenticated,
        login,
        register,
        logout,
        devLogin
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
