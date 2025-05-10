/**
 * Tests for the ExperimentCard component
 */

import React from 'react';
import { render, screen } from '@/utils/test-utils';
import ExperimentCard from './ExperimentCard';

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

  it('renders experiment name and type', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    expect(screen.getByText('Test Experiment')).toBeInTheDocument();
    expect(screen.getByText('AI-Driven Ebooks')).toBeInTheDocument();
  });

  it('renders experiment status and progress', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    expect(screen.getByText('Running')).toBeInTheDocument();
    expect(screen.getByText('50%')).toBeInTheDocument();
  });

  it('renders time information', () => {
    render(<ExperimentCard experiment={mockExperiment} />);
    
    // Check for elapsed time (5 minutes)
    expect(screen.getByText('5m')).toBeInTheDocument();
    
    // Check for remaining time (5 minutes)
    expect(screen.getByText('5m remaining')).toBeInTheDocument();
  });

  it('renders different status colors based on experiment state', () => {
    // Running experiment
    const runningExperiment = { ...mockExperiment, state: 'STATE_RUNNING' };
    const { rerender } = render(<ExperimentCard experiment={runningExperiment} />);
    
    const runningStatus = screen.getByText('Running');
    expect(runningStatus).toHaveClass('bg-blue-100');
    expect(runningStatus).toHaveClass('text-blue-800');
    
    // Completed experiment
    const completedExperiment = { ...mockExperiment, state: 'STATE_COMPLETED' };
    rerender(<ExperimentCard experiment={completedExperiment} />);
    
    const completedStatus = screen.getByText('Completed');
    expect(completedStatus).toHaveClass('bg-green-100');
    expect(completedStatus).toHaveClass('text-green-800');
    
    // Failed experiment
    const failedExperiment = { ...mockExperiment, state: 'STATE_FAILED' };
    rerender(<ExperimentCard experiment={failedExperiment} />);
    
    const failedStatus = screen.getByText('Failed');
    expect(failedStatus).toHaveClass('bg-red-100');
    expect(failedStatus).toHaveClass('text-red-800');
  });

  it('navigates to experiment details page when clicked', () => {
    const mockRouter = require('next/router').useRouter();
    render(<ExperimentCard experiment={mockExperiment} />);
    
    // Click on the card
    screen.getByRole('link').click();
    
    // Check if router.push was called with the correct path
    expect(mockRouter.push).toHaveBeenCalledWith(`/experiments/${mockExperiment._id}`);
  });
});
