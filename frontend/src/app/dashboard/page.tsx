"use client";

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/lib/AuthContext';

// Define interfaces based on agent.proto messages (simplified for frontend)
interface ExperimentId {
  id: string;
}

interface ExperimentDefinition {
  type: string; // Use string for enum name
  name: string;
  description: string;
  parameters: any; // Use any for Struct, will be JSON-like object
}

interface ExperimentStatus {
  id: ExperimentId;
  name: string;
  type: string; // Use string for enum name
  state: string; // Use string for enum name
  status_message: string;
  metrics: any; // Use any for Struct
  start_time?: { seconds: number, nanos: number }; // Timestamp structure
  last_update_time?: { seconds: number, nanos: number };
  estimated_completion_time?: { seconds: number, nanos: number };
}

interface AgentStatus {
  agent_state: string;
  active_experiments: number;
  cpu_usage_percent: number;
  memory_usage_mb: number;
  last_updated?: { seconds: number, nanos: number }; // Timestamp structure
}

interface AgentStatusResponse extends AgentStatus {
    error?: string; // Add error for fetch failures
}


export default function DashboardPage() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [agentStatus, setAgentStatus] = useState<AgentStatusResponse | null>(null);
  const [experiments, setExperiments] = useState<ExperimentStatus[]>([]); // State for list of experiments
  const [loadingStatus, setLoadingStatus] = useState(true);

  // Define fetchAgentData outside useEffect so it can be referenced elsewhere
  const fetchAgentData = async () => {
    setLoadingStatus(true);
    try {
      // Get token from localStorage
      const token = localStorage.getItem('token');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      };

      // Fetch Agent Status with retry logic
      let statusData: AgentStatus | null = null;
      let statusError: Error | null = null;

      try {
        console.log('Fetching agent status...');
        const statusResponse = await fetch('/api/agent/status', {
          headers,
          // Add cache control to prevent caching
          cache: 'no-store',
        });

        if (!statusResponse.ok) {
          console.warn(`Agent status response not OK: ${statusResponse.status}`);
          // Don't throw immediately, try to parse the response
          const errorData = await statusResponse.json().catch(() => ({}));
          if (errorData._mock) {
            // This is our mock endpoint response, use it
            console.log('Using mock agent status data');
            statusData = errorData;
          } else {
            throw new Error(`HTTP error fetching agent status! status: ${statusResponse.status}`);
          }
        } else {
          statusData = await statusResponse.json();
          console.log('Successfully fetched agent status');
        }
      } catch (error: any) {
        console.error("Error fetching agent status:", error);
        statusError = error;
      }

      // Update state based on status fetch results
      if (statusData) {
        setAgentStatus(statusData);
      } else if (statusError) {
        setAgentStatus({
          error: statusError.message || "Could not fetch agent data",
          agent_state: 'UNKNOWN',
          active_experiments: 0,
          cpu_usage_percent: 0,
          memory_usage_mb: 0
        });
      }

      // Fetch list of experiments
      try {
        console.log('Fetching experiments...');
        const experimentsResponse = await fetch('/api/agent/experiments', {
          headers,
          // Add cache control to prevent caching
          cache: 'no-store',
        });

        if (experimentsResponse.ok) {
          const experimentsData: ExperimentStatus[] = await experimentsResponse.json();
          console.log(`Fetched ${experimentsData.length} experiments`);
          setExperiments(experimentsData);
        } else {
          console.error(`HTTP error fetching experiments! status: ${experimentsResponse.status}`);
          // Don't throw here, we'll just show empty experiments list
        }
      } catch (expError: any) {
        console.error("Could not fetch experiments:", expError);
        // Don't throw here, we'll just show empty experiments list
      }

    } catch (error: any) {
      console.error("Could not fetch agent data:", error);
      setAgentStatus({
        error: error.message || "Could not fetch agent data",
        agent_state: 'UNKNOWN',
        active_experiments: 0,
        cpu_usage_percent: 0,
        memory_usage_mb: 0
      });
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {

    if (isAuthenticated) {
      fetchAgentData();
      // Optionally set up an interval to refresh status periodically
      const intervalId = setInterval(fetchAgentData, 15000); // Refresh every 15 seconds
      return () => clearInterval(intervalId); // Cleanup interval on unmount
    }
  }, [isAuthenticated]);

  // For client components in Next.js 13+, we handle redirects differently
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // In a client component, we can use window.location
      window.location.href = '/login';
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect from the useEffect
  }

  // Helper to format timestamp
  const formatTimestamp = (timestamp?: { seconds: number, nanos: number }) => {
      if (!timestamp) return 'N/A';
      const date = new Date(timestamp.seconds * 1000);
      return date.toLocaleString(); // Or format as needed
  };


  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <span className="text-xl font-bold text-gray-900">Nick the Great</span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <a href="/dashboard" className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </a>
                <a href="/dashboard/strategies" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Strategies
                </a>
                <a href="/dashboard/resources" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Resources
                </a>
              </div>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:items-center">
              <div className="ml-3 relative">
                <div className="flex items-center">
                  <span className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-600 bg-white hover:text-gray-700">
                    {user?.name}
                  </span>
                  <button
                    type="button"
                    onClick={logout}
                    className="ml-4 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="py-10">
        <header>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold leading-tight text-gray-900">Welcome to Your Dashboard</h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div className="px-4 py-8 sm:px-0">
              {/* Agent Status Section */}
              <div className="bg-white shadow overflow-hidden rounded-lg mb-4">
                <div className="px-4 py-5 sm:px-6">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Agent Core Service Status</h3>
                  <p className="mt-1 max-w-2xl text-sm text-gray-500">
                    {loadingStatus ? 'Loading agent status...' : (agentStatus?.error ? 'Error fetching status.' : 'Current status of the Agent Core service.')}
                  </p>
                </div>
                {agentStatus ? (
                  agentStatus.error ? (
                    <div className="px-4 py-5 sm:px-6">
                      <p className="text-sm text-red-500">Error: {agentStatus.error}</p>
                    </div>
                  ) : (
                    <div className="border-t border-gray-200">
                      <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <div className="text-sm font-medium text-gray-500">Agent State</div>
                        <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.agent_state || 'N/A'}</div>
                      </div>
                      <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <div className="text-sm font-medium text-gray-500">Active Experiments</div>
                        <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.active_experiments ?? 'N/A'}</div>
                      </div>
                      <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <div className="text-sm font-medium text-gray-500">CPU Usage</div>
                        <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.cpu_usage_percent?.toFixed(2) ?? 'N/A'}%</div>
                      </div>
                      <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <div className="text-sm font-medium text-gray-500">Memory Usage</div>
                        <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.memory_usage_mb?.toFixed(2) ?? 'N/A'} MB</div>
                      </div>
                      <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <div className="text-sm font-medium text-gray-500">Last Updated</div>
                        <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{formatTimestamp(agentStatus.last_updated)}</div>
                      </div>
                    </div>
                  )
                ) : (
                  <div className="px-4 py-5 sm:px-6">
                    <p className="text-sm text-gray-500">Loading agent status...</p>
                  </div>
                )}
              </div>

              {/* Experiments List Section */}
               <div className="bg-white shadow overflow-hidden rounded-lg">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                  <div>
                    <h3 className="text-lg font-medium leading-6 text-gray-900">Experiments</h3>
                    <p className="mt-1 max-w-2xl text-sm text-gray-500">
                      List of experiments managed by the agent.
                    </p>
                  </div>
                  <button
                    type="button"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={() => {
                      window.location.href = '/dashboard/experiments/new';
                    }}
                  >
                    New Experiment
                  </button>
                </div>
                <div className="border-t border-gray-200">
                  {experiments.length === 0 ? (
                    <div className="px-4 py-5 sm:px-6 text-sm text-gray-500">
                      No experiments found.
                    </div>
                  ) : (
                    <ul role="list" className="divide-y divide-gray-200">
                      {experiments.map((experiment) => (
                        <li key={experiment.id.id} className="px-4 py-4 sm:px-6">
                          <div className="flex items-center justify-between">
                            <div className="text-sm font-medium text-gray-900 truncate">
                              {experiment.name} ({experiment.type})
                            </div>
                            <div className="ml-2 flex-shrink-0 flex">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                experiment.state === 'STATE_RUNNING' ? 'bg-blue-100 text-blue-800' :
                                experiment.state === 'STATE_COMPLETED' ? 'bg-green-100 text-green-800' :
                                experiment.state === 'STATE_FAILED' ? 'bg-red-100 text-red-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {experiment.state}
                              </span>
                            </div>
                          </div>
                          <div className="mt-2 sm:flex sm:justify-between">
                            <div className="sm:flex">
                              <p className="flex items-center text-sm text-gray-500">
                                {experiment.status_message || 'No status message'}
                              </p>
                            </div>
                            <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                {/* Display start time if available */}
                                {experiment.start_time && (
                                    <p className="mr-2">Started: {formatTimestamp(experiment.start_time)}</p>
                                )}
                                {/* Display last update time if available */}
                                {experiment.last_update_time && (
                                     <p>Last Update: {formatTimestamp(experiment.last_update_time)}</p>
                                )}
                            </div>
                          </div>

                          {/* Experiment Actions */}
                          <div className="mt-3 flex space-x-2">
                            {experiment.state === 'STATE_DEFINED' && (
                              <button
                                type="button"
                                className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                onClick={async () => {
                                  try {
                                    const token = localStorage.getItem('token');
                                    const response = await fetch(`/api/agent/experiments/${experiment.id.id}/start`, {
                                      method: 'POST',
                                      headers: {
                                        'Content-Type': 'application/json',
                                        'Authorization': token ? `Bearer ${token}` : ''
                                      }
                                    });
                                    if (response.ok) {
                                      // Refresh data after starting experiment
                                      fetchAgentData();
                                    } else {
                                      console.error('Failed to start experiment');
                                    }
                                  } catch (error) {
                                    console.error('Error starting experiment:', error);
                                  }
                                }}
                              >
                                Start
                              </button>
                            )}

                            {experiment.state === 'STATE_RUNNING' && (
                              <button
                                type="button"
                                className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                                onClick={async () => {
                                  try {
                                    const token = localStorage.getItem('token');
                                    const response = await fetch(`/api/agent/experiments/${experiment.id.id}/stop`, {
                                      method: 'POST',
                                      headers: {
                                        'Content-Type': 'application/json',
                                        'Authorization': token ? `Bearer ${token}` : ''
                                      }
                                    });
                                    if (response.ok) {
                                      // Refresh data after stopping experiment
                                      fetchAgentData();
                                    } else {
                                      console.error('Failed to stop experiment');
                                    }
                                  } catch (error) {
                                    console.error('Error stopping experiment:', error);
                                  }
                                }}
                              >
                                Stop
                              </button>
                            )}

                            <button
                              type="button"
                              className="inline-flex items-center px-2.5 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                              onClick={() => {
                                // Navigate to experiment details page
                                window.location.href = `/dashboard/experiments/${experiment.id.id}`;
                              }}
                            >
                              View Details
                            </button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>


              {/* Development Mode Section - Can be removed or repurposed later */}
              {/*
              <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4 bg-white mt-4">
                <div className="text-center">
                  <h2 className="text-lg font-medium text-gray-900">Development Mode</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    This section can be used for development-specific tools or information.
                  </p>
                </div>
              </div>
              */}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
