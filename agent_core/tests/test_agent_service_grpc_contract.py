import sys
import os
import pytest
from concurrent import futures
import grpc
import logging
import time # For GetAgentStatus response field check

# Ensure the generated protobuf modules are discoverable.
# This assumes the tests are run from a context where 'agent_core' is in PYTHONPATH.
# Adjust if your project structure or test execution environment is different.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# --- Attempt to use real protobuf modules ---
# This section tries to remove any mocks set up by conftest.py for these specific modules.
# This is crucial for contract testing against the actual gRPC interface.
MOCKED_MODULES_TO_REMOVE = ['agent_pb2', 'agent_pb2_grpc', 'database_sync_pb2', 'database_sync_pb2_grpc']
real_protos = {}
import_error_raised = None

for mod_name in MOCKED_MODULES_TO_REMOVE:
    if mod_name in sys.modules:
        # Check if it's a MagicMock or similar mock object
        if 'mock' in str(type(sys.modules[mod_name])).lower():
            logging.warning(f"Removing mocked module '{mod_name}' from sys.modules to import real proto.")
            del sys.modules[mod_name]
        else:
            # If it's already imported and not a mock, we can try to use it.
            # However, to be safe and ensure we get the one from the path,
            # we might still want to del and re-import if paths are tricky.
            # For now, assume if not a mock, it's the real one.
            logging.info(f"Module '{mod_name}' found in sys.modules and is not a mock. Attempting to use as is.")


# Now, try to import the real generated protobuf modules
try:
    import agent_pb2
    import agent_pb2_grpc
    # We might need other protos if AgentServiceServicer internally uses them upon instantiation
    # or if the tested methods interact with them.
    # For now, focusing on agent_pb2 and agent_pb2_grpc for the AgentService.
    real_protos['agent_pb2'] = agent_pb2
    real_protos['agent_pb2_grpc'] = agent_pb2_grpc
    PROTO_SUCCESS = True
    logging.info("Successfully imported real protobuf modules for gRPC contract tests.")
except ImportError as e:
    PROTO_SUCCESS = False
    import_error_raised = e
    logging.error(f"Failed to import real protobuf modules for gRPC contract tests: {e}. "
                  "Ensure protos are generated and PYTHONPATH is correct.")
    # Tests requiring these protos will be skipped if this fails.
# --- End of real protobuf module import attempt ---


# Conditional import of the servicer - only if real protos are available
if PROTO_SUCCESS:
    try:
        from agent_core.main import AgentServiceServicer
        # If AgentServiceServicer uses db_client globally, conftest.py should mock it.
        # If it takes db_client in __init__, we'd pass mock_db_client fixture.
        # Current AgentServiceServicer in main.py uses a global db_client,
        # which conftest.py mocks.
    except ImportError as e:
        logging.error(f"Failed to import AgentServiceServicer: {e}")
        AgentServiceServicer = None # Ensure tests demanding it are skipped
else:
    AgentServiceServicer = None


# Fixture to get a free TCP port
@pytest.fixture(scope="session")
def grpc_server_port():
    import socket
    from contextlib import closing
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

# Fixture to set up and tear down the gRPC server
@pytest.fixture(scope="session")
def grpc_server(grpc_server_port, mock_db_client): # mock_db_client from conftest.py
    if not PROTO_SUCCESS or AgentServiceServicer is None:
        pytest.skip(f"Skipping gRPC server setup due to protobuf import failure ({import_error_raised}) or AgentServiceServicer not loaded.")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Instantiate the actual servicer.
    # It implicitly uses the globally mocked db_client from conftest.py
    # and other globally mocked dependencies if any (e.g. autonomy_framework).
    servicer_instance = AgentServiceServicer()
    
    real_protos['agent_pb2_grpc'].add_AgentServiceServicer_to_server(servicer_instance, server)
    
    server.add_insecure_port(f'[::]:{grpc_server_port}')
    server.start()
    logging.info(f"gRPC test server started on port {grpc_server_port}")
    yield server
    logging.info("Stopping gRPC test server")
    server.stop(grace=0) # Use a grace period of 0 for immediate stop in tests

