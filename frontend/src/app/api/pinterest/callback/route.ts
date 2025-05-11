import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';
import { cookies } from 'next/headers';

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
      const response = await fetch(`${apiUrl}/api/pinterest/callback`, {
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
    const { code, state } = body;

    if (!code || !state) {
      return NextResponse.json({ message: 'Missing code or state parameter' }, { status: 400 });
    }

    // For demo purposes, we'll just set a cookie with mock authentication data
    const mockAuthData = {
      authenticated: true,
      tokenStatus: 'valid',
      authenticatedAt: new Date().toISOString()
    };

    // Set a cookie with the mock auth data
    const cookieStore = cookies();
    cookieStore.set('pinterest_auth', JSON.stringify(mockAuthData), {
      path: '/',
      maxAge: 86400, // 1 day
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production'
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error in Pinterest callback API route:', error);
    return NextResponse.json(
      { message: 'Error handling Pinterest callback', error: (error as Error).message },
      { status: 500 }
    );
  }
}
