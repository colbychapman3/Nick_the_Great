import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import uuid
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from db_client import BackendDBClient

# Mock the gRPC modules
sys.modules['agent_pb2'] = MagicMock()
sys.modules['database_sync_pb2'] = MagicMock()
sys.modules['database_sync_pb2_grpc'] = MagicMock()

class TestDatabaseSync(unittest.TestCase):
    """Test the database synchronization functionality"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a mock gRPC channel
        self.mock_channel = MagicMock()
        
        # Create a mock gRPC stub
        self.mock_stub = MagicMock()
        
        # Create a mock experiment status
        self.mock_experiment_status = MagicMock()
        self.mock_experiment_status.id.id = str(uuid.uuid4())
        
        # Create a mock log entry
        self.mock_log_entry = MagicMock()
        self.mock_log_entry.experiment_id.id = self.mock_experiment_status.id.id
        
        # Create a mock metrics struct
        self.mock_metrics = Struct()
        self.mock_metrics.update({
            'progress_percent': 50.0,
            'elapsed_time_seconds': 300.0,
            'estimated_remaining_seconds': 300.0,
            'cpu_usage_percent': 25.0,
            'memory_usage_mb': 100.0,
            'error_count': 0
        })
        
        # Create a mock timestamp
        self.mock_timestamp = Timestamp()
        self.mock_timestamp.GetCurrentTime()
        
        # Create a mock response
        self.mock_response = MagicMock()
        self.mock_response.success = True
        self.mock_response.message = "Success"
        
        # Patch the grpc.insecure_channel function
        self.patch_channel = patch('grpc.insecure_channel', return_value=self.mock_channel)
        self.mock_grpc_channel = self.patch_channel.start()
        
        # Patch the DatabaseSyncServiceStub constructor
        self.patch_stub = patch('database_sync_pb2_grpc.DatabaseSyncServiceStub', return_value=self.mock_stub)
        self.mock_grpc_stub = self.patch_stub.start()
        
        # Create the client
        self.client = BackendDBClient()
        
        # Set up the mock stub methods
        self.mock_stub.RestoreExperiments.return_value = MagicMock(
            success=True,
            message="Restored experiments",
            experiments=[self.mock_experiment_status]
        )
        self.mock_stub.SyncExperimentStatus.return_value = MagicMock(
            success=True,
            message="Synced experiment status"
        )
        self.mock_stub.SyncLogEntry.return_value = MagicMock(
            success=True,
            message="Synced log entry"
        )
        self.mock_stub.SyncMetrics.return_value = MagicMock(
            success=True,
            message="Synced metrics"
        )
    
    def tearDown(self):
        """Clean up after the test"""
        # Stop the patches
        self.patch_channel.stop()
        self.patch_stub.stop()
    
    def test_connect(self):
        """Test the connect method"""
        # The client should already be connected from setUp
        self.assertTrue(self.client.connected)
        
        # Test reconnecting
        self.client.connected = False
        result = self.client.connect()
        self.assertTrue(result)
        self.assertTrue(self.client.connected)
        
        # Test connection failure
        self.mock_grpc_channel.side_effect = Exception("Connection failed")
        self.client.connected = False
        result = self.client.connect()
        self.assertFalse(result)
        self.assertFalse(self.client.connected)
        
        # Reset the side effect
        self.mock_grpc_channel.side_effect = None
    
    def test_restore_experiments(self):
        """Test the restore_experiments method"""
        # Test successful restoration
        experiments = self.client.restore_experiments()
        self.assertEqual(len(experiments), 1)
        self.assertEqual(experiments[0], self.mock_experiment_status)
        
        # Test failed restoration
        self.mock_stub.RestoreExperiments.return_value = MagicMock(
            success=False,
            message="Failed to restore experiments",
            experiments=[]
        )
        experiments = self.client.restore_experiments()
        self.assertIsNone(experiments)
        
        # Test exception
        self.mock_stub.RestoreExperiments.side_effect = Exception("Restoration failed")
        experiments = self.client.restore_experiments()
        self.assertIsNone(experiments)
        
        # Reset the side effect
        self.mock_stub.RestoreExperiments.side_effect = None
    
    def test_sync_experiment_status(self):
        """Test the sync_experiment_status method"""
        # Test successful sync
        result = self.client.sync_experiment_status(self.mock_experiment_status)
        self.assertTrue(result)
        
        # Test failed sync
        self.mock_stub.SyncExperimentStatus.return_value = MagicMock(
            success=False,
            message="Failed to sync experiment status"
        )
        result = self.client.sync_experiment_status(self.mock_experiment_status)
        self.assertFalse(result)
        
        # Test exception
        self.mock_stub.SyncExperimentStatus.side_effect = Exception("Sync failed")
        result = self.client.sync_experiment_status(self.mock_experiment_status)
        self.assertFalse(result)
        
        # Reset the side effect
        self.mock_stub.SyncExperimentStatus.side_effect = None
    
    def test_sync_log_entry(self):
        """Test the sync_log_entry method"""
        # Test successful sync
        result = self.client.sync_log_entry(self.mock_log_entry)
        self.assertTrue(result)
        
        # Test failed sync
        self.mock_stub.SyncLogEntry.return_value = MagicMock(
            success=False,
            message="Failed to sync log entry"
        )
        result = self.client.sync_log_entry(self.mock_log_entry)
        self.assertFalse(result)
        
        # Test exception
        self.mock_stub.SyncLogEntry.side_effect = Exception("Sync failed")
        result = self.client.sync_log_entry(self.mock_log_entry)
        self.assertFalse(result)
        
        # Reset the side effect
        self.mock_stub.SyncLogEntry.side_effect = None
    
    def test_sync_metrics(self):
        """Test the sync_metrics method"""
        # Test successful sync
        result = self.client.sync_metrics(self.mock_experiment_status.id.id, self.mock_metrics)
        self.assertTrue(result)
        
        # Test failed sync
        self.mock_stub.SyncMetrics.return_value = MagicMock(
            success=False,
            message="Failed to sync metrics"
        )
        result = self.client.sync_metrics(self.mock_experiment_status.id.id, self.mock_metrics)
        self.assertFalse(result)
        
        # Test exception
        self.mock_stub.SyncMetrics.side_effect = Exception("Sync failed")
        result = self.client.sync_metrics(self.mock_experiment_status.id.id, self.mock_metrics)
        self.assertFalse(result)
        
        # Reset the side effect
        self.mock_stub.SyncMetrics.side_effect = None
    
    def test_close(self):
        """Test the close method"""
        # Test closing the channel
        self.client.close()
        self.assertFalse(self.client.connected)
        self.mock_channel.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
