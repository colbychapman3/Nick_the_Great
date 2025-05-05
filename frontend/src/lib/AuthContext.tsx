"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the User type
interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

// Define the AuthContext interface
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  error: null
});

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        setIsLoading(true);
        
        // Check for token in localStorage
        const token = localStorage.getItem('token');
        if (!token) {
          setIsAuthenticated(false);
          setUser(null);
          setIsLoading(false);
          return;
        }

        // Check if token is valid by parsing it (in a real app, you'd validate with the server)
        try {
          // Simple JWT decoding to get user data from token
          const base64Url = token.split('.')[1];
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          const payload = JSON.parse(window.atob(base64));
          
          // Check if token is expired
          if (payload.exp && payload.exp * 1000 < Date.now()) {
            // Token expired
            localStorage.removeItem('token');
            setIsAuthenticated(false);
            setUser(null);
            setIsLoading(false);
            return;
          }
          
          // Token is valid
          setUser({
            id: payload.id,
            email: payload.email,
            name: payload.name,
            role: payload.role
          });
          setIsAuthenticated(true);
        } catch (e) {
          // Invalid token format
          localStorage.removeItem('token');
          setIsAuthenticated(false);
          setUser(null);
        }
      } catch (error) {
        console.error('Authentication check error:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const apiUrl = process.env.NEXT_PUBLIC_AUTH_API_URL || 'https://nick-the-great.onrender.com/auth';
      console.log('Auth API URL:', apiUrl);
      
      const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      
      console.log('Full Auth URL:', `${apiUrl}/login`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();
      
      // Save token to localStorage
      localStorage.setItem('token', data.token);
      
      // Set user data and auth state
      setUser(data.user);
      setIsAuthenticated(true);
    } catch (err: any) {
      console.error('Error during login', err);
      setError(err.message || 'Login failed. Please try again.');
      setIsAuthenticated(false);
      setUser(null);
      throw err; // Re-throw the error for the component to handle
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const apiUrl = process.env.NEXT_PUBLIC_AUTH_API_URL || 'https://nick-the-great.onrender.com/auth';
      
      const response = await fetch(`${apiUrl}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      const data = await response.json();
      
      // Save token to localStorage
      localStorage.setItem('token', data.token);
      
      // Set user data and auth state
      setUser(data.user);
      setIsAuthenticated(true);
    } catch (err: any) {
      console.error('Error during registration', err);
      setError(err.message || 'Registration failed. Please try again.');
      setIsAuthenticated(false);
      setUser(null);
      throw err; // Re-throw the error for the component to handle
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAuthenticated(false);
    
    // Redirect to login page is handled by the component using the hook
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        login,
        register,
        logout,
        error
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
