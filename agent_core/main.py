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

            # Load the AbacusAI API key from environment variables
            abacus_api_key = os.getenv('ABACUSAI_API_KEY')
            if not abacus_api_key:
                logging.error("ABACUSAI_API_KEY not found in environment variables")
                return agent_pb2.CreateExperimentResponse(
                    id=agent_pb2.ExperimentId(id="error"),
                    status=agent_pb2.StatusResponse(success=False, message="ABACUSAI_API_KEY not found in environment variables")
                )

            # Initialize the EbookGenerator
            from task_modules.ebook_generator import EbookGenerator
            ebook_generator = EbookGenerator(abacus_api_key)

            # Create a unique experiment ID
            import uuid
            experiment_id = str(uuid.uuid4())

            # Store the experiment details (for now, just in memory)
            self.experiments = {} # Initialize experiments dictionary if it doesn't exist
            self.experiments[experiment_id] = {
                "type": experiment_type,
                "name": experiment_name,
                "description": experiment_description,
                "parameters": experiment_parameters,
                "generator": ebook_generator,
                "status": "DEFINED"
            }

            return agent_pb2.CreateExperimentResponse(
                id=agent_pb2.ExperimentId(id=experiment_id),
                status=agent_pb2.StatusResponse(success=True, message="Ebook experiment creation initiated")
            )
        except Exception as e:
            logging.error(f"Error creating experiment: {e}")
            return agent_pb2.CreateExperimentResponse(
                id=agent_pb2.ExperimentId(id="error"),
                status=agent_pb2.StatusResponse(success=False, message=f"Error creating experiment: {e}")
            )

    def StartExperiment(self, request, context):
        logging.info(f"StartExperiment called with request: {request}")
        try:
            experiment_id = request.id.id
            if experiment_id not in self.experiments:
                return agent_pb2.StatusResponse(success=False, message=f"Experiment with id {experiment_id} not found")

            experiment = self.experiments[experiment_id]
            if experiment["status"] != "DEFINED":
                return agent_pb2.StatusResponse(success=False, message=f"Experiment with id {experiment_id} is not in DEFINED state")

            # TODO: Implement Autonomy Framework interaction before starting the experiment

            # Start the experiment
            experiment["status"] = "RUNNING"
            logging.info(f"Starting experiment: id={experiment_id}, type={experiment['type']}, name={experiment['name']}")

            # Call the EbookGenerator to generate the book
            try:
                topic = experiment["parameters"]["topic"]
                audience = experiment["parameters"]["audience"]
                output_dir = experiment["name"].replace(" ", "_").lower()  # Generate output directory from experiment name
                num_chapters = 10 # Default number of chapters

                experiment["generator"].generate_full_book(topic, audience, output_dir, num_chapters)
                experiment["status"] = "COMPLETED"
                return agent_pb2.StatusResponse(success=True, message=f"Experiment {experiment_id} started and completed successfully")

            except Exception as e:
                experiment["status"] = "FAILED"
                logging.error(f"Error generating ebook: {e}")
                return agent_pb2.StatusResponse(success=False, message=f"Error generating ebook: {e}")

        except Exception as e:
            logging.error(f"Error starting experiment: {e}")
            return agent_pb2.StatusResponse(success=False, message=f"Error starting experiment: {e}")

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
        try:
            # TODO: Implement actual logic to retrieve agent status
            # For now, return some dummy data
            agent_status = agent_pb2.AgentStatus(
                agent_state="IDLE",
                active_experiments=0,
                cpu_usage_percent=10.5,
                memory_usage_mb=500.2
            )
            return agent_status
        except Exception as e:
            logging.error(f"Error getting agent status: {e}")
            return agent_pb2.AgentStatus(agent_state="ERROR", active_experiments=0, cpu_usage_percent=0.0, memory_usage_mb=0.0)

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
