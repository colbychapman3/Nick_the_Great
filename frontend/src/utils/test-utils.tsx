/**
 * Test utilities for the frontend
 */

import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { ThemeProvider } from 'next-themes';

// Add any providers here
const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllProviders, ...options });

// Mock API response for experiments
export const mockExperiments = [
  {
    _id: 'exp-1',
    name: 'Test Experiment 1',
    type: 'AI_DRIVEN_EBOOKS',
    state: 'STATE_RUNNING',
    statusMessage: 'Experiment running',
    metrics: {
      progress_percent: 50,
      elapsed_time_seconds: 300,
      estimated_remaining_seconds: 300,
    },
    startTime: new Date(Date.now() - 300000).toISOString(),
    lastUpdateTime: new Date().toISOString(),
    estimatedCompletionTime: new Date(Date.now() + 300000).toISOString(),
    createdAt: new Date(Date.now() - 600000).toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    _id: 'exp-2',
    name: 'Test Experiment 2',
    type: 'PINTEREST_STRATEGY',
    state: 'STATE_COMPLETED',
    statusMessage: 'Experiment completed',
    metrics: {
      progress_percent: 100,
      elapsed_time_seconds: 600,
      estimated_remaining_seconds: 0,
    },
    startTime: new Date(Date.now() - 600000).toISOString(),
    lastUpdateTime: new Date().toISOString(),
    estimatedCompletionTime: new Date(Date.now()).toISOString(),
    createdAt: new Date(Date.now() - 1200000).toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

// Mock API response for experiment details
export const mockExperimentDetails = {
  _id: 'exp-1',
  name: 'Test Experiment 1',
  type: 'AI_DRIVEN_EBOOKS',
  description: 'A test experiment for AI-driven ebooks',
  parameters: {
    topic: 'Test Topic',
    target_audience: 'Test Audience',
    length: '1000 words',
  },
  state: 'STATE_RUNNING',
  statusMessage: 'Experiment running',
  metrics: {
    progress_percent: 50,
    elapsed_time_seconds: 300,
    estimated_remaining_seconds: 300,
    cpu_usage_percent: 25,
    memory_usage_mb: 100,
    error_count: 0,
  },
  startTime: new Date(Date.now() - 300000).toISOString(),
  lastUpdateTime: new Date().toISOString(),
  estimatedCompletionTime: new Date(Date.now() + 300000).toISOString(),
  createdAt: new Date(Date.now() - 600000).toISOString(),
  updatedAt: new Date().toISOString(),
};

// Mock API response for experiment logs
export const mockExperimentLogs = [
  {
    _id: 'log-1',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 300000).toISOString(),
    level: 'INFO',
    message: 'Experiment started',
    sourceComponent: 'AgentCore',
  },
  {
    _id: 'log-2',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 200000).toISOString(),
    level: 'INFO',
    message: 'Processing data',
    sourceComponent: 'TaskModule',
  },
  {
    _id: 'log-3',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 100000).toISOString(),
    level: 'INFO',
    message: 'Progress update: 50%',
    sourceComponent: 'TaskModule',
  },
];

// Mock API response for experiment metrics
export const mockExperimentMetrics = [
  {
    _id: 'metrics-1',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 300000).toISOString(),
    progressPercent: 0,
    elapsedTimeSeconds: 0,
    estimatedRemainingSeconds: 600,
    cpuUsagePercent: 10,
    memoryUsageMb: 50,
    errorCount: 0,
  },
  {
    _id: 'metrics-2',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 200000).toISOString(),
    progressPercent: 25,
    elapsedTimeSeconds: 100,
    estimatedRemainingSeconds: 450,
    cpuUsagePercent: 20,
    memoryUsageMb: 75,
    errorCount: 0,
  },
  {
    _id: 'metrics-3',
    experimentId: 'exp-1',
    timestamp: new Date(Date.now() - 100000).toISOString(),
    progressPercent: 50,
    elapsedTimeSeconds: 300,
    estimatedRemainingSeconds: 300,
    cpuUsagePercent: 25,
    memoryUsageMb: 100,
    errorCount: 0,
  },
];

// re-export everything
export * from '@testing-library/react';

// override render method
export { customRender as render };
