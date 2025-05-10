/**
 * Test utilities for the mobile app
 */

import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { AuthProvider } from '../context/AuthContext';

// Mock navigation container
const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthProvider>
      <NavigationContainer>{children}</NavigationContainer>
    </AuthProvider>
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

// re-export everything
export * from '@testing-library/react-native';

// override render method
export { customRender as render };
