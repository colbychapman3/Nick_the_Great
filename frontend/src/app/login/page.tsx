"use client";

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [localError, setLocalError] = useState<string | null>(null);
  
  const { login, error: authError, isAuthenticated, isLoading } = useAuth();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      window.location.href = '/dashboard';
    }
  }, [isAuthenticated]);

  // Clear local error when auth error changes
  useEffect(() => {
    if (authError) {
      setLocalError(null);
    }
  }, [authError]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setLocalError(null);
    
    // Basic form validation
    if (!email || !password) {
      setLocalError('Please enter both email and password');
      setIsSubmitting(false);
      return;
    }
    
    try {
      await login(email, password);
    } catch (error: any) {
      console.error('Login error:', error);
      // Any additional local error handling can be done here
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Get API URL for debugging
  const apiUrl = process.env.NEXT_PUBLIC_AUTH_API_URL || 'https://nick-the-great.onrender.com/auth';

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Access your Nick the Great dashboard
          </p>
          
          {/* Debug information (only visible in development) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="mt-2 text-xs text-gray-500 p-2 bg-gray-100 rounded-md">
              <p><strong>Auth API URL:</strong> {apiUrl}</p>
            </div>
          )}
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {/* Display either auth context error or local validation error */}
          {(authError || localError) && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{authError || localError}</span>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </span>
                  Signing in...
                </>
              ) : 'Sign in'}
            </button>
          </div>
          
          <div className="pt-4 text-center border-t border-gray-200">
          </div>
          
          <div className="flex items-center justify-between">
            <div className="text-sm">
              <a href="/" className="font-medium text-blue-600 hover:text-blue-500">
                Back to home
              </a>
            </div>
            <div className="text-sm">
              <a href="/register" className="font-medium text-blue-600 hover:text-blue-500">
                Don't have an account? Sign up
              </a>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
