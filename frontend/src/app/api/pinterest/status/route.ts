import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function GET(request: NextRequest) {
  try {
    const token = await getToken({ req: request });
    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    try {
      // Try to fetch from the backend API
      const response = await fetch(`${apiUrl}/api/pinterest/status`, {
        headers: {
          'Authorization': `Bearer ${token.accessToken || token.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        return NextResponse.json(data);
      }
    } catch (fetchError) {
      console.log('Backend API fetch failed, using mock data:', fetchError);
      // Continue to mock implementation if fetch fails
    }

    // Mock implementation for when backend is not available (e.g., Vercel deployment)
    // Check localStorage for Pinterest auth status (client-side only, so we use cookies for SSR)
    const cookies = request.cookies;
    const pinterestAuthCookie = cookies.get('pinterest_auth');

    if (pinterestAuthCookie) {
      try {
        const authData = JSON.parse(pinterestAuthCookie.value);
        return NextResponse.json({
          authenticated: true,
          tokenStatus: 'valid',
          authenticatedAt: authData.authenticatedAt || new Date().toISOString()
        });
      } catch (e) {
        // Invalid cookie format
      }
    }

    // Default response when no auth data is found
    return NextResponse.json({ authenticated: false });
  } catch (error) {
    console.error('Error in Pinterest status API route:', error);
    return NextResponse.json(
      { message: 'Error checking Pinterest authentication status', error: (error as Error).message },
      { status: 500 }
    );
  }
}
