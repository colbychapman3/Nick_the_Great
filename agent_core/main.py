import grpc
import time
import os
import uuid
from concurrent import futures
import logging
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2
from google.protobuf.struct_pb2 import Struct # Import Struct
import threading # Import threading for running tasks in background

# Load environment variables from .env file
load_dotenv()

# Import generated gRPC code
from . import agent_pb2
from . import agent_pb2_grpc

# Import task modules
from task_modules.ebook_generator import EbookGeneratorTask
# TODO: Import other task modules as they are developed

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# In-memory storage for experiment statuses (for initial stub)
# TODO: Replace with persistent storage (e.g., connect to MongoDB via backend)
experiment_statuses = {}

# Thread pool for executing tasks
task_executor = futures.ThreadPoolExecutor(max_workers=5) # Use a small pool for tasks

# TODO: Initialize gRPC client for backend communication (for status updates)
# BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost")
# BACKEND_PORT = os.getenv("BACKEND_PORT", "10000") # Default backend port
# backend_channel = grpc.insecure_channel(f"{BACKEND_HOST}:{BACKEND_PORT}") # TODO: Use secure channel for production
# backend_stub = agent_pb2_grpc.BackendServiceStub(backend_channel) # Assuming a BackendService in proto

# Define the AgentServiceServicer
class AgentServiceServicer(agent_pb2_grpc.AgentServiceServicer):
    def CreateExperiment(self, request, context):
        logger.info(f"Received CreateExperiment request: {request}")
        # Generate a unique ID for the experiment
        experiment_id = str(uuid.uuid4())

        # Store initial experiment status, including the definition
        experiment_statuses[experiment_id] = agent_pb2.ExperimentStatus(
            id=agent_pb2.ExperimentId(id=experiment_id),
            name=request.definition.name,
            type=request.definition.type,
            state=agent_pb2.ExperimentState.STATE_DEFINED,
            status_message="Experiment defined",
            metrics=None, # Initialize metrics as None or empty Struct
            start_time=None,
            last_update_time=None,
            estimated_completion_time=None,
            # Store the original definition with the status
            definition=request.definition
        )
        logger.info(f"Created experiment with ID: {experiment_id}")
        # TODO: Persist experiment status to backend/DB via gRPC client

        return agent_pb2.CreateExperimentResponse(
            id=agent_pb2.ExperimentId(id=experiment_id),
            status=agent_pb2.StatusResponse(success=True, message="Experiment created successfully")
        )

    def StartExperiment(self, request, context):
        logger.info(f"Received StartExperiment request: {request}")
        experiment_id = request.id.id

        if experiment_id not in experiment_statuses:
            logger.warning(f"Attempted to start non-existent experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} not found")

        status = experiment_statuses[experiment_id]
        if status.state == agent_pb2.ExperimentState.STATE_RUNNING:
            logger.warning(f"Attempted to start already running experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} is already running")

        # Update status to running
        status.state = agent_pb2.ExperimentState.STATE_RUNNING
        status.status_message = "Starting experiment..."
        status.start_time.CopyFrom(timestamp_pb2.Timestamp(seconds=int(time.time())))
        status.last_update_time.CopyFrom(timestamp_pb2.Timestamp(seconds=int(time.time())))
        logger.info(f"Starting experiment: {experiment_id}")
        # TODO: Persist status change to backend/DB via gRPC client

        # Submit task execution to the thread pool
        task_type = status.type
        task_parameters = status.definition.parameters

        task_instance = None
        if task_type == agent_pb2.ExperimentType.AI_DRIVEN_EBOOKS:
            task_instance = EbookGeneratorTask()
            status.status_message = "Ebook generation task submitted to executor"
            logger.info(f"Ebook generation task submitted for experiment {experiment_id}")
            future = task_executor.submit(task_instance.execute, task_parameters)
            future.add_done_callback(lambda f: self._handle_task_completion(experiment_id, f))
        # TODO: Add elif blocks for other experiment types and their corresponding task modules
        # elif task_type == agent_pb2.ExperimentType.FREELANCE_WRITING:
        #     task_instance = FreelanceWritingTask()
        #     status.status_message = "Freelance writing task submitted to executor"
        #     logger.info(f"Freelance writing task submitted for experiment {experiment_id}")
        else:
            status.status_message = f"Unknown experiment type: {task_type}. Cannot start task."
            status.state = agent_pb2.ExperimentState.STATE_FAILED
            logger.error(status.status_message)
            # No task submitted, update status immediately
            status.last_update_time.CopyFrom(timestamp_pb2.Timestamp(seconds=int(time.time())))
            # TODO: Notify backend of status change


        return agent_pb2.StatusResponse(success=True, message=f"Experiment {experiment_id} started")

    def _handle_task_completion(self, experiment_id, future):
        """
        Callback function to handle the result of a completed task.
        Updates the experiment status based on the task result and notifies the backend.
        """
        logger.info(f"Task completed for experiment {experiment_id}")
        status = experiment_statuses.get(experiment_id)
        if not status:
            logger.error(f"Experiment status not found for completed task: {experiment_id}")
            return

        try:
            task_result = future.result() # Get the result or raise exception
            logger.info(f"Task result for {experiment_id}: {task_result}")

            # Update status based on task_result structure (assuming dict with 'status' and 'result'/'message')
            if task_result.get("status") == "completed":
                status.state = agent_pb2.ExperimentState.STATE_COMPLETED
                status.status_message = "Task completed successfully"
                # TODO: Store task_result.get("result") persistently (via backend)
            else: # Assuming "failed" status or exception
                status.state = agent_pb2.ExperimentState.STATE_FAILED
                status.status_message = task_result.get("message", "Task failed")
                logger.error(f"Task failed for experiment {experiment_id}: {status.status_message}")

        except Exception as e:
            logger.error(f"Task execution failed for experiment {experiment_id}: {e}")
            status.state = agent_pb2.ExperimentState.STATE_FAILED
            status.status_message = f"Task execution failed: {e}"
        finally:
            status.last_update_time.CopyFrom(timestamp_pb2.Timestamp(seconds=int(time.time())))
            logger.info(f"Experiment {experiment_id} status updated to {status.state}")
            # TODO: Notify backend of status change via gRPC client

    def StopExperiment(self, request, context):
        logger.info(f"Received StopExperiment request: {request}")
        experiment_id = request.id.id

        if experiment_id not in experiment_statuses:
            logger.warning(f"Attempted to stop non-existent experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} not found")

        status = experiment_statuses[experiment_id]
        if status.state in [agent_pb2.ExperimentState.STATE_COMPLETED, agent_pb2.ExperimentState.STATE_FAILED, agent_pb2.ExperimentState.STATE_STOPPED]:
            logger.warning(f"Attempted to stop experiment that is not running: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message="Experiment with ID {experiment_id} is not running")

        # Update status to stopped
        status.state = agent_pb2.ExperimentState.STATE_STOPPED
        status.status_message = "Experiment stopped manually"
        status.last_update_time.CopyFrom(timestamp_pb2.Timestamp(seconds=int(time.time())))
        logger.info(f"Stopped experiment: {experiment_id}")

        # TODO: Implement logic to actually stop the running task in the executor
        # This might involve cancelling the future if the task supports it

        # TODO: Notify backend of status change via gRPC client

        return agent_pb2.StatusResponse(success=True, message="Experiment {experiment_id} stopped")

    def GetExperimentStatus(self, request, context):
        logger.info(f"Received GetExperimentStatus request: {request}")
        experiment_id = request.id.id

        if experiment_id not in experiment_statuses:
            logger.warning(f"Attempted to get status for non-existent experiment: {experiment_id}")
            # Return a default or error status
            return agent_pb2.ExperimentStatus(
                id=request.id,
                name="Not Found",
                type=agent_pb2.ExperimentType.TYPE_UNSPECIFIED,
                state=agent_pb2.ExperimentState.STATE_UNSPECIFIED,
                status_message=f"Experiment with ID {experiment_id} not found"
            )

        # Return the current status
        return experiment_statuses[experiment_id]

    def GetAgentStatus(self, request, context):
        logger.info(f"Received GetAgentStatus request: {request}")
        # Calculate active experiments
        active_count = sum(1 for status in experiment_statuses.values() if status.state == agent_pb2.ExperimentState.STATE_RUNNING)

        # TODO: Implement actual CPU/Memory usage monitoring
        cpu_usage = 0.0
        memory_usage = 0.0

        # Determine overall agent state
        agent_state = "IDLE"
        if active_count > 0:
            agent_state = "RUNNING_EXPERIMENTS"
        # TODO: Add state for AWAITING_APPROVAL

        return agent_pb2.AgentStatus(
            agent_state=agent_state,
            active_experiments=active_count,
            cpu_usage_percent=cpu_usage,
            memory_usage_mb=memory_usage,
            last_updated=timestamp_pb2.Timestamp(seconds=int(time.time()))
        )

    def GetLogs(self, request, context):
        logger.info(f"Received GetLogs request")
        # TODO: Implement server-streaming logs logic
        # This would involve capturing logs and yielding LogEntry messages
        # based on the request filters (experiment_id, minimum_level)
        # For now, this is a stub and won't yield anything.
        pass

    def ApproveDecision(self, request, context):
        logger.info(f"Received ApproveDecision request: {request}")
        # TODO: Implement approve decision logic based on autonomy framework
        return agent_pb2.StatusResponse(success=True, message="Approve decision stub")

    def StopAgent(self, request, context):
        logger.info(f"Received StopAgent request")
        # TODO: Implement stop all agent activities (kill switch)
        # This would involve stopping all running tasks and changing overall agent state
        logger.info("Agent stop requested. Implementing kill switch...")
        # For now, just log and return success
        return agent_pb2.StatusResponse(success=True, message="Agent stop initiated")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServiceServicer(), server)

    port = os.getenv("AGENT_CORE_PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Agent Core Service starting on port {port}")
    server.start()
    try:
        while True:
            time.sleep(86400) # Server stays alive for 24 hours
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    # Need to import uuid and timestamp_pb2 here for the stubbed implementation
    import uuid
    from google.protobuf import timestamp_pb2
    serve()
