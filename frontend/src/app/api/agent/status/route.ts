import { NextRequest, NextResponse } from 'next/server';

// Add export config to mark this route as dynamic
export const dynamic = 'force-dynamic';

/**
 * This is a fallback API route that provides a mock agent status
 * when the backend API is not available. This helps prevent 404 errors
 * in the frontend when the backend is not running.
 */
export async function GET(request: NextRequest) {
  try {
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    // Try to fetch from the actual backend API first
    try {
      console.log(`Attempting to fetch agent status from backend: ${apiUrl}/api/agent/status`);

      // Get authorization header from request
      const authHeader = request.headers.get('Authorization');

      const response = await fetch(`${apiUrl}/api/agent/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Forward the authorization header if present
          ...(authHeader ? { 'Authorization': authHeader } : {})
        },
        cache: 'no-store',
      });

      // If the backend API responds successfully, return its response
      if (response.ok) {
        console.log('Successfully fetched agent status from backend');
        const data = await response.json();
        return NextResponse.json(data);
      }

      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error fetching from backend:', error);
    }

    // If we couldn't fetch from the backend, return a mock response
    console.log('Returning mock agent status');

    // Get current timestamp in seconds
    const now = Math.floor(Date.now() / 1000);

    return NextResponse.json({
      agent_state: 'MOCK_MODE',
      active_experiments: 0,
      cpu_usage_percent: 5.2,
      memory_usage_mb: 128.5,
      last_updated: {
        seconds: now,
        nanos: 0
      },
      _mock: true, // Flag to indicate this is mock data
    });
  } catch (error) {
    console.error('Error in agent status API route:', error);
    return NextResponse.json(
      {
        error: 'Failed to get agent status',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
