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
            # TODO: Ensure 'server_root_ca.pem' is available in a known location.
            # This file is necessary for the client to verify the server's SSL certificate.
            # It should be provisioned securely to the agent's environment.
            # For now, we assume it's in the 'agent_core' directory alongside db_client.py or a configured path.
            # A more robust solution might involve a configuration setting for the cert path.
            cert_path = os.path.join(os.path.dirname(__file__), 'server_root_ca.pem') # Assumes cert is in the same dir

            try:
                with open(cert_path, 'rb') as f:
                    root_certs = f.read()
            except FileNotFoundError:
                logger.error(f"Server root CA certificate ({cert_path}) not found. Cannot create secure gRPC channel.")
                self.connected = False
                return False
            
            credentials = grpc.ssl_channel_credentials(root_certificates=root_certs)
            self.channel = grpc.secure_channel(self.backend_address, credentials)
            logger.info(f"Attempting to establish secure gRPC connection to {self.backend_address}")

            # Create database sync stub
            self.db_sync_stub = database_sync_pb2_grpc.DatabaseSyncServiceStub(self.channel)

            # Set connected flag
            self.connected = True

            # Test connection (optional, but good for immediate feedback)
            # You might need a simple health check RPC method on the server
            # For now, we assume connection is successful if channel is created.
            logger.info(f"Secure gRPC channel created. Connected to Backend gRPC service at {self.backend_address}")
            return True
        except grpc.RpcError as rpc_error: # More specific gRPC error
            logger.error(f"Failed to connect to Backend gRPC service via secure channel: {rpc_error}")
            # Example: check for specific statuses like UNAVAILABLE if server is down or cert issue
            if hasattr(rpc_error, 'code') and rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                 logger.error("Service unavailable. Ensure the backend gRPC server is running and accessible, and SSL/TLS settings match.")
            elif hasattr(rpc_error, 'code') and rpc_error.code() == grpc.StatusCode.INTERNAL and "ssl" in str(rpc_error.details()).lower():
                 logger.error("SSL handshake failed. Check server_root_ca.pem and server certificates.")

            self.connected = False
            return False
        except Exception as e: # Catch other potential errors during channel creation
            logger.error(f"An unexpected error occurred while creating secure gRPC channel: {e}")
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
