import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const token = await getToken({ req: request });
    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const { id } = params;
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

    // Forward request to backend
    const response = await fetch(`${apiUrl}/api/pinterest/strategy/${id}`, {
      headers: {
        'Authorization': `Bearer ${token.accessToken || token.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json({ message: 'Strategy not found' }, { status: 404 });
      }

      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to retrieve Pinterest strategy');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in Pinterest strategy/[id] API route:', error);
    return NextResponse.json(
      { message: 'Error retrieving Pinterest strategy', error: (error as Error).message },
      { status: 500 }
    );
  }
}
