"""
Integration tests for the Agent Core and Backend API.
"""

import os
import sys
import pytest
import uuid
from unittest.mock import MagicMock, patch
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
import concurrent.futures

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from main import AgentServiceServicer, experiment_statuses, running_tasks, task_executor
from db_client import BackendDBClient

class TestAgentBackendIntegration:
    """Test the integration between the Agent Core and Backend API."""
    
    def setup_method(self):
        """Set up the test environment."""
        # Create an instance of the AgentServiceServicer
        self.agent_service = AgentServiceServicer()
        
        # Create a mock gRPC context
        self.mock_context = MagicMock()
        
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Set environment variables
        os.environ['ABACUSAI_API_KEY'] = 'test-api-key'
        os.environ['BACKEND_HOST'] = 'localhost'
        os.environ['BACKEND_GRPC_PORT'] = '50052'
        os.environ['DB_SYNC_ENABLED'] = 'true'
        
        # Mock the BackendDBClient
        self.mock_db_client = MagicMock(spec=BackendDBClient)
        self.mock_db_client.connected = True
        self.mock_db_client.sync_experiment.return_value = True
        self.mock_db_client.sync_log_entry.return_value = True
        self.mock_db_client.sync_metrics.return_value = True
        
        # Patch the db_client in the main module
        self.patch_db_client = patch('main.db_client', self.mock_db_client)
        self.mock_db_client_instance = self.patch_db_client.start()
    
    def teardown_method(self):
        """Clean up after the test."""
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Stop the patches
        self.patch_db_client.stop()
        
        # Remove environment variables
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
        if 'BACKEND_HOST' in os.environ:
            del os.environ['BACKEND_HOST']
        if 'BACKEND_GRPC_PORT' in os.environ:
            del os.environ['BACKEND_GRPC_PORT']
        if 'DB_SYNC_ENABLED' in os.environ:
            del os.environ['DB_SYNC_ENABLED']
    
    def test_create_experiment_syncs_to_backend(self):
        """Test that creating an experiment syncs the data to the backend."""
        # Arrange
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Test Experiment'
        create_request.definition.description = 'A test experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 5
        })
        create_request.definition.parameters = parameters
        
        # Act
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        
        # Assert
        assert create_response is not None
        assert create_response.status.success is True
        assert create_response.id is not None
        experiment_id = create_response.id.id
        assert experiment_id in experiment_statuses
        
        # Verify the experiment was synced to the backend
        self.mock_db_client.sync_experiment.assert_called_once()
        call_args = self.mock_db_client.sync_experiment.call_args[0]
        assert call_args[0] == experiment_id
    
    def test_update_metrics_syncs_to_backend(self):
        """Test that updating experiment metrics syncs the data to the backend."""
        # Arrange
        # Create an experiment
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Test Experiment'
        create_request.definition.description = 'A test experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 5
        })
        create_request.definition.parameters = parameters
        
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        experiment_id = create_response.id.id
        
        # Reset the mock to clear the call history
        self.mock_db_client.sync_metrics.reset_mock()
        
        # Create metrics
        metrics = Struct()
        metrics.update({
            'progress': 0.5,
            'chapters_completed': 2,
            'words_generated': 5000
        })
        
        # Act
        # Call the _update_experiment_metrics method directly
        self.agent_service._update_experiment_metrics(experiment_id, metrics)
        
        # Assert
        # Verify the metrics were synced to the backend
        self.mock_db_client.sync_metrics.assert_called_once()
        call_args = self.mock_db_client.sync_metrics.call_args[0]
        assert call_args[0] == experiment_id
        assert call_args[1] == metrics
    
    def test_log_entry_syncs_to_backend(self):
        """Test that adding a log entry syncs the data to the backend."""
        # Arrange
        # Create an experiment
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Test Experiment'
        create_request.definition.description = 'A test experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 5
        })
        create_request.definition.parameters = parameters
        
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        experiment_id = create_response.id.id
        
        # Reset the mock to clear the call history
        self.mock_db_client.sync_log_entry.reset_mock()
        
        # Act
        # Call the _add_log_entry method directly
        self.agent_service._add_log_entry(experiment_id, "Test log message", "INFO")
        
        # Assert
        # Verify the log entry was synced to the backend
        self.mock_db_client.sync_log_entry.assert_called_once()
        call_args = self.mock_db_client.sync_log_entry.call_args[0]
        assert call_args[0].experiment_id.id == experiment_id
        assert call_args[0].message == "Test log message"
        assert call_args[0].level == "INFO"
