'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/AuthContext';

interface PinterestAuthProps {
  onAuthStatusChange?: (isAuthenticated: boolean) => void;
}

export default function PinterestAuth({ onAuthStatusChange }: PinterestAuthProps) {
  const { isAuthenticated } = useAuth();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [pinterestStatus, setPinterestStatus] = useState<{
    authenticated: boolean;
    tokenStatus?: string;
    authenticatedAt?: string;
  } | null>(null);

  // Check Pinterest authentication status
  const checkPinterestStatus = async () => {
    if (!isAuthenticated) return;

    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch('/api/pinterest/status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to check Pinterest authentication status');
      }

      const data = await response.json();
      setPinterestStatus(data);

      // Notify parent component if callback is provided
      if (onAuthStatusChange) {
        onAuthStatusChange(data.authenticated);
      }
    } catch (err: any) {
      console.error('Error checking Pinterest status:', err);
      setError(err.message || 'Failed to check Pinterest authentication status');
    } finally {
      setLoading(false);
    }
  };

  // Initialize authentication
  const initiatePinterestAuth = async () => {
    if (!isAuthenticated) return;

    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');

      try {
        // Try to fetch from the backend API
        const response = await fetch('/api/pinterest/auth-url', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();

          // Open the authorization URL in a new window
          window.open(data.authUrl, 'pinterest-auth', 'width=800,height=600');
          return;
        }
      } catch (fetchError) {
        console.log('Backend API fetch failed, using mock implementation:', fetchError);
      }

      // Mock implementation for when backend is not available (e.g., Vercel deployment)
      const appId = process.env.NEXT_PUBLIC_PINTEREST_APP_ID || '1518892';
      const redirectUri = process.env.NEXT_PUBLIC_PINTEREST_REDIRECT_URI ||
                         `${window.location.origin}/pinterest/callback`;

      // Generate a mock state parameter
      const state = btoa(JSON.stringify({
        userId: 'mock-user',
        timestamp: Date.now()
      }));

      // For demo/development purposes, we'll just set a cookie directly
      // In production, this should go through the proper OAuth flow
      const mockAuthData = {
        authenticated: true,
        tokenStatus: 'valid',
        authenticatedAt: new Date().toISOString()
      };

      // Store in a cookie for the mock API implementation
      document.cookie = `pinterest_auth=${JSON.stringify(mockAuthData)}; path=/; max-age=86400`;

      // Notify parent component
      if (onAuthStatusChange) {
        onAuthStatusChange(true);
      }

      // Update local state
      setPinterestStatus(mockAuthData);

      // Show success message
      setError(null);
      alert('Mock Pinterest authentication successful! This is a simulated connection for demo purposes.');

    } catch (err: any) {
      console.error('Error initiating Pinterest auth:', err);
      setError(err.message || 'Failed to initiate Pinterest authentication');
    } finally {
      setLoading(false);
    }
  };

  // Check status on component mount and when authentication state changes
  useEffect(() => {
    if (isAuthenticated) {
      checkPinterestStatus();
    }
  }, [isAuthenticated]);

  // Handle the callback from Pinterest
  useEffect(() => {
    // Function to handle the callback message from the popup window
    const handleCallback = async (event: MessageEvent) => {
      // Verify the origin of the message
      if (event.origin !== window.location.origin) return;

      // Check if the message is from our Pinterest callback
      if (event.data && event.data.type === 'pinterest-callback') {
        const { code, state } = event.data;

        try {
          setLoading(true);
          setError(null);

          const token = localStorage.getItem('token');
          const response = await fetch('/api/pinterest/callback', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ code, state })
          });

          if (!response.ok) {
            throw new Error('Failed to complete Pinterest authentication');
          }

          // Check the updated status
          await checkPinterestStatus();
        } catch (err: any) {
          console.error('Error handling Pinterest callback:', err);
          setError(err.message || 'Failed to complete Pinterest authentication');
        } finally {
          setLoading(false);
        }
      }
    };

    // Add event listener for messages from the popup
    window.addEventListener('message', handleCallback);

    // Clean up the event listener
    return () => {
      window.removeEventListener('message', handleCallback);
    };
  }, []);

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Pinterest Authentication</h2>

      {loading && (
        <div className="flex items-center justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-2">Loading...</span>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
      )}

      {!loading && pinterestStatus && (
        <div className={`border rounded-md p-4 mb-4 ${pinterestStatus.authenticated ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'}`}>
          <p className={pinterestStatus.authenticated ? 'text-green-700' : 'text-yellow-700'}>
            {pinterestStatus.authenticated
              ? `Connected to Pinterest (${pinterestStatus.tokenStatus === 'valid' ? 'Active' : 'Expired'})`
              : 'Not connected to Pinterest'}
          </p>

          {pinterestStatus.authenticated && pinterestStatus.authenticatedAt && (
            <p className="text-sm text-gray-600 mt-1">
              Connected since: {new Date(pinterestStatus.authenticatedAt).toLocaleString()}
            </p>
          )}
        </div>
      )}

      <button
        type="button"
        onClick={initiatePinterestAuth}
        disabled={loading}
        className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
      >
        {pinterestStatus?.authenticated ? 'Reconnect to Pinterest' : 'Connect to Pinterest'}
      </button>

      {pinterestStatus?.authenticated && (
        <p className="text-sm text-gray-500 mt-2">
          Your Pinterest account is connected. You can reconnect if you need to refresh your authentication.
        </p>
      )}
    </div>
  );
}
