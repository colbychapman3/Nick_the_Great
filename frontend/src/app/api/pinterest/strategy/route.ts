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

    // Validate required parameters
    const { niche, targetAudience, businessGoal } = body;
    if (!niche || !targetAudience || !businessGoal) {
      return NextResponse.json({ message: 'Missing required parameters' }, { status: 400 });
    }

    // Forward request to backend
    const response = await fetch(`${apiUrl}/api/pinterest/strategy`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.accessToken || token.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to create Pinterest strategy');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in Pinterest strategy API route:', error);
    return NextResponse.json(
      { message: 'Error creating Pinterest strategy', error: (error as Error).message },
      { status: 500 }
    );
  }
}
