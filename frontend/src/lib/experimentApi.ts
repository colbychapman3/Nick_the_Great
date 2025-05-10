import { ApiClient } from './client';

// Define experiment-related types
export interface ExperimentId {
  id: string;
}

export interface ExperimentDefinition {
  name: string;
  type: string;
  description?: string;
  parameters: any;
}

export interface ExperimentStatus {
  id: ExperimentId;
  name: string;
  type: string;
  state: string;
  statusMessage?: string;
  metrics?: any;
  startTime?: string;
  lastUpdateTime?: string;
  estimatedCompletionTime?: string;
  definition?: ExperimentDefinition;
  results?: any;
  logs?: Array<{
    timestamp: string;
    level: string;
    message: string;
  }>;
}

export interface CreateExperimentResponse {
  id: ExperimentId;
  status: {
    success: boolean;
    message: string;
  };
}

export interface StatusResponse {
  success: boolean;
  message: string;
}

/**
 * Fetch all experiments
 * @returns {Promise<ExperimentStatus[]>} List of experiments
 */
export async function fetchExperiments(): Promise<ExperimentStatus[]> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch experiments');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching experiments:', error);
    throw error;
  }
}

/**
 * Fetch a specific experiment by ID
 * @param {string} id - Experiment ID
 * @returns {Promise<ExperimentStatus>} Experiment details
 */
export async function fetchExperimentDetails(id: string): Promise<ExperimentStatus> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch experiment details');
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching experiment ${id}:`, error);
    throw error;
  }
}

/**
 * Create a new experiment
 * @param {ExperimentDefinition} definition - Experiment definition
 * @returns {Promise<CreateExperimentResponse>} Created experiment response
 */
export async function createExperiment(definition: ExperimentDefinition): Promise<CreateExperimentResponse> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ definition }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create experiment');
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating experiment:', error);
    throw error;
  }
}

/**
 * Start an experiment
 * @param {string} id - Experiment ID
 * @returns {Promise<StatusResponse>} Status response
 */
export async function startExperiment(id: string): Promise<StatusResponse> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments/${id}/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to start experiment');
    }

    return await response.json();
  } catch (error) {
    console.error(`Error starting experiment ${id}:`, error);
    throw error;
  }
}

/**
 * Stop an experiment
 * @param {string} id - Experiment ID
 * @returns {Promise<StatusResponse>} Status response
 */
export async function stopExperiment(id: string): Promise<StatusResponse> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments/${id}/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to stop experiment');
    }

    return await response.json();
  } catch (error) {
    console.error(`Error stopping experiment ${id}:`, error);
    throw error;
  }
}

/**
 * Get experiment logs
 * @param {string} id - Experiment ID
 * @returns {Promise<Array<{timestamp: string, level: string, message: string}>>} Experiment logs
 */
export async function fetchExperimentLogs(id: string): Promise<Array<{timestamp: string, level: string, message: string}>> {
  const client = ApiClient();
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/agent/experiments/${id}/logs`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch experiment logs');
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching logs for experiment ${id}:`, error);
    throw error;
  }
}
