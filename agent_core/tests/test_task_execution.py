"""
Unit tests for the task execution functionality.
"""

import pytest
import uuid
from unittest.mock import MagicMock, patch
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Import the modules to test
from main import AgentServiceServicer, experiment_statuses, running_tasks, _execute_task, _handle_task_completion, _update_experiment_metrics

class TestTaskExecution:
    """Test the task execution functionality."""
    
    def test_execute_task(self, mock_experiment_status, mock_task_module, reset_experiment_statuses):
        """Test executing a task."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        # Mock the task module selection
        with patch('main._get_task_module_for_experiment_type', return_value=mock_task_module):
            # Act
            result = _execute_task(experiment_id)
            
            # Assert
            assert result is not None
            assert result['success'] is True
            assert 'message' in result
            assert 'results' in result
            
            # Verify the task module was called
            mock_task_module.execute.assert_called_once_with(mock_experiment_status)
    
    def test_handle_task_completion_success(self, mock_experiment_status, reset_experiment_statuses):
        """Test handling successful task completion."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        task_result = {
            'success': True,
            'message': 'Task executed successfully',
            'results': {
                'output': 'Test output'
            }
        }
        
        # Act
        _handle_task_completion(experiment_id, task_result)
        
        # Assert
        assert experiment_statuses[experiment_id].state == 'STATE_COMPLETED'
        assert experiment_statuses[experiment_id].status_message == 'Task executed successfully'
    
    def test_handle_task_completion_failure(self, mock_experiment_status, reset_experiment_statuses):
        """Test handling failed task completion."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        task_result = {
            'success': False,
            'message': 'Task execution failed',
            'error': 'Test error'
        }
        
        # Act
        _handle_task_completion(experiment_id, task_result)
        
        # Assert
        assert experiment_statuses[experiment_id].state == 'STATE_FAILED'
        assert experiment_statuses[experiment_id].status_message == 'Task execution failed: Test error'
    
    def test_update_experiment_metrics(self, mock_experiment_status, reset_experiment_statuses):
        """Test updating experiment metrics."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        metrics = {
            'progress_percent': 50.0,
            'elapsed_time_seconds': 300.0,
            'estimated_remaining_seconds': 300.0,
            'cpu_usage_percent': 25.0,
            'memory_usage_mb': 100.0,
            'error_count': 0,
            'custom_metric': 'test value'
        }
        
        # Act
        _update_experiment_metrics(experiment_id, metrics)
        
        # Assert
        assert experiment_statuses[experiment_id].metrics['progress_percent'] == 50.0
        assert experiment_statuses[experiment_id].metrics['elapsed_time_seconds'] == 300.0
        assert experiment_statuses[experiment_id].metrics['estimated_remaining_seconds'] == 300.0
        assert experiment_statuses[experiment_id].metrics['cpu_usage_percent'] == 25.0
        assert experiment_statuses[experiment_id].metrics['memory_usage_mb'] == 100.0
        assert experiment_statuses[experiment_id].metrics['error_count'] == 0
        assert experiment_statuses[experiment_id].metrics['custom_metric'] == 'test value'
