'use client';

import React from 'react';
import PinterestStrategy from '@/components/pinterest/PinterestStrategy';
import PinterestLayout from '@/components/pinterest/PinterestLayout';
import Link from 'next/link';

export default function PinterestPage() {
  const breadcrumbs = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Pinterest' }
  ];

  const actions = (
    <>
      <Link
        href="/pinterest/strategies"
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        View All Strategies
      </Link>
      <Link
        href="/dashboard"
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
      >
        Back to Dashboard
      </Link>
    </>
  );

  return (
    <PinterestLayout
      title="Pinterest Strategy"
      breadcrumbs={breadcrumbs}
      actions={actions}
    >
      <PinterestStrategy />
    </PinterestLayout>
  );
}
