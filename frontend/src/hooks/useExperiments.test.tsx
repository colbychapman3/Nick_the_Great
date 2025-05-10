/**
 * Tests for the useExperiments hook
 */

import { renderHook, act } from '@testing-library/react';
import { useExperiments } from './useExperiments';
import { mockExperiments } from '@/utils/test-utils';

// Mock fetch
global.fetch = jest.fn();

describe('useExperiments', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('fetches experiments successfully', async () => {
    // Mock successful fetch response
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        experiments: mockExperiments,
        pagination: {
          total: 2,
          page: 1,
          limit: 10,
          totalPages: 1
        }
      }),
    });

    // Render the hook
    const { result } = renderHook(() => useExperiments());

    // Initially, it should be loading with no data
    expect(result.current.isLoading).toBe(true);
    expect(result.current.experiments).toEqual([]);
    expect(result.current.error).toBeNull();

    // Wait for the fetch to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // After loading, it should have data and not be loading
    expect(result.current.isLoading).toBe(false);
    expect(result.current.experiments).toEqual(mockExperiments);
    expect(result.current.pagination).toEqual({
      total: 2,
      page: 1,
      limit: 10,
      totalPages: 1
    });
    expect(result.current.error).toBeNull();

    // Verify fetch was called with the correct URL
    expect(global.fetch).toHaveBeenCalledWith(
      `${process.env.NEXT_PUBLIC_API_URL}/api/agent/experiments?page=1&limit=10`,
      expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      })
    );
  });

  it('handles fetch error', async () => {
    // Mock failed fetch response
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    });

    // Render the hook
    const { result } = renderHook(() => useExperiments());

    // Wait for the fetch to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // After error, it should not be loading and have an error
    expect(result.current.isLoading).toBe(false);
    expect(result.current.experiments).toEqual([]);
    expect(result.current.error).toBe('Failed to fetch experiments: 500 Internal Server Error');
  });

  it('handles network error', async () => {
    // Mock network error
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    // Render the hook
    const { result } = renderHook(() => useExperiments());

    // Wait for the fetch to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // After error, it should not be loading and have an error
    expect(result.current.isLoading).toBe(false);
    expect(result.current.experiments).toEqual([]);
    expect(result.current.error).toBe('Failed to fetch experiments: Network error');
  });

  it('refetches experiments when called', async () => {
    // Mock successful fetch responses
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          experiments: mockExperiments,
          pagination: {
            total: 2,
            page: 1,
            limit: 10,
            totalPages: 1
          }
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          experiments: [...mockExperiments, {
            _id: 'exp-3',
            name: 'New Experiment',
            type: 'FREELANCE_WRITING',
            state: 'STATE_DEFINED',
          }],
          pagination: {
            total: 3,
            page: 1,
            limit: 10,
            totalPages: 1
          }
        }),
      });

    // Render the hook
    const { result } = renderHook(() => useExperiments());

    // Wait for the initial fetch to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // Verify initial data
    expect(result.current.experiments).toHaveLength(2);

    // Call refetch
    await act(async () => {
      await result.current.refetch();
    });

    // Verify updated data
    expect(result.current.experiments).toHaveLength(3);
    expect(result.current.experiments[2].name).toBe('New Experiment');
    expect(result.current.pagination.total).toBe(3);
  });
});