# Fixture to create a gRPC client stub
@pytest.fixture(scope="session")
def grpc_stub(grpc_server, grpc_server_port): # grpc_server fixture ensures server is running
    if not PROTO_SUCCESS:
        pytest.skip("Skipping gRPC stub creation due to protobuf import failure.")
        
    channel = grpc.insecure_channel(f'localhost:{grpc_server_port}')
    stub = real_protos['agent_pb2_grpc'].AgentServiceStub(channel)
    yield stub
    channel.close()


# --- Test Cases ---

@pytest.mark.skipif(not PROTO_SUCCESS or AgentServiceServicer is None, reason=f"Skipping due to protobuf/servicer import error: {import_error_raised}")
def test_get_agent_status_contract(grpc_stub):
    """Test the GetAgentStatus gRPC contract."""
    request = real_protos['agent_pb2'].GetAgentStatusRequest()
    try:
        response = grpc_stub.GetAgentStatus(request, timeout=5) # Added timeout
    except grpc.RpcError as e:
        pytest.fail(f"GetAgentStatus RPC failed: {e}")

    assert isinstance(response, real_protos['agent_pb2'].AgentStatus), "Response is not an AgentStatus message"
    assert hasattr(response, 'agent_state'), "AgentStatus response missing 'agent_state' field"
    assert isinstance(response.agent_state, str), "'agent_state' field is not a string"
    assert response.agent_state in ["IDLE", "RUNNING_EXPERIMENTS", "AWAITING_APPROVAL", "UNKNOWN_STATE"], "Unexpected agent_state value"
    
    assert hasattr(response, 'active_experiments'), "AgentStatus response missing 'active_experiments' field"
    assert isinstance(response.active_experiments, int), "'active_experiments' field is not an int"

    assert hasattr(response, 'last_updated'), "AgentStatus response missing 'last_updated' field"
    assert response.last_updated.seconds > 0 or response.last_updated.nanos >= 0, "last_updated timestamp seems invalid"


@pytest.mark.skipif(not PROTO_SUCCESS or AgentServiceServicer is None, reason=f"Skipping due to protobuf/servicer import error: {import_error_raised}")
def test_create_experiment_contract(grpc_stub, mock_db_client): # mock_db_client from conftest.py
    """Test the CreateExperiment gRPC contract."""
    definition = real_protos['agent_pb2'].ExperimentDefinition(
        name="Test Contract Experiment",
        type=real_protos['agent_pb2'].AgentTaskType.Value('AI_DRIVEN_EBOOKS'), # Use enum value from AgentTaskType
        description="A test experiment for gRPC contract.",
        # parameters Struct needs to be created correctly
    )
    # For parameters, google.protobuf.struct_pb2.Struct can be used
    # Example: definition.parameters.update({"key": "value"})
    # If parameters are required by your CreateExperiment logic, populate them.
    # For now, assuming it can be empty or None if not strictly required for the contract itself.

    request = real_protos['agent_pb2'].CreateExperimentRequest(definition=definition)

    try:
        response = grpc_stub.CreateExperiment(request, timeout=5) # Added timeout
    except grpc.RpcError as e:
        # More detailed error reporting for debugging
        details = e.details() if hasattr(e, 'details') else str(e)
        code = e.code().name if hasattr(e, 'code') and hasattr(e.code(), 'name') else "UNKNOWN"
        pytest.fail(f"CreateExperiment RPC failed with code {code}: {details}")

    assert isinstance(response, real_protos['agent_pb2'].CreateExperimentResponse), "Response is not a CreateExperimentResponse message"
    assert hasattr(response, 'status'), "CreateExperimentResponse missing 'status' field"
    assert response.status.success is True, f"CreateExperiment was not successful: {response.status.message}"
    
    assert hasattr(response, 'id'), "CreateExperimentResponse missing 'id' field"
    assert hasattr(response.id, 'id'), "ExperimentId missing 'id' field"
    assert isinstance(response.id.id, str), "Experiment ID is not a string"
    assert len(response.id.id) > 0, "Experiment ID is empty"

    # Verify that the mock_db_client was called as expected by the servicer
    # This confirms that the servicer is interacting with its dependencies.
    # The actual call depends on how AgentServiceServicer uses db_client.
    # Assuming it calls _sync_experiment_to_db which calls db_client.sync_experiment_status
    # after creating the experiment.
    # This part might need adjustment based on exact servicer logic.
    # For now, we'll assume the mock_db_client's methods are called.
    # If conftest.py correctly mocks the global db_client, this should work.
    # Check if the db_client (which is mocked) was called.
    # Example: mock_db_client.sync_experiment_status.assert_called_once() 
    # However, this requires the mock_db_client fixture to be a MagicMock instance
    # and for AgentServiceServicer to use it.
    # If using the global mock from conftest, we'd need to access that mock.
    # For now, this test focuses on contract, interaction test is secondary here.
    # If the setup in conftest.py correctly mocks the global `db_client` used by `AgentServiceServicer`,
    # then the call to `CreateExperiment` should proceed without error if `db_client` methods are called.
    # A more direct assertion would require access to that globally mocked `db_client`.
    # For now, success of the RPC call with mock_db_client injected is the primary check.
    # Let's assume conftest.py has a mock for the global db_client that AgentServiceServicer uses.
    # If `mock_db_client` fixture itself is that global mock, then we can assert on it.
    # Based on conftest.py, `mock_db_client` is a MagicMock instance.
    # We need to ensure AgentServiceServicer uses *this* instance.
    # The current setup of AgentServiceServicer uses a global `db_client`.
    # `conftest.py` replaces this global `db_client` with a `MagicMock`.
    # The `mock_db_client` fixture from `conftest.py` *is* that global mock.
    
    # So, we can assert that a method on it was called.
    # The `AgentServiceServicer.CreateExperiment` calls `self._sync_experiment_to_db`
    # which then calls `db_client.sync_experiment_status`.
    mock_db_client.sync_experiment_status.assert_called() 
    # We can be more specific if needed, e.g. assert_called_once_with(...)
    # For a contract test, just ensuring it was called (meaning no crashes) is a good start.

