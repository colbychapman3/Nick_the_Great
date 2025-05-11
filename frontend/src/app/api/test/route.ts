import { NextResponse } from 'next/server';

// Mark this route as dynamic
export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://nick-the-great.onrender.com';

    // Log the API URL
    console.log(`Testing API connection to: ${apiUrl}`);

    // Try to fetch from the API
    const response = await fetch(`${apiUrl}/api/agent/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    // Log the response status
    console.log(`API response status: ${response.status}`);

    // Return the response data
    const data = await response.json().catch(() => ({ error: 'Failed to parse JSON response' }));

    return NextResponse.json({
      apiUrl,
      status: response.status,
      data,
    });
  } catch (error) {
    console.error('Error testing API connection:', error);

    return NextResponse.json({
      error: 'Failed to connect to API',
      message: error instanceof Error ? error.message : String(error),
    }, { status: 500 });
  }
}
