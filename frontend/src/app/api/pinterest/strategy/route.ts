import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function POST(request: NextRequest) {
  try {
    const token = await getToken({ req: request });
    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    try {
      // Try to forward request to backend
      const response = await fetch(`${apiUrl}/api/pinterest/strategy`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.accessToken || token.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        return NextResponse.json(data);
      }
    } catch (fetchError) {
      console.log('Backend API fetch failed, using mock implementation:', fetchError);
    }

    // Mock implementation for when backend is not available (e.g., Vercel deployment)
    const { niche, targetAudience, businessGoal } = body;

    if (!niche || !targetAudience || !businessGoal) {
      return NextResponse.json({ message: 'Missing required parameters' }, { status: 400 });
    }

    // Generate a mock strategy ID
    const mockStrategyId = `mock-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

    // Store the strategy request in localStorage (this will be handled client-side)
    // For server-side, we'd use a database or other persistent storage

    return NextResponse.json({
      message: 'Pinterest strategy generation started',
      strategyId: mockStrategyId
    });
  } catch (error) {
    console.error('Error in Pinterest strategy API route:', error);
    return NextResponse.json(
      { message: 'Error creating Pinterest strategy', error: (error as Error).message },
      { status: 500 }
    );
  }
}
