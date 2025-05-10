"""
Unit tests for the Database Client.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import grpc
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from db_client import BackendDBClient

class TestBackendDBClient:
    """Test the BackendDBClient class."""
    
    def setup_method(self):
        """Set up the test environment."""
        # Mock the gRPC channel and stub
        self.mock_channel = MagicMock()
        self.mock_stub = MagicMock()
        
        # Patch the grpc.insecure_channel function
        self.patch_channel = patch('grpc.insecure_channel', return_value=self.mock_channel)
        self.mock_grpc_channel = self.patch_channel.start()
        
        # Patch the DatabaseSyncServiceStub constructor
        self.patch_stub = patch('database_sync_pb2_grpc.DatabaseSyncServiceStub', return_value=self.mock_stub)
        self.mock_grpc_stub = self.patch_stub.start()
        
        # Set environment variables
        os.environ['BACKEND_HOST'] = 'localhost'
        os.environ['BACKEND_GRPC_PORT'] = '50052'
        
        # Create the client
        self.client = BackendDBClient()
    
    def teardown_method(self):
        """Clean up after the test."""
        # Stop the patches
        self.patch_channel.stop()
        self.patch_stub.stop()
        
        # Remove environment variables
        if 'BACKEND_HOST' in os.environ:
            del os.environ['BACKEND_HOST']
        if 'BACKEND_GRPC_PORT' in os.environ:
            del os.environ['BACKEND_GRPC_PORT']
    
    def test_init(self):
        """Test the initialization of the client."""
        assert self.client.host == 'localhost'
        assert self.client.port == '50052'
        assert self.client.channel == self.mock_channel
        assert self.client.stub == self.mock_stub
        assert self.client.connected is True
    
    def test_connect_success(self):
        """Test successful connection."""
        # Arrange
        self.client.connected = False
        
        # Act
        result = self.client.connect()
        
        # Assert
        assert result is True
        assert self.client.connected is True
        self.mock_grpc_channel.assert_called_once_with('localhost:50052')
        self.mock_grpc_stub.assert_called_once_with(self.mock_channel)
    
    def test_connect_failure(self):
        """Test connection failure."""
        # Arrange
        self.client.connected = False
        self.mock_grpc_channel.side_effect = Exception("Connection failed")
        
        # Act
        result = self.client.connect()
        
        # Assert
        assert result is False
        assert self.client.connected is False
    
    def test_restore_experiments_success(self):
        """Test successful restoration of experiments."""
        # Arrange
        mock_experiment = MagicMock()
        self.mock_stub.RestoreExperiments.return_value = MagicMock(
            success=True,
            message="Restored experiments",
            experiments=[mock_experiment]
        )
        
        # Act
        experiments = self.client.restore_experiments()
        
        # Assert
        assert experiments == [mock_experiment]
        self.mock_stub.RestoreExperiments.assert_called_once()
    
    def test_restore_experiments_failure(self):
        """Test failed restoration of experiments."""
        # Arrange
        self.mock_stub.RestoreExperiments.return_value = MagicMock(
            success=False,
            message="Failed to restore experiments",
            experiments=[]
        )
        
        # Act
        experiments = self.client.restore_experiments()
        
        # Assert
        assert experiments is None
        self.mock_stub.RestoreExperiments.assert_called_once()
    
    def test_restore_experiments_exception(self):
        """Test exception during restoration of experiments."""
        # Arrange
        self.mock_stub.RestoreExperiments.side_effect = Exception("Restoration failed")
        
        # Act
        experiments = self.client.restore_experiments()
        
        # Assert
        assert experiments is None
        self.mock_stub.RestoreExperiments.assert_called_once()
    
    def test_sync_experiment_status_success(self):
        """Test successful synchronization of experiment status."""
        # Arrange
        mock_experiment = MagicMock()
        self.mock_stub.SyncExperimentStatus.return_value = MagicMock(
            success=True,
            message="Synced experiment status"
        )
        
        # Act
        result = self.client.sync_experiment_status(mock_experiment)
        
        # Assert
        assert result is True
        self.mock_stub.SyncExperimentStatus.assert_called_once_with(mock_experiment)
    
    def test_sync_experiment_status_failure(self):
        """Test failed synchronization of experiment status."""
        # Arrange
        mock_experiment = MagicMock()
        self.mock_stub.SyncExperimentStatus.return_value = MagicMock(
            success=False,
            message="Failed to sync experiment status"
        )
        
        # Act
        result = self.client.sync_experiment_status(mock_experiment)
        
        # Assert
        assert result is False
        self.mock_stub.SyncExperimentStatus.assert_called_once_with(mock_experiment)
    
    def test_sync_experiment_status_exception(self):
        """Test exception during synchronization of experiment status."""
        # Arrange
        mock_experiment = MagicMock()
        self.mock_stub.SyncExperimentStatus.side_effect = Exception("Sync failed")
        
        # Act
        result = self.client.sync_experiment_status(mock_experiment)
        
        # Assert
        assert result is False
        self.mock_stub.SyncExperimentStatus.assert_called_once_with(mock_experiment)
    
    def test_sync_log_entry_success(self):
        """Test successful synchronization of log entry."""
        # Arrange
        mock_log_entry = MagicMock()
        self.mock_stub.SyncLogEntry.return_value = MagicMock(
            success=True,
            message="Synced log entry"
        )
        
        # Act
        result = self.client.sync_log_entry(mock_log_entry)
        
        # Assert
        assert result is True
        self.mock_stub.SyncLogEntry.assert_called_once_with(mock_log_entry)
    
    def test_sync_metrics_success(self):
        """Test successful synchronization of metrics."""
        # Arrange
        experiment_id = "test-experiment-id"
        metrics = Struct()
        metrics.update({"progress": 50.0})
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        
        self.mock_stub.SyncMetrics.return_value = MagicMock(
            success=True,
            message="Synced metrics"
        )
        
        # Act
        result = self.client.sync_metrics(experiment_id, metrics, timestamp)
        
        # Assert
        assert result is True
        self.mock_stub.SyncMetrics.assert_called_once()
        
        # Verify the correct parameters were passed
        call_args = self.mock_stub.SyncMetrics.call_args[0][0]
        assert call_args.experiment_id == experiment_id
        assert call_args.metrics == metrics
        assert call_args.timestamp == timestamp
    
    def test_close(self):
        """Test closing the client."""
        # Act
        self.client.close()
        
        # Assert
        assert self.client.connected is False
        self.mock_channel.close.assert_called_once()
