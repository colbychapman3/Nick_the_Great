import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Log incoming requests in development
  if (process.env.NODE_ENV === 'development') {
    console.log(`Middleware: Processing ${request.method} request to ${request.nextUrl.pathname}`);
  }

  // Special handling for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    // Don't rewrite for internal routes like revalidate
    if (request.nextUrl.pathname.startsWith('/api/revalidate')) {
      return NextResponse.next();
    }

    // Let Next.js rewrites handle API routes
    return NextResponse.next();
  }

  // Allow normal page rendering to proceed
  return NextResponse.next();
}

// Configuration for which paths middleware should run on
export const config = {
  matcher: [
    // Apply to all routes except static files and Next.js internals
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
