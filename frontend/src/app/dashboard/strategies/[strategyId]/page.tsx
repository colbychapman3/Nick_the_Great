"use client";

import React from 'react';
import { useParams } from 'next/navigation'; // Hook to get route parameters

export default function StrategyDetailPage() {
  const params = useParams();
  const strategyId = params.strategyId; // Access the dynamic part of the URL

  // TODO: Fetch strategy details from the backend using the strategyId

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Strategy Details</h1>
      <p className="mb-6">
        Displaying details for strategy with ID: <strong>{strategyId}</strong>
      </p>
      
      {/* Placeholder for strategy details */}
      <div className="bg-gray-100 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-2">Strategy Name Placeholder</h2>
        <p className="text-gray-700 mb-4">Strategy description placeholder...</p>
        <p>Status: <span className="font-medium">Placeholder</span></p>
        {/* Add more detail fields here */}
      </div>

      {/* Add buttons for actions like Edit, Delete, etc. */}
      <div className="mt-6">
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded mr-2">
          Edit Strategy
        </button>
        <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">
          Delete Strategy
        </button>
      </div>
    </div>
  );
}
