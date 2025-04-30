'use client';

import React from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function CatchAllPage() {
  const params = useParams();
  const slug = params?.slug;
  const path = Array.isArray(slug) ? `/${slug.join('/')}` : slug;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-lg bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-red-500 mb-2">404 - Page Not Found</h1>
        <p className="text-gray-600 mb-4">
          The page <code className="bg-gray-100 px-1 rounded">{path}</code> could not be found.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-6">
          <h2 className="text-lg font-medium text-blue-700 mb-2">Debug Information</h2>
          <p className="text-sm text-blue-600 mb-1">
            <strong>Current path:</strong> {path}
          </p>
          <p className="text-sm text-blue-600 mb-1">
            <strong>Raw params:</strong> {JSON.stringify(params)}
          </p>
          <p className="text-sm text-blue-600 mb-1">
            <strong>Client-side rendering:</strong> Yes
          </p>
          <p className="text-sm text-blue-600">
            <strong>Build time:</strong> {new Date().toISOString()}
          </p>
        </div>
        
        <h2 className="text-lg font-semibold mb-2">Available Routes</h2>
        <ul className="space-y-2 mb-6">
          <li>
            <Link href="/" className="text-blue-600 hover:underline">
              Home Page
            </Link>
          </li>
          <li>
            <Link href="/login" className="text-blue-600 hover:underline">
              Login Page
            </Link>
          </li>
          <li>
            <Link href="/register" className="text-blue-600 hover:underline">
              Register Page
            </Link>
          </li>
          <li>
            <Link href="/dashboard" className="text-blue-600 hover:underline">
              Dashboard Page
            </Link>
          </li>
          <li>
            <Link href="/test" className="text-blue-600 hover:underline">
              Test Page
            </Link>
          </li>
          <li>
            <Link href="/api-test" className="text-blue-600 hover:underline">
              API Test Page
            </Link>
          </li>
        </ul>
        
        <div className="border-t border-gray-200 pt-4">
          <Link 
            href="/"
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Return Home
          </Link>
        </div>
      </div>
    </div>
  );
}
