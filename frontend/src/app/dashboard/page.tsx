"use client";

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/lib/AuthContext';

interface AgentStatus {
  agent_state?: string;
  active_experiments?: number;
  cpu_usage_percent?: number;
  memory_usage_mb?: number;
  last_updated?: string; // Assuming timestamp is serialized as string
  error?: string;
}

export default function DashboardPage() {
const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [agentStatus, setAgentStatus] = useState<AgentStatus | null>(null);

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const response = await fetch('/api/agent/status');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: AgentStatus = await response.json();
        setAgentStatus(data);
      } catch (error) {
        console.error("Could not fetch agent status:", error);
        setAgentStatus({ error: "Could not fetch agent status" });
      }
    };

    if (isAuthenticated) {
      fetchAgentStatus();
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
                    Retrieving agent status...
                  </p>
                </div>
                {agentStatus ? (
                  agentStatus.error ? (
                    <div className="px-4 py-5 sm:px-6">
                      <p className="text-sm text-red-500">Error: {agentStatus.error}</p>
                    </div>
                  ) : (
                    <div className="border-t border-gray-200">
                      <dl>
                        <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Agent State</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.agent_state || 'N/A'}</dd>
                        </div>
                        <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Active Experiments</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.active_experiments || 'N/A'}</dd>
                        </div>
                        <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">CPU Usage</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.cpu_usage_percent || 'N/A'}</dd>
                        </div>
                        <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                          <dt className="text-sm font-medium text-gray-500">Memory Usage</dt>
                          <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{agentStatus.memory_usage_mb || 'N/A'}</dd>
                        </div>
                      </dl>
                    </div>
                  )
                ) : (
                  <div className="px-4 py-5 sm:px-6">
                    <p className="text-sm text-gray-500">Loading agent status...</p>
                  </div>
                )}
              </div>

              {/* Development Mode Section */}
              <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4 bg-white">
                <div className="text-center">
                  <h2 className="text-lg font-medium text-gray-900">Development Mode</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    This is a placeholder dashboard for development purposes.
                  </p>
                  <div className="mt-6">
                    {/* Added comment to force a change for git */}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
