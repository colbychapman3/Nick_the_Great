'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/AuthContext';
import Link from 'next/link';
import PinterestLayout from '@/components/pinterest/PinterestLayout';

interface PinterestStrategy {
  id: string;
  name: string;
  niche: string;
  targetAudience: string;
  businessGoal: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

export default function PinterestStrategiesPage() {
  const { isAuthenticated } = useAuth();
  const [strategies, setStrategies] = useState<PinterestStrategy[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch strategies
  const fetchStrategies = async () => {
    if (!isAuthenticated) return;

    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch('/api/pinterest/strategies', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch Pinterest strategies');
      }

      const data = await response.json();
      setStrategies(data);
    } catch (err: any) {
      console.error('Error fetching Pinterest strategies:', err);
      setError(err.message || 'Failed to fetch Pinterest strategies');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchStrategies();
    }
  }, [isAuthenticated]);

  const breadcrumbs = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Pinterest', href: '/pinterest' },
    { label: 'Strategies' }
  ];

  const actions = (
    <Link
      href="/pinterest"
      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
    >
      Create New Strategy
    </Link>
  );

  return (
    <PinterestLayout
      title="Pinterest Strategies"
      breadcrumbs={breadcrumbs}
      actions={actions}
    >
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-2">Loading strategies...</span>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {strategies.length === 0 ? (
            <div className="px-4 py-5 sm:p-6 text-center">
              <h3 className="text-lg leading-6 font-medium text-gray-900">No strategies found</h3>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>You haven't created any Pinterest strategies yet.</p>
              </div>
              <div className="mt-5">
                <Link
                  href="/pinterest"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Create Your First Strategy
                </Link>
              </div>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {strategies.map((strategy) => (
                <li key={strategy.id}>
                  <Link href={`/pinterest/strategies/${strategy.id}`} className="block hover:bg-gray-50">
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-blue-600 truncate">{strategy.name || `Strategy for ${strategy.niche}`}</p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            strategy.status === 'completed' ? 'bg-green-100 text-green-800' :
                            strategy.status === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {strategy.status === 'completed' ? 'Completed' :
                             strategy.status === 'failed' ? 'Failed' :
                             strategy.status === 'processing' ? 'Processing' : 'Pending'}
                          </p>
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            <span className="truncate">{strategy.niche}</span>
                          </p>
                          <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                            <span className="truncate">Target: {strategy.targetAudience}</span>
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <p>Created: {new Date(strategy.createdAt).toLocaleDateString()}</p>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </PinterestLayout>
  );
}
