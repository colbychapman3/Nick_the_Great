import grpc
import time
import os
import uuid
import psutil
from concurrent import futures
import logging
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2
from google.protobuf.struct_pb2 import Struct # Import Struct
import threading # Import threading for running tasks in background
import json

# Import autonomy framework
try:
    from agent_core.autonomy_framework import AutonomyFramework, DecisionCategory
except ImportError:
    try:
        from autonomy_framework import AutonomyFramework, DecisionCategory
    except ImportError:
        pass  # Will be imported later

# Load environment variables from .env file
load_dotenv()

# Import generated gRPC code
try:
    # Try to import from the generated directory first
    from agent_core.generated import agent_pb2, agent_pb2_grpc
    from agent_core.generated import database_sync_pb2, database_sync_pb2_grpc
except ImportError:
    # Fall back to direct import (for backward compatibility)
    from . import agent_pb2, agent_pb2_grpc

# Import task modules
try:
    from agent_core.task_modules.ebook_generator_task import EbookGeneratorTask
    from agent_core.task_modules.freelance_writing_task import FreelanceWritingTask
    from agent_core.task_modules.niche_affiliate_website_task import NicheAffiliateWebsiteTask
    from agent_core.task_modules.pinterest_strategy_task import PinterestStrategyTask
except ImportError:
    try:
        from task_modules.ebook_generator_task import EbookGeneratorTask
        from task_modules.freelance_writing_task import FreelanceWritingTask
        from task_modules.niche_affiliate_website_task import NicheAffiliateWebsiteTask
        from task_modules.pinterest_strategy_task import PinterestStrategyTask
    except ImportError:
        # Create mock task modules for testing
        class MockTask:
            def execute(self, parameters):
                return {"status": "completed", "result": "Mock task completed"}

        EbookGeneratorTask = MockTask
        FreelanceWritingTask = MockTask
        NicheAffiliateWebsiteTask = MockTask
        PinterestStrategyTask = MockTask

# Import autonomy framework
try:
    from agent_core.autonomy import AutonomyFramework, DecisionCategory, ApprovalLevel, ApprovalStatus
except ImportError:
    try:
        from autonomy import AutonomyFramework, DecisionCategory, ApprovalLevel, ApprovalStatus
    except ImportError:
        try:
            from .autonomy import AutonomyFramework, DecisionCategory, ApprovalLevel, ApprovalStatus
        except ImportError:
            pass  # Will be imported later

# Import database client for persistence
try:
    from agent_core.db_client import db_client
except ImportError:
    try:
        from db_client import db_client
    except ImportError:
        try:
            from .db_client import db_client
        except ImportError:
            # Create a mock db_client for testing
            class MockDBClient:
                def __init__(self):
                    self.connected = False

                def connect(self):
                    return False

                def restore_experiments(self):
                    return []

                def sync_experiment_status(self, status):
                    pass

                def sync_log_entry(self, log_entry):
                    pass

                def sync_metrics(self, experiment_id, metrics, timestamp):
                    pass

                def close(self):
                    pass

            db_client = MockDBClient()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# In-memory storage for experiment statuses
# This will be initialized from the database on startup
experiment_statuses = {}

# In-memory storage for running task futures (for cancellation)
running_tasks = {}

# Thread pool for executing tasks
task_executor = futures.ThreadPoolExecutor(max_workers=5) # Use a small pool for tasks

# Initialize autonomy framework
autonomy_framework = AutonomyFramework()

# Initialize database sync flag
db_sync_enabled = os.getenv('DB_SYNC_ENABLED', 'true').lower() == 'true'

# Initialize metrics tracking
def create_empty_metrics():
    """Create an empty metrics Struct for experiment initialization"""
    metrics = Struct()
    metrics.update({
        "progress_percent": 0.0,
        "elapsed_time_seconds": 0.0,
        "estimated_remaining_seconds": 0.0,
        "cpu_usage_percent": 0.0,
        "memory_usage_mb": 0.0,
        "error_count": 0
    })
    return metrics

def get_system_metrics():
    """Get current system metrics for the agent status"""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        return cpu_usage, memory_usage
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return 0.0, 0.0

