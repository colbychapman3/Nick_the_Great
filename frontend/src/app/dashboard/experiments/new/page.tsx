'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/AuthContext';
import Link from 'next/link';

export default function NewExperimentPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    type: 'AI_DRIVEN_EBOOKS', // Default type
    description: '',
    parameters: {
      // Default empty parameters
    }
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle form input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle parameters change (JSON textarea)
  const handleParametersChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    try {
      const parameters = JSON.parse(e.target.value);
      setFormData({
        ...formData,
        parameters
      });
      setError(null);
    } catch (err) {
      // Don't update parameters if JSON is invalid, but don't show error yet
      // Only show error on submit
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      // Validate parameters
      try {
        JSON.stringify(formData.parameters);
      } catch (err) {
        throw new Error('Invalid parameters JSON');
      }

      // Get token from localStorage
      const token = localStorage.getItem('token');

      // Submit to API
      const response = await fetch('/api/agent/experiments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create experiment');
      }

      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsSubmitting(false);
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
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold leading-tight text-gray-900">Create New Experiment</h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div className="px-4 py-8 sm:px-0">
              <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  {error && (
                    <div className="rounded-md bg-red-50 p-4 mb-6">
                      <div className="flex">
                        <div className="ml-3">
                          <h3 className="text-sm font-medium text-red-800">Error</h3>
                          <div className="mt-2 text-sm text-red-700">
                            <p>{error}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <form onSubmit={handleSubmit}>
                    <div className="space-y-6">
                      <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                          Experiment Name
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            name="name"
                            id="name"
                            required
                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            value={formData.name}
                            onChange={handleInputChange}
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="type" className="block text-sm font-medium text-gray-700">
                          Experiment Type
                        </label>
                        <div className="mt-1">
                          <select
                            id="type"
                            name="type"
                            required
                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            value={formData.type}
                            onChange={handleInputChange}
                          >
                            <option value="AI_DRIVEN_EBOOKS">AI-Driven Ebooks</option>
                            <option value="FREELANCE_WRITING">Freelance Writing</option>
                            <option value="NICHE_AFFILIATE_WEBSITE">Niche Affiliate Website</option>
                            <option value="PINTEREST_STRATEGY">Pinterest Strategy</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                          Description
                        </label>
                        <div className="mt-1">
                          <textarea
                            id="description"
                            name="description"
                            rows={3}
                            required
                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            value={formData.description}
                            onChange={handleInputChange}
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="parameters" className="block text-sm font-medium text-gray-700">
                          Parameters (JSON)
                        </label>
                        <div className="mt-1">
                          <textarea
                            id="parameters"
                            name="parameters"
                            rows={5}
                            className="font-mono shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            defaultValue="{}"
                            onChange={handleParametersChange}
                          />
                        </div>
                        <p className="mt-2 text-sm text-gray-500">
                          Enter parameters as a valid JSON object.
                        </p>
                      </div>

                      <div className="flex justify-end space-x-3">
                        <Link
                          href="/dashboard"
                          className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          Cancel
                        </Link>
                        <button
                          type="submit"
                          disabled={isSubmitting}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                        >
                          {isSubmitting ? 'Creating...' : 'Create Experiment'}
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
