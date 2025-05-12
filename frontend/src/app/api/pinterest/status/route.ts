import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

// Force dynamic rendering for this route
export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  try {
    const token = await getToken({ req: request });
    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    // Fetch from the backend API
    const response = await fetch(`${apiUrl}/api/pinterest/status`, {
      headers: {
        'Authorization': `Bearer ${token.accessToken || token.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to check Pinterest authentication status');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in Pinterest status API route:', error);
    return NextResponse.json(
      { message: 'Error checking Pinterest authentication status', error: (error as Error).message },
      { status: 500 }
    );
  }
}
