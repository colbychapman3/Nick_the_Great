'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/AuthContext';
import Link from 'next/link';

// Helper function to format timestamps
function formatTimestamp(timestamp: any): string {
  if (!timestamp) return 'N/A';

  try {
    // Handle different timestamp formats
    let date;
    if (typeof timestamp === 'string') {
      date = new Date(timestamp);
    } else if (timestamp.seconds) {
      // Handle protobuf timestamp format
      date = new Date(Number(timestamp.seconds) * 1000);
    } else {
      return 'Invalid date';
    }

    return date.toLocaleString();
  } catch (e) {
    console.error('Error formatting timestamp:', e);
    return 'Invalid date';
  }
}

// Helper function to get state color
function getStateColor(state: string): string {
  switch (state) {
    case 'STATE_RUNNING':
      return 'bg-green-100 text-green-800';
    case 'STATE_COMPLETED':
      return 'bg-blue-100 text-blue-800';
    case 'STATE_FAILED':
      return 'bg-red-100 text-red-800';
    case 'STATE_STOPPED':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

export default function ExperimentDetailsPage({ params }: { params: { id: string } }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [experiment, setExperiment] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionInProgress, setActionInProgress] = useState(false);
  const [activeTab, setActiveTab] = useState('details');
  const [logs, setLogs] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any[]>([]);

  // Fetch experiment details
  useEffect(() => {
    const fetchExperiment = async () => {
      setLoading(true);
      try {
        const response = await fetch(`/api/agent/experiments/${params.id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch experiment: ${response.statusText}`);
        }
        const data = await response.json();
        setExperiment(data);

        // If the experiment has logs, set them
        if (data.logs) {
          setLogs(data.logs);
        }
      } catch (err: any) {
        console.error('Error fetching experiment:', err);
        setError(err.message || 'Failed to load experiment details');
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated && params.id) {
      fetchExperiment();

      // Set up polling for updates every 5 seconds
      const intervalId = setInterval(fetchExperiment, 5000);

      // Clean up interval on unmount
      return () => clearInterval(intervalId);
    }
  }, [isAuthenticated, params.id]);

  // Fetch logs
  useEffect(() => {
    const fetchLogs = async () => {
      if (!isAuthenticated || !params.id || activeTab !== 'logs') return;

      try {
        const response = await fetch(`/api/agent/experiments/${params.id}/logs`);
        if (!response.ok) {
          throw new Error(`Failed to fetch logs: ${response.statusText}`);
        }
        const data = await response.json();
        setLogs(data);
      } catch (err: any) {
        console.error('Error fetching logs:', err);
        // Don't set error state here to avoid disrupting the main UI
      }
    };

    if (activeTab === 'logs') {
      fetchLogs();

      // Set up polling for logs updates every 5 seconds
      const intervalId = setInterval(fetchLogs, 5000);

      // Clean up interval on unmount or tab change
      return () => clearInterval(intervalId);
    }
  }, [isAuthenticated, params.id, activeTab]);

  // Fetch metrics
  useEffect(() => {
    const fetchMetrics = async () => {
      if (!isAuthenticated || !params.id || activeTab !== 'metrics') return;

      try {
        const response = await fetch(`/api/agent/experiments/${params.id}/metrics`);
        if (!response.ok) {
          throw new Error(`Failed to fetch metrics: ${response.statusText}`);
        }
        const data = await response.json();
        setMetrics(data);
      } catch (err: any) {
        console.error('Error fetching metrics:', err);
        // Don't set error state here to avoid disrupting the main UI
      }
    };

    if (activeTab === 'metrics') {
      fetchMetrics();

      // Set up polling for metrics updates every 5 seconds
      const intervalId = setInterval(fetchMetrics, 5000);

      // Clean up interval on unmount or tab change
      return () => clearInterval(intervalId);
    }
  }, [isAuthenticated, params.id, activeTab]);

  // Handle start experiment
  const handleStart = async () => {
    setActionInProgress(true);
    try {
      const response = await fetch(`/api/agent/experiments/${params.id}/start`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to start experiment');
      }

      // Refresh experiment data
      const updatedResponse = await fetch(`/api/agent/experiments/${params.id}`);
      if (updatedResponse.ok) {
        const data = await updatedResponse.json();
        setExperiment(data);
      }
    } catch (err: any) {
      console.error('Error starting experiment:', err);
      setError(err.message || 'Failed to start experiment');
    } finally {
      setActionInProgress(false);
    }
  };

  // Handle stop experiment
  const handleStop = async () => {
    setActionInProgress(true);
    try {
      const response = await fetch(`/api/agent/experiments/${params.id}/stop`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to stop experiment');
      }

      // Refresh experiment data
      const updatedResponse = await fetch(`/api/agent/experiments/${params.id}`);
      if (updatedResponse.ok) {
        const data = await updatedResponse.json();
        setExperiment(data);
      }
    } catch (err: any) {
      console.error('Error stopping experiment:', err);
      setError(err.message || 'Failed to stop experiment');
    } finally {
      setActionInProgress(false);
    }
  };

  // Redirect if not authenticated
  if (!isLoading && !isAuthenticated) {
    router.push('/login');
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="py-10">
        <header>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold leading-tight text-gray-900">Experiment Details</h1>
            <Link
              href="/dashboard"
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Back to Dashboard
            </Link>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div className="px-4 py-8 sm:px-0">
              {loading ? (
                <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                  <p className="text-gray-500">Loading experiment details...</p>
                </div>
              ) : error ? (
                <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                  <div className="rounded-md bg-red-50 p-4">
                    <div className="flex">
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-red-800">Error</h3>
                        <div className="mt-2 text-sm text-red-700">
                          <p>{error}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : experiment ? (
                <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                  {/* Experiment Header */}
                  <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">{experiment.name}</h3>
                      <p className="mt-1 max-w-2xl text-sm text-gray-500">{experiment.description || 'No description'}</p>
                    </div>
                    <div>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStateColor(experiment.state)}`}>
                        {experiment.state.replace('STATE_', '')}
                      </span>
                    </div>
                  </div>

                  {/* Experiment Actions */}
                  <div className="border-t border-gray-200 px-4 py-4 sm:px-6">
                    <div className="flex space-x-3 justify-end">
                      {experiment.state === 'STATE_DEFINED' && (
                        <button
                          type="button"
                          disabled={actionInProgress}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                          onClick={handleStart}
                        >
                          {actionInProgress ? 'Starting...' : 'Start Experiment'}
                        </button>
                      )}

                      {experiment.state === 'STATE_RUNNING' && (
                        <button
                          type="button"
                          disabled={actionInProgress}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                          onClick={handleStop}
                        >
                          {actionInProgress ? 'Stopping...' : 'Stop Experiment'}
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Tabs */}
                  <div className="border-t border-gray-200">
                    <div className="px-4 py-2 sm:px-6">
                      <nav className="flex space-x-4" aria-label="Tabs">
                        <button
                          type="button"
                          onClick={() => setActiveTab('details')}
                          className={`px-3 py-2 text-sm font-medium rounded-md ${
                            activeTab === 'details'
                              ? 'bg-blue-100 text-blue-700'
                              : 'text-gray-500 hover:text-gray-700'
                          }`}
                        >
                          Details
                        </button>
                        <button
                          type="button"
                          onClick={() => setActiveTab('logs')}
                          className={`px-3 py-2 text-sm font-medium rounded-md ${
                            activeTab === 'logs'
                              ? 'bg-blue-100 text-blue-700'
                              : 'text-gray-500 hover:text-gray-700'
                          }`}
                        >
                          Logs
                        </button>
                        <button
                          type="button"
                          onClick={() => setActiveTab('metrics')}
                          className={`px-3 py-2 text-sm font-medium rounded-md ${
                            activeTab === 'metrics'
                              ? 'bg-blue-100 text-blue-700'
                              : 'text-gray-500 hover:text-gray-700'
                          }`}
                        >
                          Metrics
                        </button>
                      </nav>
                    </div>
                  </div>

                  {/* Details Tab */}
                  {activeTab === 'details' && (
                    <div className="border-t border-gray-200">
                      <dl>
                        <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">ID</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{experiment.id?.id || 'N/A'}</dd>
                        </div>
                        <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Type</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{experiment.type || 'N/A'}</dd>
                        </div>
                        <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Status</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{experiment.status_message || 'N/A'}</dd>
                        </div>
                        <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Start Time</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{formatTimestamp(experiment.start_time)}</dd>
                        </div>
                        <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{formatTimestamp(experiment.last_update_time)}</dd>
                        </div>

                        {/* Show metrics if available */}
                        {experiment.metrics && (
                          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Progress</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                              <div className="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                  className="bg-blue-600 h-2.5 rounded-full"
                                  style={{ width: `${experiment.metrics.progress_percent || 0}%` }}
                                ></div>
                              </div>
                              <span className="text-xs text-gray-500 mt-1 inline-block">
                                {(experiment.metrics.progress_percent || 0).toFixed(1)}%
                              </span>
                            </dd>
                          </div>
                        )}
                      </dl>
                    </div>
                  )}

                  {/* Logs Tab */}
                  {activeTab === 'logs' && (
                    <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                      <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Experiment Logs</h3>
                      {logs.length > 0 ? (
                        <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                          <table className="min-w-full divide-y divide-gray-300">
                            <thead className="bg-gray-50">
                              <tr>
                                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Timestamp</th>
                                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Level</th>
                                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Source</th>
                                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Message</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200 bg-white">
                              {logs.map((log, index) => (
                                <tr key={index}>
                                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-500 sm:pl-6">{formatTimestamp(log.timestamp)}</td>
                                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                      log.level === 'ERROR' ? 'bg-red-100 text-red-800' :
                                      log.level === 'WARNING' ? 'bg-yellow-100 text-yellow-800' :
                                      'bg-green-100 text-green-800'
                                    }`}>
                                      {log.level}
                                    </span>
                                  </td>
                                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{log.source_component}</td>
                                  <td className="px-3 py-4 text-sm text-gray-500">{log.message}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : (
                        <p className="text-gray-500">No logs available for this experiment.</p>
                      )}
                    </div>
                  )}

                  {/* Metrics Tab */}
                  {activeTab === 'metrics' && (
                    <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                      <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Experiment Metrics</h3>
                      {metrics.length > 0 ? (
                        <div className="space-y-6">
                          {/* Progress over time */}
                          <div>
                            <h4 className="text-sm font-medium text-gray-500 mb-2">Progress Over Time</h4>
                            <div className="h-64 bg-gray-50 rounded-lg p-4 flex items-end space-x-2">
                              {metrics.map((metric, index) => (
                                <div key={index} className="flex flex-col items-center">
                                  <div
                                    className="w-8 bg-blue-600 rounded-t"
                                    style={{
                                      height: `${(metric.metrics.progress_percent || 0) / 100 * 200}px`,
                                      minHeight: '1px'
                                    }}
                                  ></div>
                                  <span className="text-xs text-gray-500 mt-1 transform -rotate-45 origin-top-left">
                                    {formatTimestamp(metric.timestamp).split(' ')[1]}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Other metrics */}
                          <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                            <table className="min-w-full divide-y divide-gray-300">
                              <thead className="bg-gray-50">
                                <tr>
                                  <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Timestamp</th>
                                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Progress</th>
                                  {metrics[0]?.metrics?.cpu_usage_percent !== undefined && (
                                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">CPU Usage</th>
                                  )}
                                  {metrics[0]?.metrics?.memory_usage_mb !== undefined && (
                                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Memory Usage</th>
                                  )}
                                  {metrics[0]?.metrics?.pins_created !== undefined && (
                                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Pins Created</th>
                                  )}
                                  {metrics[0]?.metrics?.articles_created !== undefined && (
                                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Articles Created</th>
                                  )}
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-gray-200 bg-white">
                                {metrics.map((metric, index) => (
                                  <tr key={index}>
                                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-500 sm:pl-6">{formatTimestamp(metric.timestamp)}</td>
                                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{(metric.metrics.progress_percent || 0).toFixed(1)}%</td>
                                    {metric.metrics?.cpu_usage_percent !== undefined && (
                                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{metric.metrics.cpu_usage_percent}%</td>
                                    )}
                                    {metric.metrics?.memory_usage_mb !== undefined && (
                                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{metric.metrics.memory_usage_mb} MB</td>
                                    )}
                                    {metric.metrics?.pins_created !== undefined && (
                                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{metric.metrics.pins_created}</td>
                                    )}
                                    {metric.metrics?.articles_created !== undefined && (
                                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{metric.metrics.articles_created}</td>
                                    )}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      ) : (
                        <p className="text-gray-500">No metrics available for this experiment.</p>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                  <p className="text-gray-500">Experiment not found</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
