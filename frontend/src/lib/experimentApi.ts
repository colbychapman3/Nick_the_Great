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
  const client = ApiClient(); // client.request is now available
  try {
    // The client.request function handles token, headers, and base URL.
    return await client.request('/agent/experiments', 'GET');
  } catch (error) {
    // The error handling here catches errors thrown by client.request
    // or any other errors during the process.
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
    return await client.request(`/agent/experiments/${id}`, 'GET');
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
    return await client.request('/agent/experiments', 'POST', { definition });
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
    return await client.request(`/agent/experiments/${id}/start`, 'POST');
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
    return await client.request(`/agent/experiments/${id}/stop`, 'POST');
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
    return await client.request(`/agent/experiments/${id}/logs`, 'GET');
  } catch (error) {
    console.error(`Error fetching logs for experiment ${id}:`, error);
    throw error;
  }
}
