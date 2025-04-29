import React from "react";

export function StatusOverview() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-2xl font-bold mb-4">Status Overview</h2>
      <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
        <p className="text-gray-600 dark:text-gray-300">
          [Agent status, recent activity, or generated plan summaries will appear here...]
        </p>
      </div>
    </div>
  );
}
