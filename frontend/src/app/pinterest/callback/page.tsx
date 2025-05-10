'use client';

import React, { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';

export default function PinterestCallbackPage() {
  const searchParams = useSearchParams();
  
  useEffect(() => {
    // Get the code and state from the URL
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    
    if (code && state) {
      // Send a message to the opener window with the code and state
      if (window.opener) {
        window.opener.postMessage({
          type: 'pinterest-callback',
          code,
          state
        }, window.location.origin);
        
        // Close the popup window
        window.close();
      } else {
        // If there's no opener, redirect to the Pinterest dashboard
        window.location.href = '/pinterest';
      }
    }
  }, [searchParams]);
  
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="bg-white shadow-md rounded-lg p-6 max-w-md w-full">
        <h1 className="text-xl font-bold mb-4">Pinterest Authentication</h1>
        
        <div className="flex items-center justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-2">Completing authentication...</span>
        </div>
        
        <p className="text-sm text-gray-600 mt-4">
          This window should close automatically. If it doesn't, you can close it manually and return to the Pinterest strategy page.
        </p>
      </div>
    </div>
  );
}
