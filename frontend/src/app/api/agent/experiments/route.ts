import { NextRequest, NextResponse } from 'next/server';

// Mark this route as dynamic
export const dynamic = 'force-dynamic';

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

/**
 * Handle POST requests to create a new experiment
 */
export async function POST(request: NextRequest) {
  try {
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    // Parse the request body
    let experimentData;
    try {
      experimentData = await request.json();
      console.log('Received experiment creation request:', experimentData);
    } catch (error) {
      console.error('Error parsing request body:', error);
      return NextResponse.json(
        {
          error: 'Invalid request body',
          message: 'Could not parse JSON body'
        },
        { status: 400 }
      );
    }

    // Try to send to the actual backend API first
    try {
      console.log(`Attempting to create experiment via backend: ${apiUrl}/api/agent/experiments`);

      const response = await fetch(`${apiUrl}/api/agent/experiments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Forward the authorization header if present
          ...(request.headers.get('Authorization')
            ? { 'Authorization': request.headers.get('Authorization') as string }
            : {})
        },
        body: JSON.stringify(experimentData),
        cache: 'no-store',
      });

      // If the backend API responds successfully, return its response
      if (response.ok) {
        console.log('Successfully created experiment via backend');
        const data = await response.json();
        return NextResponse.json(data);
      }

      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error sending to backend:', error);
    }

    // If we couldn't send to the backend, return mock response
    console.log('Returning mock experiment creation response');

    // Generate a mock experiment ID
    const mockId = `mock-exp-${Math.floor(Math.random() * 1000).toString().padStart(3, '0')}`;
    const now = Math.floor(Date.now() / 1000);

    return NextResponse.json({
      id: { id: mockId },
      name: experimentData.name || 'Unnamed Experiment',
      type: experimentData.type || 'TYPE_GENERIC',
      state: 'STATE_DEFINED',
      status_message: 'Created successfully (mock)',
      metrics: {
        progress_percent: 0,
        estimated_remaining_seconds: 3600,
        error_count: 0
      },
      last_update_time: {
        seconds: now,
        nanos: 0
      },
      definition: experimentData,
      _mock: true
    });
  } catch (error) {
    console.error('Error in create experiment API route:', error);
    return NextResponse.json(
      {
        error: 'Failed to create experiment',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}