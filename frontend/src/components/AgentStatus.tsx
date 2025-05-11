'use client';

import React, { useState, useEffect } from 'react';

interface AgentStatusType {
  status: string;
  userId: string;
  message: string;
}

function AgentStatus() {
  const [agentStatus, setAgentStatus] = useState<AgentStatusType | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function getAgentStatus() {
      try {
        const response = await fetch('/api/agent/status', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAgentStatus(data as AgentStatusType);
      } catch (error: any) {
        console.error("Error fetching agent status:", error);
        setError(error);
      }
    }

    getAgentStatus();
  }, []);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!agentStatus) {
    return <div>Loading agent status...</div>;
  }

  return (
    <div>
      <h2>Agent Status</h2>
      <p>Status: {agentStatus.status}</p>
      <p>User ID: {agentStatus.userId}</p>
      <p>Message: {agentStatus.message}</p>
    </div>
  );
}

export default AgentStatus;
