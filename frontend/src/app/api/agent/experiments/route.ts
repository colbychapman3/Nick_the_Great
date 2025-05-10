import { NextRequest, NextResponse } from 'next/server';

/**
 * This is a fallback API route that provides mock experiment data
 * when the backend API is not available. This helps prevent 404 errors
 * in the frontend when the backend is not running.
 */
export async function GET(request: NextRequest) {
  try {
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
    
    // Try to fetch from the actual backend API first
    try {
      console.log(`Attempting to fetch experiments from backend: ${apiUrl}/api/agent/experiments`);
      
      const response = await fetch(`${apiUrl}/api/agent/experiments`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Forward the authorization header if present
          ...(request.headers.get('Authorization') 
            ? { 'Authorization': request.headers.get('Authorization') as string } 
            : {})
        },
        cache: 'no-store',
      });
      
      // If the backend API responds successfully, return its response
      if (response.ok) {
        console.log('Successfully fetched experiments from backend');
        const data = await response.json();
        return NextResponse.json(data);
      }
      
      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error fetching from backend:', error);
    }
    
    // If we couldn't fetch from the backend, return mock data
    console.log('Returning mock experiments data');
    
    // Get current timestamp in seconds
    const now = Math.floor(Date.now() / 1000);
    const fiveMinutesAgo = now - 300;
    
    return NextResponse.json([
      {
        id: { id: 'mock-exp-001' },
        name: 'Mock Pinterest Strategy',
        type: 'TYPE_PINTEREST',
        state: 'STATE_DEFINED',
        status_message: 'Ready to start',
        metrics: {
          progress_percent: 0,
          estimated_remaining_seconds: 3600,
          error_count: 0
        },
        last_update_time: {
          seconds: now,
          nanos: 0
        },
        _mock: true
      },
      {
        id: { id: 'mock-exp-002' },
        name: 'Mock Content Generation',
        type: 'TYPE_CONTENT',
        state: 'STATE_RUNNING',
        status_message: 'Generating content...',
        metrics: {
          progress_percent: 45,
          estimated_remaining_seconds: 1800,
          error_count: 0
        },
        start_time: {
          seconds: fiveMinutesAgo,
          nanos: 0
        },
        last_update_time: {
          seconds: now,
          nanos: 0
        },
        _mock: true
      }
    ]);
  } catch (error) {
    console.error('Error in experiments API route:', error);
    return NextResponse.json(
      { 
        error: 'Failed to get experiments',
        message: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}
