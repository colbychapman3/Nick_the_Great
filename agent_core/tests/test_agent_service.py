"""
Unit tests for the Agent Core Service.
"""

import pytest
import uuid
from unittest.mock import MagicMock, patch
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Import the modules to test
from main import AgentServiceServicer, experiment_statuses, running_tasks

class TestAgentService:
    """Test the Agent Core Service."""
    
    def test_create_experiment(self, agent_service, mock_context, reset_experiment_statuses):
        """Test creating an experiment."""
        # Arrange
        request = MagicMock()
        request.definition.type = 'AI_DRIVEN_EBOOKS'
        request.definition.name = 'Test Experiment'
        request.definition.description = 'A test experiment'
        request.definition.parameters = Struct()
        
        # Act
        response = agent_service.CreateExperiment(request, mock_context)
        
        # Assert
        assert response is not None
        assert response.status.success is True
        assert response.id is not None
        assert response.id.id in experiment_statuses
        
        # Verify the experiment was created correctly
        experiment = experiment_statuses[response.id.id]
        assert experiment.name == 'Test Experiment'
        assert experiment.type == 'AI_DRIVEN_EBOOKS'
        assert experiment.state == 'STATE_DEFINED'
    
    def test_start_experiment(self, agent_service, mock_context, mock_experiment_status, reset_experiment_statuses):
        """Test starting an experiment."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        request = MagicMock()
        request.id.id = experiment_id
        
        # Mock the task execution
        with patch('main.task_executor.submit') as mock_submit:
            mock_future = MagicMock()
            mock_submit.return_value = mock_future
            
            # Act
            response = agent_service.StartExperiment(request, mock_context)
            
            # Assert
            assert response is not None
            assert response.success is True
            assert experiment_statuses[experiment_id].state == 'STATE_RUNNING'
            assert experiment_id in running_tasks
            assert running_tasks[experiment_id] == mock_future
            
            # Verify the task was submitted
            mock_submit.assert_called_once()
    
    def test_stop_experiment(self, agent_service, mock_context, mock_experiment_status, reset_experiment_statuses):
        """Test stopping an experiment."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        mock_experiment_status.state = 'STATE_RUNNING'
        experiment_statuses[experiment_id] = mock_experiment_status
        
        # Create a mock future
        mock_future = MagicMock()
        mock_future.done.return_value = False
        mock_future.cancel.return_value = True
        running_tasks[experiment_id] = mock_future
        
        request = MagicMock()
        request.id.id = experiment_id
        
        # Act
        response = agent_service.StopExperiment(request, mock_context)
        
        # Assert
        assert response is not None
        assert response.success is True
        assert experiment_statuses[experiment_id].state == 'STATE_STOPPED'
        assert experiment_id not in running_tasks
        
        # Verify the future was cancelled
        mock_future.cancel.assert_called_once()
    
    def test_get_experiment_status(self, agent_service, mock_context, mock_experiment_status, reset_experiment_statuses):
        """Test getting experiment status."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        request = MagicMock()
        request.id = experiment_id
        
        # Act
        response = agent_service.GetExperimentStatus(request, mock_context)
        
        # Assert
        assert response is not None
        assert response.id.id == experiment_id
        assert response.name == mock_experiment_status.name
        assert response.type == mock_experiment_status.type
        assert response.state == mock_experiment_status.state
    
    def test_list_experiments(self, agent_service, mock_context, mock_experiment_status, reset_experiment_statuses):
        """Test listing experiments."""
        # Arrange
        experiment_id = mock_experiment_status.id.id
        experiment_statuses[experiment_id] = mock_experiment_status
        
        # Create a second experiment
        second_experiment = MagicMock()
        second_experiment.id.id = str(uuid.uuid4())
        second_experiment.name = 'Second Experiment'
        second_experiment.type = 'PINTEREST_STRATEGY'
        second_experiment.state = 'STATE_COMPLETED'
        experiment_statuses[second_experiment.id.id] = second_experiment
        
        request = MagicMock()
        
        # Act
        response = agent_service.ListExperiments(request, mock_context)
        
        # Assert
        assert response is not None
        assert len(response) == 2
        
        # Verify both experiments are in the response
        experiment_ids = [exp.id.id for exp in response]
        assert experiment_id in experiment_ids
        assert second_experiment.id.id in experiment_ids
    
    def test_get_agent_status(self, agent_service, mock_context):
        """Test getting agent status."""
        # Arrange
        request = MagicMock()
        
        # Act
        response = agent_service.GetAgentStatus(request, mock_context)
        
        # Assert
        assert response is not None
        assert response.status == 'RUNNING'
        assert response.version is not None
        assert response.uptime_seconds >= 0
        assert response.experiment_count >= 0
