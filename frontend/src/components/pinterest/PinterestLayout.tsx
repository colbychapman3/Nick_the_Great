'use client';

import React, { ReactNode } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/AuthContext';

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface PinterestLayoutProps {
  children: ReactNode;
  title: string;
  breadcrumbs: BreadcrumbItem[];
  actions?: ReactNode;
}

export default function PinterestLayout({ 
  children, 
  title, 
  breadcrumbs,
  actions
}: PinterestLayoutProps) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
        <div className="bg-white shadow-md rounded-lg p-6 max-w-md w-full">
          <h1 className="text-xl font-bold mb-4">Authentication Required</h1>
          <p className="mb-6">You need to be logged in to access the Pinterest strategy feature.</p>
          <Link 
            href="/login" 
            className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
              {breadcrumbs.length > 0 && (
                <nav className="flex mt-2" aria-label="Breadcrumb">
                  <ol className="flex items-center space-x-2">
                    {breadcrumbs.map((item, index) => (
                      <li key={index} className={index > 0 ? "flex items-center" : ""}>
                        {index > 0 && (
                          <svg className="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                          </svg>
                        )}
                        {item.href ? (
                          <Link 
                            href={item.href} 
                            className={`${index > 0 ? "ml-2 " : ""}text-sm ${index === breadcrumbs.length - 1 ? "font-medium text-gray-700" : "text-gray-500 hover:text-gray-700"}`}
                          >
                            {item.label}
                          </Link>
                        ) : (
                          <span className={`${index > 0 ? "ml-2 " : ""}text-sm font-medium text-gray-700`}>
                            {item.label}
                          </span>
                        )}
                      </li>
                    ))}
                  </ol>
                </nav>
              )}
            </div>
            {actions && (
              <div className="flex space-x-3">
                {actions}
              </div>
            )}
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
