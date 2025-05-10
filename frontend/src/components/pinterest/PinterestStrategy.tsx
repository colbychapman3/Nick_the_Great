'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/AuthContext';
import PinterestAuth from './PinterestAuth';

interface PinterestStrategyFormData {
  niche: string;
  targetAudience: string;
  businessGoal: string;
  numPins: number;
}

export default function PinterestStrategy() {
  const { isAuthenticated } = useAuth();
  const [isPinterestAuthenticated, setIsPinterestAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [strategyId, setStrategyId] = useState<string | null>(null);
  const [formData, setFormData] = useState<PinterestStrategyFormData>({
    niche: '',
    targetAudience: '',
    businessGoal: '',
    numPins: 5
  });
  const [strategy, setStrategy] = useState<any | null>(null);

  // Handle form input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'numPins' ? parseInt(value) : value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isAuthenticated || !isPinterestAuthenticated) {
      setError('You must be authenticated with both Nick the Great and Pinterest to create a strategy');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);
      setStrategyId(null);
      setStrategy(null);

      const token = localStorage.getItem('token');
      const response = await fetch('/api/pinterest/strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create Pinterest strategy');
      }

      const data = await response.json();
      setSuccess('Pinterest strategy generation started successfully!');
      setStrategyId(data.strategyId);
      
      // Start polling for strategy status
      pollStrategyStatus(data.strategyId);
    } catch (err: any) {
      console.error('Error creating Pinterest strategy:', err);
      setError(err.message || 'Failed to create Pinterest strategy');
    } finally {
      setLoading(false);
    }
  };

  // Poll for strategy status
  const pollStrategyStatus = async (id: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pinterest/strategy/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch strategy status');
      }

      const data = await response.json();
      setStrategy(data);

      // Continue polling if the strategy is still processing
      if (data.status === 'pending' || data.status === 'processing') {
        setTimeout(() => pollStrategyStatus(id), 5000);
      }
    } catch (err: any) {
      console.error('Error polling strategy status:', err);
    }
  };

  // Handle Pinterest authentication status change
  const handlePinterestAuthStatusChange = (isAuthenticated: boolean) => {
    setIsPinterestAuthenticated(isAuthenticated);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Pinterest Strategy Generator</h1>
      
      <PinterestAuth onAuthStatusChange={handlePinterestAuthStatusChange} />
      
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Create Pinterest Strategy</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p>{error}</p>
          </div>
        )}
        
        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            <p>{success}</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="niche" className="block text-sm font-medium text-gray-700 mb-1">
              Business Niche
            </label>
            <input
              type="text"
              id="niche"
              name="niche"
              value={formData.niche}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Sustainable Fashion, Organic Gardening, Digital Marketing"
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="targetAudience" className="block text-sm font-medium text-gray-700 mb-1">
              Target Audience
            </label>
            <input
              type="text"
              id="targetAudience"
              name="targetAudience"
              value={formData.targetAudience}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Millennial women, Small business owners, Health-conscious parents"
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="businessGoal" className="block text-sm font-medium text-gray-700 mb-1">
              Business Goal
            </label>
            <input
              type="text"
              id="businessGoal"
              name="businessGoal"
              value={formData.businessGoal}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Increase website traffic, Generate leads, Build brand awareness"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="numPins" className="block text-sm font-medium text-gray-700 mb-1">
              Number of Pin Ideas
            </label>
            <select
              id="numPins"
              name="numPins"
              value={formData.numPins}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={3}>3 pins</option>
              <option value={5}>5 pins</option>
              <option value={10}>10 pins</option>
              <option value={15}>15 pins</option>
              <option value={20}>20 pins</option>
            </select>
          </div>
          
          <button
            type="submit"
            disabled={loading || !isPinterestAuthenticated}
            className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating Strategy...
              </>
            ) : (
              'Generate Pinterest Strategy'
            )}
          </button>
          
          {!isPinterestAuthenticated && (
            <p className="text-sm text-red-500 mt-2">
              You must connect your Pinterest account before generating a strategy.
            </p>
          )}
        </form>
      </div>
      
      {strategy && (
        <div className="bg-white shadow-md rounded-lg p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Strategy Status</h2>
          
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700">Status:</p>
            <p className={`text-sm ${
              strategy.status === 'completed' ? 'text-green-600' : 
              strategy.status === 'failed' ? 'text-red-600' : 
              'text-yellow-600'
            }`}>
              {strategy.status === 'completed' ? 'Completed' : 
               strategy.status === 'failed' ? 'Failed' : 
               strategy.status === 'processing' ? 'Processing' : 'Pending'}
            </p>
          </div>
          
          {strategy.status === 'completed' && strategy.result && (
            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">Pinterest Strategy</h3>
              
              {/* Display the strategy details */}
              {strategy.result.pinterestStrategy && (
                <div className="bg-gray-50 p-4 rounded-md">
                  <h4 className="font-medium mb-2">Strategy Overview</h4>
                  <p className="text-sm mb-4">{strategy.result.pinterestStrategy.overview}</p>
                  
                  <h4 className="font-medium mb-2">Target Audience</h4>
                  <p className="text-sm mb-4">{strategy.result.pinterestStrategy.target_audience_analysis}</p>
                  
                  <h4 className="font-medium mb-2">Content Strategy</h4>
                  <p className="text-sm mb-4">{strategy.result.pinterestStrategy.content_strategy}</p>
                  
                  <h4 className="font-medium mb-2">Board Structure</h4>
                  <ul className="list-disc pl-5 mb-4">
                    {Object.entries(strategy.result.pinterestStrategy.board_structure).map(([board, description]: [string, any]) => (
                      <li key={board} className="text-sm mb-1">
                        <span className="font-medium">{board}:</span> {description}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {/* Display pin ideas */}
              {strategy.result.pinIdeas && strategy.result.pinIdeas.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Pin Ideas</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {strategy.result.pinIdeas.map((pin: any, index: number) => (
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
            </div>
          )}
          
          {strategy.status === 'failed' && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4 mt-4">
              <p className="text-sm text-red-700">
                {strategy.error || 'Strategy generation failed. Please try again.'}
              </p>
            </div>
          )}
          
          {(strategy.status === 'pending' || strategy.status === 'processing') && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <span className="ml-2">Generating your Pinterest strategy...</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
