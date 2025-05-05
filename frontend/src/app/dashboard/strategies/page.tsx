"use client";

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/AuthContext';

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, user } = useAuth();

  // Fetch strategies from the backend
  useEffect(() => {
    const fetchStrategies = async () => {
      if (!isAuthenticated) return;
      
      try {
        setLoading(true);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://nick-the-great.onrender.com';
        const token = localStorage.getItem('token');

        const response = await fetch(`${apiUrl}/api/strategies`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch strategies');
        }

        const data = await response.json();
        setStrategies(data);
      } catch (err: any) {
        console.error('Error fetching strategies:', err);
        setError(err.message || 'Failed to load strategies');
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchStrategies();
    }
  }, [isAuthenticated]);

  // For client components in Next.js 13+, we handle redirects differently
  if (!isAuthenticated) {
    // In a client component, we can use window.location for simple redirects
    // or we can show a "not authenticated" message with a link to login
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Authentication Required
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            You need to be logged in to view this page.
          </p>
          <div className="mt-5">
            <a
              href="/login"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Go to Login
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Investment Strategies</h1>
        <button 
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          onClick={() => {/* Add new strategy function */}}
        >
          Add New Strategy
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      ) : strategies.length === 0 ? (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded relative mb-6">
          <p className="font-medium">No strategies found</p>
          <p className="mt-2">You haven't created any investment strategies yet. Click the "Add New Strategy" button to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {strategies.map((strategy) => (
            <div key={strategy._id} className="border rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <h2 className="text-xl font-semibold mb-2">{strategy.name}</h2>
              <p className="text-gray-600 mb-4">{strategy.description}</p>
              <div className="flex justify-between items-center">
                <span className={`px-3 py-1 rounded-full text-sm ${
                  strategy.status === 'active' ? 'bg-green-100 text-green-800' : 
                  strategy.status === 'paused' ? 'bg-yellow-100 text-yellow-800' : 
                  'bg-gray-100 text-gray-800'
                }`}>
                  {strategy.status || 'Draft'}
                </span>
                <button className="text-blue-600 hover:text-blue-800">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Development placeholder when no real data */}
      {strategies.length === 0 && !loading && !error && (
        <div className="mt-8 border-t pt-8">
          <h2 className="text-xl font-semibold mb-4">Development Placeholders</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                name: "Long-term Growth",
                description: "Focus on stocks with long-term growth potential",
                status: "active"
              },
              {
                name: "Dividend Income",
                description: "Invest in dividend-paying stocks for regular income",
                status: "paused"
              },
              {
                name: "Value Investing",
                description: "Find undervalued companies with strong fundamentals",
                status: "draft"
              }
            ].map((strategy, index) => (
              <div key={index} className="border rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow relative">
                <div className="absolute top-2 right-2 text-xs text-gray-500">(Demo)</div>
                <h2 className="text-xl font-semibold mb-2">{strategy.name}</h2>
                <p className="text-gray-600 mb-4">{strategy.description}</p>
                <div className="flex justify-between items-center">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    strategy.status === 'active' ? 'bg-green-100 text-green-800' : 
                    strategy.status === 'paused' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {strategy.status}
                  </span>
                  <button className="text-blue-600 hover:text-blue-800">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
