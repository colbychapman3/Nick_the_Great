import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';
import { cookies } from 'next/headers';

// Force dynamic rendering for this route
export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
  try {
    const token = await getToken({ req: request });
    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    // Validate required parameters
    const { code, state } = body;
    if (!code || !state) {
      return NextResponse.json({ message: 'Missing code or state parameter' }, { status: 400 });
    }

    // Forward request to backend
    const response = await fetch(`${apiUrl}/api/pinterest/callback`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.accessToken || token.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to complete Pinterest authentication');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in Pinterest callback API route:', error);
    return NextResponse.json(
      { message: 'Error handling Pinterest callback', error: (error as Error).message },
      { status: 500 }
    );
  }
}
