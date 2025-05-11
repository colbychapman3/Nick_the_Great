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

    try {
      // Try to forward request to backend
      const response = await fetch(`${apiUrl}/api/pinterest/strategy/${id}`, {
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
      console.log('Backend API fetch failed, using mock implementation:', fetchError);
    }

    // Mock implementation for when backend is not available (e.g., Vercel deployment)
    // Check if this is a mock ID
    if (id.startsWith('mock-')) {
      // For demo purposes, return a mock strategy with completed status after a delay
      // In a real app, we'd store this in a database

      // Check if enough time has passed to simulate completion (10 seconds)
      const mockTimestamp = parseInt(id.split('-')[1]);
      const currentTime = Date.now();
      const elapsedTime = currentTime - mockTimestamp;

      if (elapsedTime < 10000) {
        // Still "processing"
        return NextResponse.json({
          _id: id,
          userId: 'mock-user',
          type: 'pinterest',
          status: 'processing',
          createdAt: new Date(mockTimestamp).toISOString()
        });
      }

      // Return a completed mock strategy
      return NextResponse.json({
        _id: id,
        userId: 'mock-user',
        type: 'pinterest',
        status: 'completed',
        createdAt: new Date(mockTimestamp).toISOString(),
        result: {
          pinterestStrategy: {
            overview: "This Pinterest strategy focuses on creating visually appealing, value-driven content that resonates with your target audience while supporting your business goals.",
            target_audience_analysis: "Your target audience is looking for inspiration, solutions, and ideas related to your niche. They're likely to engage with content that provides clear value and addresses their specific needs.",
            content_strategy: "Focus on creating high-quality, visually appealing pins that provide immediate value. Use a mix of educational content, inspirational ideas, and product showcases to maintain engagement and drive traffic.",
            board_structure: {
              "Core Niche Board": "Central board focused on your primary business offerings",
              "Inspiration & Ideas": "Broader content that inspires your audience",
              "Educational Content": "How-to guides and educational resources",
              "Community Engagement": "Content that encourages interaction and sharing"
            }
          },
          pinIdeas: [
            {
              title: "5 Essential Tips for Success in Your Niche",
              description: "Learn the top strategies that experts use to excel in this field",
              type: "Infographic",
              target_board: "Educational Content"
            },
            {
              title: "How to Get Started with Your First Project",
              description: "A beginner's guide to taking the first steps in your journey",
              type: "Step-by-step guide",
              target_board: "Core Niche Board"
            },
            {
              title: "Inspiration: Amazing Examples from Industry Leaders",
              description: "Get inspired by these stunning examples from top creators",
              type: "Image collection",
              target_board: "Inspiration & Ideas"
            },
            {
              title: "Quick Guide: Solving Common Problems",
              description: "Solutions to the most frequent challenges you'll encounter",
              type: "Checklist",
              target_board: "Educational Content"
            },
            {
              title: "Join Our Community: Share Your Journey",
              description: "Connect with like-minded individuals and share your experiences",
              type: "Community call",
              target_board: "Community Engagement"
            }
          ]
        }
      });
    }

    // If not a mock ID, return not found
    return NextResponse.json({ message: 'Strategy not found' }, { status: 404 });
  } catch (error) {
    console.error('Error in Pinterest strategy/[id] API route:', error);
    return NextResponse.json(
      { message: 'Error retrieving Pinterest strategy', error: (error as Error).message },
      { status: 500 }
    );
  }
}
