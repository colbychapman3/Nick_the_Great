import { NextRequest, NextResponse } from 'next/server';

/**
 * This is a fallback API route that provides mock experiment details
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
      console.log(`Attempting to fetch experiment ${experimentId} from backend: ${apiUrl}/api/agent/experiments/${experimentId}`);

      const response = await fetch(`${apiUrl}/api/agent/experiments/${experimentId}`, {
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
        console.log(`Successfully fetched experiment ${experimentId} from backend`);
        const data = await response.json();
        return NextResponse.json(data);
      }

      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error fetching from backend:', error);
    }

    // If we couldn't fetch from the backend, return mock data
    console.log(`Returning mock data for experiment ${experimentId}`);

    // Get current timestamp in seconds
    const now = Math.floor(Date.now() / 1000);
    const fiveMinutesAgo = now - 300;

    // Check if this is one of our mock experiment IDs
    if (experimentId === 'mock-exp-001') {
      return NextResponse.json({
        id: { id: 'mock-exp-001' },
        name: 'Mock Pinterest Strategy',
        type: 'TYPE_PINTEREST',
        state: 'STATE_DEFINED',
        status_message: 'Ready to start',
        metrics: {
          progress_percent: 0,
          estimated_remaining_seconds: 3600,
          error_count: 0,
          pins_created: 0,
          boards_created: 0
        },
        last_update_time: {
          seconds: now,
          nanos: 0
        },
        definition: {
          name: 'Mock Pinterest Strategy',
          type: 'TYPE_PINTEREST',
          description: 'A mock Pinterest strategy experiment for testing',
          parameters: {
            board_count: 3,
            pins_per_board: 5,
            topics: ['houseplants', 'indoor gardening', 'plant care']
          }
        },
        _mock: true,
        logs: [
          {
            timestamp: { seconds: now - 300, nanos: 0 },
            level: 'INFO',
            message: 'Experiment created',
            source_component: 'AgentCore'
          },
          {
            timestamp: { seconds: now - 240, nanos: 0 },
            level: 'INFO',
            message: 'Experiment configuration validated',
            source_component: 'AgentCore'
          }
        ]
      });
    } else if (experimentId === 'mock-exp-002') {
      return NextResponse.json({
        id: { id: 'mock-exp-002' },
        name: 'Mock Content Generation',
        type: 'TYPE_CONTENT',
        state: 'STATE_RUNNING',
        status_message: 'Generating content...',
        metrics: {
          progress_percent: 45,
          estimated_remaining_seconds: 1800,
          error_count: 0,
          articles_created: 2,
          words_generated: 1500
        },
        start_time: {
          seconds: fiveMinutesAgo,
          nanos: 0
        },
        last_update_time: {
          seconds: now,
          nanos: 0
        },
        definition: {
          name: 'Mock Content Generation',
          type: 'TYPE_CONTENT',
          description: 'A mock content generation experiment for testing',
          parameters: {
            article_count: 5,
            words_per_article: 1000,
            topics: ['indoor plants', 'plant care', 'houseplant tips']
          }
        },
        _mock: true,
        logs: [
          {
            timestamp: { seconds: fiveMinutesAgo, nanos: 0 },
            level: 'INFO',
            message: 'Experiment started',
            source_component: 'AgentCore'
          },
          {
            timestamp: { seconds: fiveMinutesAgo + 60, nanos: 0 },
            level: 'INFO',
            message: 'Processing task 1',
            source_component: 'TaskExecutor'
          },
          {
            timestamp: { seconds: fiveMinutesAgo + 120, nanos: 0 },
            level: 'INFO',
            message: 'Task 1 completed',
            source_component: 'TaskExecutor'
          },
          {
            timestamp: { seconds: now - 60, nanos: 0 },
            level: 'INFO',
            message: 'Processing task 2',
            source_component: 'TaskExecutor'
          }
        ]
      });
    } else {
      // Return a generic mock experiment for any other ID
      return NextResponse.json({
        id: { id: experimentId },
        name: `Mock Experiment ${experimentId}`,
        type: 'TYPE_GENERIC',
        state: 'STATE_DEFINED',
        status_message: 'Mock experiment details',
        metrics: {
          progress_percent: 0,
          estimated_remaining_seconds: 3600,
          error_count: 0
        },
        last_update_time: {
          seconds: now,
          nanos: 0
        },
        definition: {
          name: `Mock Experiment ${experimentId}`,
          type: 'TYPE_GENERIC',
          description: 'A generic mock experiment for testing',
          parameters: {
            param1: 'value1',
            param2: 'value2'
          }
        },
        _mock: true,
        logs: [
          {
            timestamp: { seconds: now - 120, nanos: 0 },
            level: 'INFO',
            message: 'Experiment created',
            source_component: 'AgentCore'
          },
          {
            timestamp: { seconds: now - 60, nanos: 0 },
            level: 'INFO',
            message: 'Experiment configuration validated',
            source_component: 'AgentCore'
          }
        ]
      });
    }
  } catch (error) {
    console.error('Error in experiment details API route:', error);
    return NextResponse.json(
      {
        error: 'Failed to get experiment details',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
