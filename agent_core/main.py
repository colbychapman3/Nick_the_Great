import grpc
from concurrent import futures
import time
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import generated gRPC code
try:
    import agent_service.agent_pb2 as agent_pb2
    import agent_service.agent_pb2_grpc as agent_pb2_grpc
except ImportError as e:
    logging.error(f"Failed to import generated gRPC code: {e}. Make sure you have generated the code using protoc and that the agent_service directory is in the Python path.")
    raise

# Implement the AgentService
class AgentServiceServicer(agent_pb2_grpc.AgentServiceServicer):
    def CreateExperiment(self, request, context):
        logging.info(f"CreateExperiment called with request: {request}")
        try:
            # Extract experiment details from the request
            experiment_type = request.definition.type
            experiment_name = request.definition.name
            experiment_description = request.definition.description
            experiment_parameters = request.definition.parameters

            logging.info(f"Creating experiment: type={experiment_type}, name={experiment_name}, description={experiment_description}, parameters={experiment_parameters}")

            # TODO: Implement experiment creation logic based on experiment_type
            # For now, just log the details and return a success message

            experiment_id = "not-implemented"  # Replace with actual experiment ID generation

            return agent_pb2.CreateExperimentResponse(
                id=agent_pb2.ExperimentId(id=experiment_id),
                status=agent_pb2.StatusResponse(success=True, message="Experiment creation initiated (logic not implemented yet)")
            )
        except Exception as e:
            logging.error(f"Error creating experiment: {e}")
            return agent_pb2.CreateExperimentResponse(
                id=agent_pb2.ExperimentId(id="error"),
                status=agent_pb2.StatusResponse(success=False, message=f"Error creating experiment: {e}")
            )

    def StartExperiment(self, request, context):
        logging.info(f"StartExperiment called with request: {request}")
        # TODO: Implement experiment starting logic
        return agent_pb2.StatusResponse(success=False, message="Not implemented yet")

    def StopExperiment(self, request, context):
        logging.info(f"StopExperiment called with request: {request}")
        # TODO: Implement experiment stopping logic
        return agent_pb2.StatusResponse(success=False, message="Not implemented yet")

    def GetExperimentStatus(self, request, context):
        logging.info(f"GetExperimentStatus called with request: {request}")
        # TODO: Implement experiment status retrieval logic
        return agent_pb2.ExperimentStatus(id=request.id, state=agent_pb2.ExperimentState.STATE_UNSPECIFIED, status_message="Not implemented yet")

    def GetAgentStatus(self, request, context):
        logging.info(f"GetAgentStatus called")
        # TODO: Implement agent status retrieval logic
        return agent_pb2.AgentStatus(agent_state="IDLE", active_experiments=0, cpu_usage_percent=0.0, memory_usage_mb=0.0)

    def GetLogs(self, request, context):
        logging.info(f"GetLogs called with request: {request}")
        # TODO: Implement log streaming logic
        yield agent_pb2.LogEntry(message="Not implemented yet")

    def ApproveDecision(self, request, context):
        logging.info(f"ApproveDecision called with request: {request}")
        # TODO: Implement decision approval logic
        return agent_pb2.StatusResponse(success=False, message="Not implemented yet")

    def StopAgent(self, request, context):
        logging.info(f"StopAgent called with request: {request}")
        # TODO: Implement agent stopping logic
        return agent_pb2.StatusResponse(success=True, message="StopAgent not implemented yet")

def serve():
    port = os.environ.get("AGENT_PORT", "50052")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServiceServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info(f"Agent Core Service started, listening on port {port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")

if __name__ == "__main__":
    serve()
