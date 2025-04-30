"use client";

import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Nick the Great
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Start your passive income journey
          </p>
        </div>
        
        <div className="mt-8 space-y-4">
          <div>
            <Link href="/register" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Register
            </Link>
          </div>
          
          <div>
            <Link href="/login" className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Login
            </Link>
          </div>
          
          <div className="pt-4 border-t border-gray-200">
            <h3 className="text-center text-sm font-medium text-gray-500 mb-4">Test Pages</h3>
            <div className="flex space-x-4 justify-center">
              <Link href="/test" className="text-sm text-blue-600 hover:text-blue-500">
                Simple Test
              </Link>
              <Link href="/api-test" className="text-sm text-blue-600 hover:text-blue-500">
                API Test
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