# Function to restore experiments from database
def restore_experiments_from_db():
    """Restore experiment data from the database on startup"""
    if not db_sync_enabled:
        logger.info("Database sync is disabled, skipping experiment restoration")
        return

    try:
        logger.info("Attempting to restore experiments from database...")

        # Try to restore experiments from the database
        restored_experiments = db_client.restore_experiments()

        if not restored_experiments:
            logger.warning("No experiments restored from database")
            return

        # Add restored experiments to in-memory storage
        for experiment in restored_experiments:
            experiment_id = experiment.id.id
            experiment_statuses[experiment_id] = experiment
            logger.info(f"Restored experiment {experiment_id} from database")

        logger.info(f"Successfully restored {len(restored_experiments)} experiments from database")
    except Exception as e:
        logger.error(f"Error restoring experiments from database: {e}")

# Function to sync experiment status to database
def sync_experiment_to_db(experiment_id):
    """Sync experiment status to the database"""
    if not db_sync_enabled:
        return

    try:
        # Get experiment status
        status = experiment_statuses.get(experiment_id)
        if not status:
            logger.warning(f"Cannot sync experiment {experiment_id} to database: Status not found")
            return

        # Sync to database
        db_client.sync_experiment_status(status)
    except Exception as e:
        logger.error(f"Error syncing experiment {experiment_id} to database: {e}")

# Function to sync log entry to database
def sync_log_to_db(log_entry):
    """Sync log entry to the database"""
    if not db_sync_enabled:
        return

    try:
        # Sync to database
        db_client.sync_log_entry(log_entry)
    except Exception as e:
        logger.error(f"Error syncing log entry to database: {e}")

# Restore experiments on startup
restore_experiments_from_db()

