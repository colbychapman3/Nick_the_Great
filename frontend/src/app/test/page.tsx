"use client";

import React, { useState } from 'react';

export default function TestPage() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-4">Test Page</h1>
      <p className="mb-4">This is a test page to verify routing is working.</p>
      
      <div className="p-4 bg-blue-100 rounded">
        <h2 className="text-xl font-semibold mb-2">Navigation Links</h2>
        <ul className="list-disc pl-5 space-y-2">
          <li><a href="/" className="text-blue-600 hover:underline">Home</a></li>
          <li><a href="/api-test" className="text-blue-600 hover:underline">API Test</a></li>
        </ul>
      </div>
    </div>
  );
}
