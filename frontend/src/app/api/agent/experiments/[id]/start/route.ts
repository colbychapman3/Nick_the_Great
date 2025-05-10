import { NextRequest, NextResponse } from 'next/server';

/**
 * This is a fallback API route that provides mock functionality for starting experiments
 * when the backend API is not available. This helps prevent 404 errors
 * in the frontend when the backend is not running.
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const experimentId = params.id;
    
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
    
    // Try to call the actual backend API first
    try {
      console.log(`Attempting to start experiment ${experimentId} via backend: ${apiUrl}/api/agent/experiments/${experimentId}/start`);
      
      const response = await fetch(`${apiUrl}/api/agent/experiments/${experimentId}/start`, {
        method: 'POST',
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
        console.log(`Successfully started experiment ${experimentId} via backend`);
        const data = await response.json();
        return NextResponse.json(data);
      }
      
      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error calling backend:', error);
    }
    
    // If we couldn't call the backend, return mock response
    console.log(`Returning mock response for starting experiment ${experimentId}`);
    
    return NextResponse.json({
      success: true,
      message: `Mock started experiment ${experimentId}`,
      _mock: true
    });
  } catch (error) {
    console.error('Error in start experiment API route:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to start experiment',
        message: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}
