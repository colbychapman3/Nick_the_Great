import { NextRequest, NextResponse } from 'next/server';

// Mark this route as dynamic
export const dynamic = 'force-dynamic';

// Define the metrics interface to include all possible metric types
interface ExperimentMetrics {
  progress_percent: number;
  cpu_usage_percent: number;
  memory_usage_mb: number;
  error_count: number;
  estimated_remaining_seconds: number;
  // Pinterest-specific metrics
  pins_created?: number;
  boards_created?: number;
  // Content-specific metrics
  articles_created?: number;
  words_generated?: number;
  // Ebook-specific metrics
  pages_generated?: number;
  chapters_completed?: number;
}

/**
 * This is a fallback API route that provides mock experiment metrics
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
      console.log(`Attempting to fetch metrics for experiment ${experimentId} from backend: ${apiUrl}/api/agent/experiments/${experimentId}/metrics`);

      const response = await fetch(`${apiUrl}/api/agent/experiments/${experimentId}/metrics`, {
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
        console.log(`Successfully fetched metrics for experiment ${experimentId} from backend`);
        const data = await response.json();
        return NextResponse.json(data);
      }

      console.log(`Backend API returned status: ${response.status}`);
    } catch (error) {
      console.error('Error fetching from backend:', error);
    }

    // If we couldn't fetch from the backend, return mock data
    console.log(`Returning mock metrics for experiment ${experimentId}`);

    // Get current timestamp in seconds
    const now = Math.floor(Date.now() / 1000);
    const oneHourAgo = now - 3600;

    // Generate mock metrics data points
    const mockMetrics = [];
    const numDataPoints = 12; // One data point every 5 minutes for the last hour

    for (let i = 0; i < numDataPoints; i++) {
      const timestamp = oneHourAgo + (i * 300); // 300 seconds = 5 minutes
      const progress = Math.min(100, Math.floor((i / (numDataPoints - 1)) * 100));

      // Generate some variation in the metrics
      const cpuUsage = 20 + Math.floor(Math.random() * 30); // 20-50%
      const memoryUsage = 100 + Math.floor(Math.random() * 100); // 100-200 MB

      mockMetrics.push({
        timestamp: { seconds: timestamp, nanos: 0 },
        metrics: {
          progress_percent: progress,
          cpu_usage_percent: cpuUsage,
          memory_usage_mb: memoryUsage,
          error_count: 0,
          estimated_remaining_seconds: Math.max(0, 3600 - (i * 300))
        } as ExperimentMetrics
      });
    }

    // Add experiment-specific metrics based on ID
    if (experimentId.includes('pinterest') || experimentId.includes('001')) {
      // Add Pinterest-specific metrics
      mockMetrics.forEach((metric, index) => {
        metric.metrics.pins_created = Math.floor(index * 2.5);
        metric.metrics.boards_created = Math.floor(index / 4);
      });
    } else if (experimentId.includes('content') || experimentId.includes('002')) {
      // Add Content-specific metrics
      mockMetrics.forEach((metric, index) => {
        metric.metrics.articles_created = Math.floor(index / 3);
        metric.metrics.words_generated = Math.floor(index * 250);
      });
    } else if (experimentId.includes('ebook') || experimentId.includes('003')) {
      // Add Ebook-specific metrics
      mockMetrics.forEach((metric, index) => {
        metric.metrics.pages_generated = Math.floor(index * 2);
        metric.metrics.chapters_completed = Math.floor(index / 4);
      });
    }

    return NextResponse.json(mockMetrics);
  } catch (error) {
    console.error('Error in experiment metrics API route:', error);
    return NextResponse.json(
      {
        error: 'Failed to get experiment metrics',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