# TODO: Add more tests for other gRPC methods (StartExperiment, StopExperiment, GetExperimentStatus)
# ensuring to use real_protos['agent_pb2'] for request and response types.
# For methods that change state, ensure the mock_db_client is used and potentially assert calls on it.

# Note on `conftest.py` interaction:
# The attempt to remove mocked modules from `sys.modules` is experimental.
# If `conftest.py` performs its mocking at a very early stage or in a way that
# makes this difficult to override, these tests might still pick up mocks.
# The true test is whether `agent_pb2.GetAgentStatusRequest` (for example)
# refers to the actual generated class or a MagicMock. If it's a MagicMock,
# then the un-mocking attempt was not successful for the test execution context.
# The logging added should help indicate this.
# If `isinstance(response, real_protos['agent_pb2'].AgentStatus)` passes,
# it's a good sign we are working with real objects.

# A check to confirm if un-mocking worked (can be put in a test or fixture)
def test_unmocking_check():
    if not PROTO_SUCCESS:
        pytest.skip(f"Skipping unmocking check due to protobuf import failure: {import_error_raised}")
    
    assert 'mock' not in str(type(real_protos['agent_pb2'])).lower(), \
        f"agent_pb2 appears to still be a mock: {type(real_protos['agent_pb2'])}"
    assert 'mock' not in str(type(real_protos['agent_pb2_grpc'])).lower(), \
        f"agent_pb2_grpc appears to still be a mock: {type(real_protos['agent_pb2_grpc'])}"
    
    # Example: Check a specific type
    assert hasattr(real_protos['agent_pb2'], 'GetAgentStatusRequest'), \
        "Real agent_pb2 should have GetAgentStatusRequest attribute"
    
    # This check is more about the module itself rather than an instance
    request_instance = real_protos['agent_pb2'].GetAgentStatusRequest()
    assert 'mock' not in str(type(request_instance)).lower(), \
        f"Instance of GetAgentStatusRequest appears to be a mock: {type(request_instance)}"

    logging.info("Un-mocking check passed. Real proto modules seem to be in use.")
