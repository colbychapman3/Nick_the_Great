import os
import time
import logging
import grpc
import json
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Import the generated gRPC code
try:
    # Try to import from the generated directory first
    from agent_core.generated import agent_pb2
    from agent_core.generated import database_sync_pb2, database_sync_pb2_grpc
except ImportError:
    # Fall back to direct import (for backward compatibility)
    import agent_pb2
    # These imports will fail if the code hasn't been generated yet
    try:
        import database_sync_pb2
        import database_sync_pb2_grpc
    except ImportError:
        print("WARNING: database_sync_pb2 modules not found. Run generate_protos.sh first.")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

class BackendDBClient:
    """Client for communicating with the Backend API to sync experiment data"""

    def __init__(self):
        # Get Backend API address from environment variables
        self.backend_host = os.getenv('BACKEND_HOST', 'localhost')
        self.backend_grpc_port = os.getenv('BACKEND_GRPC_PORT', '50052')
        self.backend_address = f"{self.backend_host}:{self.backend_grpc_port}"

        # Create gRPC channel and stub
        self.channel = None
        self.db_sync_stub = None
        self.connected = False

        # Try to connect
        self.connect()

    def connect(self):
        """Connect to the Backend API"""
        try:
            # Create insecure channel (TODO: Use TLS for production)
            self.channel = grpc.insecure_channel(self.backend_address)

            # Create database sync stub
            self.db_sync_stub = database_sync_pb2_grpc.DatabaseSyncServiceStub(self.channel)

            # Set connected flag
            self.connected = True

            logger.info(f"Connected to Backend gRPC service at {self.backend_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Backend gRPC service: {e}")
            self.connected = False
            return False

    def restore_experiments(self):
        """Restore experiment data from the Backend API"""
        if not self.connected and not self.connect():
            logger.error("Cannot restore experiments: Not connected to Backend API")
            return None

        try:
            # Create request
            request = database_sync_pb2.RestoreExperimentsRequest(
                limit=100  # Limit to 100 experiments for initial load
            )

            # Call the Backend API
            response = self.db_sync_stub.RestoreExperiments(request)

            if not response.success:
                logger.error(f"Failed to restore experiments: {response.message}")
                return None

            logger.info(f"Restored {len(response.experiments)} experiments from Backend API")
            return response.experiments
        except Exception as e:
            logger.error(f"Error restoring experiments from Backend API: {e}")
            return None

    def sync_experiment_status(self, experiment_status):
        """Sync experiment status with the Backend API"""
        if not self.connected and not self.connect():
            logger.error("Cannot sync experiment status: Not connected to Backend API")
            return False

        try:
            # Create request
            request = database_sync_pb2.SyncExperimentStatusRequest(
                experiment_status=experiment_status
            )

            # Call the Backend API
            response = self.db_sync_stub.SyncExperimentStatus(request)

            if not response.success:
                logger.error(f"Failed to sync experiment status: {response.message}")
                return False

            logger.debug(f"Synced experiment status for {experiment_status.id.id}")
            return True
        except Exception as e:
            logger.error(f"Error syncing experiment status with Backend API: {e}")
            return False

    def sync_log_entry(self, log_entry):
        """Sync log entry with the Backend API"""
        if not self.connected and not self.connect():
            logger.error("Cannot sync log entry: Not connected to Backend API")
            return False

        try:
            # Create request
            request = database_sync_pb2.SyncLogEntryRequest(
                log_entry=log_entry
            )

            # Call the Backend API
            response = self.db_sync_stub.SyncLogEntry(request)

            if not response.success:
                logger.error(f"Failed to sync log entry: {response.message}")
                return False

            logger.debug(f"Synced log entry for experiment {log_entry.experiment_id.id}")
            return True
        except Exception as e:
            logger.error(f"Error syncing log entry with Backend API: {e}")
            return False

    def sync_metrics(self, experiment_id, metrics):
        """Sync metrics with the Backend API"""
        if not self.connected and not self.connect():
            logger.error("Cannot sync metrics: Not connected to Backend API")
            return False

        try:
            # Create timestamp
            timestamp = Timestamp()
            timestamp.GetCurrentTime()

            # Create request
            request = database_sync_pb2.SyncMetricsRequest(
                experiment_id=agent_pb2.ExperimentId(id=experiment_id),
                metrics=metrics,
                timestamp=timestamp
            )

            # Call the Backend API
            response = self.db_sync_stub.SyncMetrics(request)

            if not response.success:
                logger.error(f"Failed to sync metrics: {response.message}")
                return False

            logger.debug(f"Synced metrics for experiment {experiment_id}")
            return True
        except Exception as e:
            logger.error(f"Error syncing metrics with Backend API: {e}")
            return False

    def close(self):
        """Close the gRPC channel"""
        if self.channel:
            self.channel.close()
            self.connected = False
            logger.info("Closed connection to Backend API")

# Create a singleton instance
db_client = BackendDBClient()
