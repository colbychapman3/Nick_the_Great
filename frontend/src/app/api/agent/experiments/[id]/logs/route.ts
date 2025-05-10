import { NextRequest, NextResponse } from 'next/server';

/**
 * This is a fallback API route that provides mock experiment logs
 * when the backend API is not available. This helps prevent 404 errors
 * in the frontend when the backend is not running.
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const experimentId = params.id;
    
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
    
    // Try to fetch from the actual backend API first
    try {
      console.log(`Attempting to fetch logs for experiment ${experimentId} from backend: ${apiUrl}/api/agent/experiments/${experimentId}/logs`);
      
      const response = await fetch(`${apiUrl}/api/agent/experiments/${experimentId}/logs`, {
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
        console.log(`Successfully fetched logs for experiment ${experimentId} from backend`);
        const data = await response.json();
        return NextResponse.json(data);
      }
      
      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error fetching from backend:', error);
    }
    
    // If we couldn't fetch from the backend, return mock data
    console.log(`Returning mock logs for experiment ${experimentId}`);
    
    // Get current timestamp in seconds
    const now = Math.floor(Date.now() / 1000);
    const oneMinuteAgo = now - 60;
    const twoMinutesAgo = now - 120;
    const fiveMinutesAgo = now - 300;
    
    // Generate mock logs based on experiment ID
    const mockLogs = [
      {
        timestamp: { seconds: fiveMinutesAgo, nanos: 0 },
        level: 'INFO',
        message: `Experiment ${experimentId} started`,
        source_component: 'AgentCore'
      },
      {
        timestamp: { seconds: twoMinutesAgo, nanos: 0 },
        level: 'INFO',
        message: `Processing task 1 for experiment ${experimentId}`,
        source_component: 'TaskExecutor'
      },
      {
        timestamp: { seconds: oneMinuteAgo, nanos: 0 },
        level: 'INFO',
        message: `Task 1 completed for experiment ${experimentId}`,
        source_component: 'TaskExecutor'
      },
      {
        timestamp: { seconds: now, nanos: 0 },
        level: 'INFO',
        message: `Processing task 2 for experiment ${experimentId}`,
        source_component: 'TaskExecutor'
      }
    ];
    
    // Add a warning or error log for some experiment IDs to show variety
    if (experimentId.includes('2')) {
      mockLogs.push({
        timestamp: { seconds: now - 30, nanos: 0 },
        level: 'WARNING',
        message: `Resource constraint detected for experiment ${experimentId}`,
        source_component: 'ResourceMonitor'
      });
    }
    
    if (experimentId.includes('3')) {
      mockLogs.push({
        timestamp: { seconds: now - 45, nanos: 0 },
        level: 'ERROR',
        message: `Failed to connect to external service for experiment ${experimentId}`,
        source_component: 'ExternalServiceConnector'
      });
    }
    
    return NextResponse.json(mockLogs);
  } catch (error) {
    console.error('Error in experiment logs API route:', error);
    return NextResponse.json(
      { 
        error: 'Failed to get experiment logs',
        message: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}
