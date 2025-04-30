"use client";

import React, { useState, useEffect } from 'react';

export default function ApiTestPage() {
  const [testResults, setTestResults] = useState<any>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [backendUrl, setBackendUrl] = useState<string>('https://nick-the-great-api.onrender.com');
  const [error, setError] = useState<string>('');

  async function testEndpoint(endpoint: string, method: string = 'GET', body: any = null) {
    try {
      setLoading(true);
      
      const options: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      };
      
      if (body) {
        options.body = JSON.stringify(body);
      }
      
      const response = await fetch(`${backendUrl}${endpoint}`, options);
      
      // Check response type
      const contentType = response.headers.get('content-type');
      let data;
      let responseText;
      
      try {
        responseText = await response.text();
        
        if (contentType && contentType.includes('application/json')) {
          data = JSON.parse(responseText);
        } else {
          data = { text: responseText, contentType };
        }
      } catch (e) {
        data = { error: 'Failed to parse response', text: responseText };
      }
      
      return {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries()),
        data
      };
    } catch (error: any) {
      return {
        error: true,
        message: error.message
      };
    } finally {
      setLoading(false);
    }
  }

  async function runAllTests() {
    try {
      setError('');
      setLoading(true);
      
      // Test the health endpoint
      const healthResult = await testEndpoint('/api/debug/health');
      
      // Test the login endpoint
      const loginResult = await testEndpoint('/api/auth/login', 'POST', {
        email: 'demo@example.com',
        password: 'password'
      });
      
      // Test the register endpoint
      const registerResult = await testEndpoint('/api/auth/register', 'POST', {
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123'
      });
      
      setTestResults({
        health: healthResult,
        login: loginResult,
        register: registerResult
      });
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">API Connection Test</h1>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Backend URL
        </label>
        <div className="flex">
          <input
            type="text"
            value={backendUrl}
            onChange={(e) => setBackendUrl(e.target.value)}
            className="flex-grow px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={runAllTests}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {loading ? 'Testing...' : 'Run Tests'}
          </button>
        </div>
      </div>
      
      {error && (
        <div className="p-4 mb-6 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {Object.keys(testResults).length > 0 && (
        <div className="space-y-8">
          {Object.entries(testResults).map(([endpoint, result]: [string, any]) => (
            <div key={endpoint} className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4 capitalize">{endpoint} Endpoint</h2>
              
              <div className="mb-4">
                <span className="inline-block px-3 py-1 rounded-full text-sm font-medium mr-2 mb-2" 
                  style={{ 
                    backgroundColor: result.error || !result.status || result.status >= 400 
                      ? '#FEE2E2' : '#D1FAE5',
                    color: result.error || !result.status || result.status >= 400 
                      ? '#B91C1C' : '#047857'
                  }}>
                  {result.error 
                    ? 'Error' 
                    : result.status 
                      ? `Status: ${result.status} ${result.statusText || ''}` 
                      : 'Unknown Status'}
                </span>
              </div>
              
              <div className="overflow-x-auto">
                <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto whitespace-pre-wrap">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
