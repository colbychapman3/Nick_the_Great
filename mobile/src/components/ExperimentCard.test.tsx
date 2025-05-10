/**
 * Tests for the ExperimentCard component
 */

import React from 'react';
import { render, fireEvent, screen } from '../utils/test-utils';
import ExperimentCard from './ExperimentCard';
import { useNavigation } from '@react-navigation/native';

// Mock the navigation hook
jest.mock('@react-navigation/native', () => {
  return {
    ...jest.requireActual('@react-navigation/native'),
    useNavigation: jest.fn(),
  };
});

describe('ExperimentCard', () => {
  const mockExperiment = {
    _id: 'exp-1',
    name: 'Test Experiment',
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
  };

  const mockNavigation = {
    navigate: jest.fn(),
  };

  beforeEach(() => {
    (useNavigation as jest.Mock).mockReturnValue(mockNavigation);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders experiment name and type', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    expect(screen.getByText('Test Experiment')).toBeTruthy();
    expect(screen.getByText('AI-Driven Ebooks')).toBeTruthy();
  });

  it('renders experiment status and progress', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    expect(screen.getByText('Running')).toBeTruthy();
    expect(screen.getByText('50%')).toBeTruthy();
  });

  it('renders time information', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    // Check for elapsed time (5 minutes)
    expect(screen.getByText('5m')).toBeTruthy();
    
    // Check for remaining time (5 minutes)
    expect(screen.getByText('5m remaining')).toBeTruthy();
  });

  it('navigates to experiment details when pressed', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    // Press the card
    fireEvent.press(screen.getByTestId('experiment-card'));
    
    // Check if navigation.navigate was called with the correct parameters
    expect(mockNavigation.navigate).toHaveBeenCalledWith('ExperimentDetails', {
      experimentId: mockExperiment._id,
    });
  });
});