# Define the AgentServiceServicer
class AgentServiceServicer(agent_pb2_grpc.AgentServiceServicer):
    def CreateExperiment(self, request, context):
        logger.info(f"Received CreateExperiment request: {request}")

        # Check if the experiment type is valid using the autonomy framework
        experiment_type = request.definition.type
        experiment_name = request.definition.name

        # Generate a unique ID for the experiment
        experiment_id = str(uuid.uuid4())

        # Initialize metrics
        metrics = create_empty_metrics()

        # Get current timestamp
        current_time = timestamp_pb2.Timestamp(seconds=int(time.time()))

        # Create experiment status object
        experiment_status = agent_pb2.ExperimentStatus(
            id=agent_pb2.ExperimentId(id=experiment_id),
            name=experiment_name,
            type=experiment_type,
            state=agent_pb2.ExperimentState.STATE_DEFINED,
            status_message="Experiment defined",
            metrics=metrics,
            start_time=None,
            last_update_time=current_time,
            estimated_completion_time=None,
            definition=request.definition
        )

        # Store in memory
        experiment_statuses[experiment_id] = experiment_status

        logger.info(f"Created experiment with ID: {experiment_id}, type: {experiment_type}, name: {experiment_name}")

        # Sync to database
        sync_experiment_to_db(experiment_id)

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

        # Check if experiment is already running
        if status.state == agent_pb2.ExperimentState.STATE_RUNNING:
            logger.warning(f"Attempted to start already running experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} is already running")

        # Check if experiment is in a terminal state
        if status.state in [agent_pb2.ExperimentState.STATE_COMPLETED, agent_pb2.ExperimentState.STATE_FAILED]:
            logger.warning(f"Attempted to start completed/failed experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} is already completed or failed")

        # Check with autonomy framework if we can start this experiment
        can_execute, reason = autonomy_framework.can_execute(
            DecisionCategory.EXPERIMENT_MANAGEMENT,
            "start_experiment",
            {"experiment_id": experiment_id, "experiment_type": status.type}
        )

        if not can_execute:
            logger.info(f"Autonomy framework requires approval to start experiment {experiment_id}: {reason}")
            # TODO: Create approval request and return pending status
            return agent_pb2.StatusResponse(
                success=False,
                message=f"Experiment requires approval to start: {reason}"
            )

        # Get current timestamp
        current_time = timestamp_pb2.Timestamp(seconds=int(time.time()))

        # Update status to running
        status.state = agent_pb2.ExperimentState.STATE_RUNNING
        status.status_message = "Starting experiment..."
        status.start_time = current_time
        status.last_update_time = current_time

        # Reset metrics for the new run
        if status.metrics:
            status.metrics.update({
                "progress_percent": 0.0,
                "elapsed_time_seconds": 0.0,
                "estimated_remaining_seconds": 0.0,
                "error_count": 0
            })

        logger.info(f"Starting experiment: {experiment_id}")

        # Sync status change to database
        sync_experiment_to_db(experiment_id)

        # Submit task execution to the thread pool
        task_type = status.type
        task_parameters = status.definition.parameters

        task_instance = None
        if task_type == agent_pb2.ExperimentType.AI_DRIVEN_EBOOKS:
            task_instance = EbookGeneratorTask()
            status.status_message = "Ebook generation task submitted to executor"
            logger.info(f"Ebook generation task submitted for experiment {experiment_id}")
        elif task_type == agent_pb2.ExperimentType.FREELANCE_WRITING:
            task_instance = FreelanceWritingTask()
            status.status_message = "Freelance writing task submitted to executor"
            logger.info(f"Freelance writing task submitted for experiment {experiment_id}")
        elif task_type == agent_pb2.ExperimentType.NICHE_AFFILIATE_WEBSITE:
            task_instance = NicheAffiliateWebsiteTask()
            status.status_message = "Niche affiliate website task submitted to executor"
            logger.info(f"Niche affiliate website task submitted for experiment {experiment_id}")
        elif task_type == agent_pb2.ExperimentType.PINTEREST_STRATEGY:
            task_instance = PinterestStrategyTask()
            status.status_message = "Pinterest strategy task submitted to executor"
            logger.info(f"Pinterest strategy task submitted for experiment {experiment_id}")
        else:
            status.status_message = f"Unknown experiment type: {task_type}. Cannot start task."
            status.state = agent_pb2.ExperimentState.STATE_FAILED
            logger.error(status.status_message)
            # No task submitted, update status immediately
            status.last_update_time = current_time
            # TODO: Notify backend of status change
            return agent_pb2.StatusResponse(success=False, message=f"Unknown experiment type: {task_type}")

        # If we have a valid task instance, submit it to the executor
        if task_instance:
            future = task_executor.submit(task_instance.execute, task_parameters)
            future.add_done_callback(lambda f: self._handle_task_completion(experiment_id, f))

            # Store the future for potential cancellation
            running_tasks[experiment_id] = future

            # Start a background thread to update metrics periodically
            threading.Thread(
                target=self._update_experiment_metrics,
                args=(experiment_id,),
                daemon=True
            ).start()

        return agent_pb2.StatusResponse(success=True, message=f"Experiment {experiment_id} started")

    def _update_experiment_metrics(self, experiment_id):
        """
        Periodically update metrics for a running experiment.
        This runs in a background thread.
        """
        logger.info(f"Starting metrics update thread for experiment {experiment_id}")

        # Update metrics every 5 seconds while the experiment is running
        while experiment_id in experiment_statuses:
            status = experiment_statuses[experiment_id]

            # Only update metrics if the experiment is still running
            if status.state != agent_pb2.ExperimentState.STATE_RUNNING:
                break

            try:
                # Get current timestamp
                current_time = int(time.time())

                # Calculate elapsed time
                if status.start_time:
                    start_time = status.start_time.seconds
                    elapsed_seconds = current_time - start_time

                    # Update metrics
                    if status.metrics:
                        # Get system metrics
                        cpu_usage, memory_usage = get_system_metrics()

                        # Update the metrics
                        status.metrics.update({
                            "elapsed_time_seconds": float(elapsed_seconds),
                            "cpu_usage_percent": cpu_usage,
                            "memory_usage_mb": memory_usage
                        })

                        # Simulate progress for now (in a real implementation, the task would report progress)
                        # This is just a placeholder - real tasks should report actual progress
                        if elapsed_seconds > 0:
                            # Simple progress simulation - increases over time but slows down
                            progress = min(95.0, (elapsed_seconds / (elapsed_seconds + 30.0)) * 100.0)
                            status.metrics.update({"progress_percent": progress})

                            # Estimate remaining time based on progress
                            if progress > 0:
                                estimated_total = elapsed_seconds * (100.0 / progress)
                                estimated_remaining = max(0, estimated_total - elapsed_seconds)
                                status.metrics.update({"estimated_remaining_seconds": estimated_remaining})

                # Update last_update_time
                status.last_update_time.seconds = current_time

                # Sync metrics update to database
                sync_experiment_to_db(experiment_id)

            except Exception as e:
                logger.error(f"Error updating metrics for experiment {experiment_id}: {e}")

            # Sleep for 5 seconds before next update
            time.sleep(5)

        logger.info(f"Metrics update thread for experiment {experiment_id} stopped")

    def _handle_task_completion(self, experiment_id, future):
        """
        Callback function to handle the result of a completed task.
        Updates the experiment status based on the task result and notifies the backend.
        """
        logger.info(f"Task completed for experiment {experiment_id}")

        # Remove from running tasks
        if experiment_id in running_tasks:
            del running_tasks[experiment_id]

        status = experiment_statuses.get(experiment_id)
        if not status:
            logger.error(f"Experiment status not found for completed task: {experiment_id}")
            return

        try:
            # Check if the task was cancelled
            if future.cancelled():
                logger.info(f"Task for experiment {experiment_id} was cancelled")
                # The status should already be updated to STOPPED by StopExperiment
                return

            task_result = future.result() # Get the result or raise exception
            logger.info(f"Task result for {experiment_id}: {task_result}")

            # Update status based on task_result structure (assuming dict with 'status' and 'result'/'message')
            if task_result.get("status") == "completed":
                status.state = agent_pb2.ExperimentState.STATE_COMPLETED
                status.status_message = "Task completed successfully"

                # Update metrics to 100% completion
                if status.metrics:
                    status.metrics.update({
                        "progress_percent": 100.0,
                        "estimated_remaining_seconds": 0.0
                    })

                # Store results in metrics if available
                if "result" in task_result and status.metrics:
                    # Convert result to a flat structure for metrics
                    result_metrics = self._flatten_result_for_metrics(task_result["result"])
                    status.metrics.update(result_metrics)

            else: # Assuming "failed" status or exception
                status.state = agent_pb2.ExperimentState.STATE_FAILED
                status.status_message = task_result.get("message", "Task failed")

                # Update error count in metrics
                if status.metrics:
                    error_count = status.metrics.get("error_count", 0) + 1
                    status.metrics.update({"error_count": error_count})

                logger.error(f"Task failed for experiment {experiment_id}: {status.status_message}")

        except Exception as e:
            logger.error(f"Task execution failed for experiment {experiment_id}: {e}", exc_info=True)
            status.state = agent_pb2.ExperimentState.STATE_FAILED
            status.status_message = f"Task execution failed: {str(e)}"

            # Update error count in metrics
            if status.metrics:
                error_count = status.metrics.get("error_count", 0) + 1
                status.metrics.update({"error_count": error_count})

        finally:
            # Update last_update_time
            status.last_update_time.seconds = int(time.time())
            logger.info(f"Experiment {experiment_id} status updated to {status.state}")

            # Sync status change to database
            sync_experiment_to_db(experiment_id)

    def _flatten_result_for_metrics(self, result):
        """
        Convert a nested result structure to a flat dictionary for metrics.
        Only includes scalar values (strings, numbers, booleans).
        """
        flat_metrics = {}

        # If result is already a dict, flatten it
        if isinstance(result, dict):
            for key, value in result.items():
                # Only include scalar values
                if isinstance(value, (str, int, float, bool)):
                    flat_metrics[f"result_{key}"] = value

        # If result is a string, store it as a single value
        elif isinstance(result, str):
            flat_metrics["result_summary"] = result

        return flat_metrics

    def StopExperiment(self, request, context):
        logger.info(f"Received StopExperiment request: {request}")
        experiment_id = request.id.id

        if experiment_id not in experiment_statuses:
            logger.warning(f"Attempted to stop non-existent experiment: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} not found")

        status = experiment_statuses[experiment_id]
        if status.state in [agent_pb2.ExperimentState.STATE_COMPLETED, agent_pb2.ExperimentState.STATE_FAILED, agent_pb2.ExperimentState.STATE_STOPPED]:
            logger.warning(f"Attempted to stop experiment that is not running: {experiment_id}")
            return agent_pb2.StatusResponse(success=False, message=f"Experiment with ID {experiment_id} is not running")

        # Update status to stopped
        status.state = agent_pb2.ExperimentState.STATE_STOPPED
        status.status_message = "Experiment stopped manually"
        status.last_update_time.seconds = int(time.time())
        logger.info(f"Stopping experiment: {experiment_id}")

        # Cancel the running task if it exists
        if experiment_id in running_tasks:
            future = running_tasks[experiment_id]
            if not future.done():
                logger.info(f"Cancelling task for experiment {experiment_id}")
                cancelled = future.cancel()
                if cancelled:
                    logger.info(f"Task for experiment {experiment_id} cancelled successfully")
                else:
                    logger.warning(f"Failed to cancel task for experiment {experiment_id}, it may have already completed")
            else:
                logger.info(f"Task for experiment {experiment_id} already completed, no need to cancel")

            # Remove from running tasks
            del running_tasks[experiment_id]
        else:
            logger.warning(f"No running task found for experiment {experiment_id}")

        # Sync status change to database
        sync_experiment_to_db(experiment_id)

        return agent_pb2.StatusResponse(success=True, message=f"Experiment {experiment_id} stopped")

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

        # Get pending approval count
        pending_approvals = autonomy_framework.get_approval_workflow().get_pending_count()

        # Get system metrics
        cpu_usage, memory_usage = get_system_metrics()

        # Determine overall agent state
        agent_state = "IDLE"
        if active_count > 0:
            agent_state = "RUNNING_EXPERIMENTS"
        if pending_approvals > 0:
            agent_state = "AWAITING_APPROVAL"

        # Get current timestamp
        current_time = timestamp_pb2.Timestamp(seconds=int(time.time()))

        return agent_pb2.AgentStatus(
            agent_state=agent_state,
            active_experiments=active_count,
            cpu_usage_percent=cpu_usage,
            memory_usage_mb=memory_usage,
            last_updated=current_time
        )

    def GetLogs(self, request, context):
        logger.info(f"Received GetLogs request: {request}")

        # Extract request parameters
        experiment_id = request.experiment_id.id if request.experiment_id else None
        minimum_level = request.minimum_level if hasattr(request, 'minimum_level') else agent_pb2.LogLevel.LOG_LEVEL_UNSPECIFIED

        # For a real implementation, we would query logs from a persistent store
        # For now, generate some sample logs
        current_time = int(time.time())

        # Create a sample log entry
        sample_log = agent_pb2.LogEntry(
            timestamp=timestamp_pb2.Timestamp(seconds=current_time),
            level=agent_pb2.LogLevel.INFO,
            message=f"Log streaming initiated for {'experiment ' + experiment_id if experiment_id else 'all experiments'}",
            source_component="AgentCore"
        )

        # Sync log entry to database if it's for a specific experiment
        if experiment_id:
            sample_log.experiment_id = agent_pb2.ExperimentId(id=experiment_id)
            sync_log_to_db(sample_log)

        # Yield the sample log
        yield sample_log

        # If we have an experiment ID, yield some experiment-specific logs
        if experiment_id and experiment_id in experiment_statuses:
            status = experiment_statuses[experiment_id]

            # Create a log entry with the experiment status
            status_log = agent_pb2.LogEntry(
                timestamp=timestamp_pb2.Timestamp(seconds=current_time),
                level=agent_pb2.LogLevel.INFO,
                message=f"Experiment status: {status.state}, {status.status_message}",
                experiment_id=agent_pb2.ExperimentId(id=experiment_id),
                source_component="AgentCore"
            )

            # Sync log entry to database
            sync_log_to_db(status_log)

            # Yield the status log
            yield status_log

            # If the experiment has metrics, yield a log with the metrics
            if status.metrics:
                metrics_dict = {}
                for key, value in status.metrics.items():
                    metrics_dict[key] = value

                metrics_log = agent_pb2.LogEntry(
                    timestamp=timestamp_pb2.Timestamp(seconds=current_time),
                    level=agent_pb2.LogLevel.INFO,
                    message=f"Experiment metrics: {json.dumps(metrics_dict)}",
                    experiment_id=agent_pb2.ExperimentId(id=experiment_id),
                    source_component="AgentCore"
                )

                # Sync log entry to database
                sync_log_to_db(metrics_log)

                # Yield the metrics log
                yield metrics_log

    def ApproveDecision(self, request, context):
        logger.info(f"Received ApproveDecision request: {request}")

        # Extract request parameters
        decision_id = request.decision_id
        approved = request.approved
        user_id = request.user_id
        reason = request.reason if hasattr(request, 'reason') else None

        # Get the approval workflow from the autonomy framework
        approval_workflow = autonomy_framework.get_approval_workflow()

        # Approve or reject the decision
        if approved:
            success = approval_workflow.approve_request(decision_id, user_id, reason)
            if success:
                return agent_pb2.StatusResponse(success=True, message=f"Decision {decision_id} approved")
            else:
                return agent_pb2.StatusResponse(success=False, message=f"Failed to approve decision {decision_id}")
        else:
            success = approval_workflow.reject_request(decision_id, user_id, reason)
            if success:
                return agent_pb2.StatusResponse(success=True, message=f"Decision {decision_id} rejected")
            else:
                return agent_pb2.StatusResponse(success=False, message=f"Failed to reject decision {decision_id}")

    def StopAgent(self, request, context):
        logger.info(f"Received StopAgent request")
        logger.warning("Agent stop requested. Implementing kill switch...")

        # Stop all running experiments
        experiments_stopped = 0
        for experiment_id in list(running_tasks.keys()):  # Use list to avoid modification during iteration
            try:
                # Cancel the task
                future = running_tasks[experiment_id]
                if not future.done():
                    cancelled = future.cancel()
                    if cancelled:
                        logger.info(f"Task for experiment {experiment_id} cancelled successfully")
                    else:
                        logger.warning(f"Failed to cancel task for experiment {experiment_id}")

                # Update experiment status
                if experiment_id in experiment_statuses:
                    status = experiment_statuses[experiment_id]
                    if status.state == agent_pb2.ExperimentState.STATE_RUNNING:
                        status.state = agent_pb2.ExperimentState.STATE_STOPPED
                        status.status_message = "Experiment stopped by agent kill switch"
                        status.last_update_time.seconds = int(time.time())
                        experiments_stopped += 1

                # Remove from running tasks
                del running_tasks[experiment_id]

            except Exception as e:
                logger.error(f"Error stopping experiment {experiment_id}: {e}")

        # Sync all experiment statuses to database before shutdown
        if db_sync_enabled:
            for experiment_id in experiment_statuses:
                try:
                    sync_experiment_to_db(experiment_id)
                except Exception as e:
                    logger.error(f"Error syncing experiment {experiment_id} to database during shutdown: {e}")

        # Shutdown the task executor (but don't wait for tasks to complete)
        task_executor.shutdown(wait=False)

        # Close database client connection
        if db_sync_enabled:
            db_client.close()
            logger.info("Database client connection closed")

        # Log the result
        logger.warning(f"Agent kill switch activated. Stopped {experiments_stopped} running experiments.")

        return agent_pb2.StatusResponse(
            success=True,
            message=f"Agent stopped. {experiments_stopped} experiments were forcibly stopped."
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServiceServicer(), server)

    port = os.getenv("AGENT_CORE_PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Agent Core Service starting on port {port}")
    server.start()

    # Register signal handlers for graceful shutdown
    import signal

    def handle_shutdown(signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")

        # Stop the server
        server.stop(5)  # 5 seconds grace period

        # Close database client connection
        if db_sync_enabled:
            db_client.close()
            logger.info("Database client connection closed")

        # Shutdown task executor
        task_executor.shutdown(wait=False)
        logger.info("Task executor shutdown")

        # Exit
        logger.info("Shutdown complete")
        exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, handle_shutdown)  # kill command

    try:
        # Keep the server running
        while True:
            time.sleep(86400)  # Server stays alive for 24 hours
    except KeyboardInterrupt:
        # This should be caught by the signal handler, but just in case
        handle_shutdown(signal.SIGINT, None)

if __name__ == '__main__':
    # Need to import uuid and timestamp_pb2 here for the stubbed implementation
    import uuid
    from google.protobuf import timestamp_pb2
    serve()
