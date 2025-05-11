'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/AuthContext';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import PinterestLayout from '@/components/pinterest/PinterestLayout';

interface PinIdea {
  title: string;
  description: string;
  type: string;
  target_board: string;
}

interface PinterestStrategyDetails {
  id: string;
  name: string;
  niche: string;
  targetAudience: string;
  businessGoal: string;
  numPins: number;
  status: string;
  createdAt: string;
  updatedAt: string;
  result?: {
    pinterestStrategy?: {
      overview: string;
      target_audience_analysis: string;
      content_strategy: string;
      board_structure: Record<string, string>;
    };
    pinIdeas?: PinIdea[];
  };
  error?: string;
}

export default function StrategyDetailPage() {
  const { isAuthenticated } = useAuth();
  const params = useParams();
  const strategyId = params.id as string;

  const [strategy, setStrategy] = useState<PinterestStrategyDetails | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch strategy details
  const fetchStrategyDetails = async () => {
    if (!isAuthenticated || !strategyId) return;

    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pinterest/strategy/${strategyId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch strategy details');
      }

      const data = await response.json();
      setStrategy(data);
    } catch (err: any) {
      console.error('Error fetching strategy details:', err);
      setError(err.message || 'Failed to fetch strategy details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated && strategyId) {
      fetchStrategyDetails();
    }
  }, [isAuthenticated, strategyId]);

  const breadcrumbs = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Pinterest', href: '/pinterest' },
    { label: 'Strategies', href: '/pinterest/strategies' },
    { label: strategy?.name || 'Strategy Details' }
  ];

  const actions = (
    <>
      <Link
        href="/pinterest/strategies"
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
      >
        Back to Strategies
      </Link>
      <Link
        href="/pinterest"
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Create New Strategy
      </Link>
    </>
  );

  return (
    <PinterestLayout
      title="Pinterest Strategy Details"
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
          <span className="ml-2">Loading strategy details...</span>
        </div>
      ) : strategy ? (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
              <div>
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  {strategy.name || `Strategy for ${strategy.niche}`}
                </h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  Created on {new Date(strategy.createdAt).toLocaleDateString()}
                </p>
              </div>
              <div className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                strategy.status === 'completed' ? 'bg-green-100 text-green-800' :
                strategy.status === 'failed' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {strategy.status === 'completed' ? 'Completed' :
                 strategy.status === 'failed' ? 'Failed' :
                 strategy.status === 'processing' ? 'Processing' : 'Pending'}
              </div>
            </div>

            <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
              <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Niche</dt>
                  <dd className="mt-1 text-sm text-gray-900">{strategy.niche}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Target Audience</dt>
                  <dd className="mt-1 text-sm text-gray-900">{strategy.targetAudience}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Business Goal</dt>
                  <dd className="mt-1 text-sm text-gray-900">{strategy.businessGoal}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Number of Pin Ideas</dt>
                  <dd className="mt-1 text-sm text-gray-900">{strategy.numPins}</dd>
                </div>
              </dl>
            </div>

            {strategy.status === 'completed' && strategy.result && (
              <>
                {/* Strategy Overview */}
                {strategy.result.pinterestStrategy && (
                  <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Strategy Overview</h3>

                    <div className="bg-gray-50 p-4 rounded-md mb-4">
                      <h4 className="font-medium mb-2">Overview</h4>
                      <p className="text-sm mb-4">{strategy.result.pinterestStrategy.overview}</p>

                      <h4 className="font-medium mb-2">Target Audience Analysis</h4>
                      <p className="text-sm mb-4">{strategy.result.pinterestStrategy.target_audience_analysis}</p>

                      <h4 className="font-medium mb-2">Content Strategy</h4>
                      <p className="text-sm mb-4">{strategy.result.pinterestStrategy.content_strategy}</p>

                      <h4 className="font-medium mb-2">Board Structure</h4>
                      <ul className="list-disc pl-5 mb-4">
                        {Object.entries(strategy.result.pinterestStrategy.board_structure).map(([board, description]) => (
                          <li key={board} className="text-sm mb-1">
                            <span className="font-medium">{board}:</span> {description}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {/* Pin Ideas */}
                {strategy.result.pinIdeas && strategy.result.pinIdeas.length > 0 && (
                  <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Pin Ideas</h3>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {strategy.result.pinIdeas.map((pin, index) => (
                        <div key={index} className="border border-gray-200 rounded-md p-3">
                          <h5 className="font-medium text-sm">{pin.title}</h5>
                          <p className="text-xs text-gray-600 mt-1">{pin.description}</p>
                          <p className="text-xs mt-2">
                            <span className="font-medium">Type:</span> {pin.type}
                          </p>
                          <p className="text-xs">
                            <span className="font-medium">Board:</span> {pin.target_board}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {strategy.status === 'failed' && strategy.error && (
              <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                <div className="bg-red-50 border border-red-200 rounded-md p-4">
                  <h3 className="text-lg font-medium text-red-800 mb-2">Error</h3>
                  <p className="text-sm text-red-700">{strategy.error}</p>
                </div>
              </div>
            )}

            {(strategy.status === 'pending' || strategy.status === 'processing') && (
              <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                  <span className="ml-2">Generating your Pinterest strategy...</span>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6 text-center">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Strategy not found</h3>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>The requested strategy could not be found.</p>
              </div>
              <div className="mt-5">
                <Link
                  href="/pinterest/strategies"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Back to All Strategies
                </Link>
              </div>
            </div>
          </div>
        )}
    </PinterestLayout>
  );
}
