"""
Pytest configuration file for Agent Core tests.
"""

import os
import sys
import pytest
import grpc
from unittest.mock import MagicMock
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
import uuid

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables for testing
os.environ['AGENT_CORE_PORT'] = '50051'
os.environ['BACKEND_HOST'] = 'localhost'
os.environ['BACKEND_GRPC_PORT'] = '50052'
os.environ['DB_SYNC_ENABLED'] = 'false'

# Mock the gRPC modules
sys.modules['agent_pb2'] = MagicMock()
sys.modules['agent_pb2_grpc'] = MagicMock()
sys.modules['database_sync_pb2'] = MagicMock()
sys.modules['database_sync_pb2_grpc'] = MagicMock()

# Import the modules to test
from main import AgentServiceServicer, experiment_statuses, running_tasks
from db_client import BackendDBClient

@pytest.fixture
def reset_experiment_statuses():
    """Reset the experiment_statuses dictionary before each test."""
    experiment_statuses.clear()
    running_tasks.clear()
    yield
    experiment_statuses.clear()
    running_tasks.clear()

@pytest.fixture
def mock_experiment_status():
    """Create a mock experiment status."""
    experiment_id = str(uuid.uuid4())
    
    # Create a timestamp for the current time
    current_time = Timestamp()
    current_time.GetCurrentTime()
    
    # Create a metrics struct
    metrics = Struct()
    metrics.update({
        'progress_percent': 0.0,
        'elapsed_time_seconds': 0.0,
        'estimated_remaining_seconds': 0.0,
        'cpu_usage_percent': 0.0,
        'memory_usage_mb': 0.0,
        'error_count': 0
    })
    
    # Create a parameters struct
    parameters = Struct()
    parameters.update({
        'topic': 'Test Topic',
        'target_audience': 'Test Audience',
        'length': '1000 words'
    })
    
    # Create a definition struct
    definition = MagicMock()
    definition.type = 'AI_DRIVEN_EBOOKS'
    definition.name = 'Test Experiment'
    definition.description = 'A test experiment'
    definition.parameters = parameters
    
    # Create an experiment status
    status = MagicMock()
    status.id.id = experiment_id
    status.name = 'Test Experiment'
    status.type = 'AI_DRIVEN_EBOOKS'
    status.state = 'STATE_DEFINED'
    status.status_message = 'Experiment defined'
    status.metrics = metrics
    status.start_time = None
    status.last_update_time = current_time
    status.estimated_completion_time = None
    status.definition = definition
    
    return status

@pytest.fixture
def agent_service():
    """Create an instance of the AgentServiceServicer."""
    return AgentServiceServicer()

@pytest.fixture
def mock_context():
    """Create a mock gRPC context."""
    context = MagicMock()
    return context

@pytest.fixture
def mock_db_client():
    """Create a mock database client."""
    client = MagicMock(spec=BackendDBClient)
    client.connected = True
    client.restore_experiments.return_value = []
    client.sync_experiment_status.return_value = True
    client.sync_log_entry.return_value = True
    client.sync_metrics.return_value = True
    return client

@pytest.fixture
def mock_task_module():
    """Create a mock task module."""
    task_module = MagicMock()
    task_module.execute.return_value = {
        'success': True,
        'message': 'Task executed successfully',
        'results': {
            'output': 'Test output'
        }
    }
    return task_module
