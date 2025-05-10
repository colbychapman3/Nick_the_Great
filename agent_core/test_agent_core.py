"""
Test script for the Agent Core Service.

This script tests the basic functionality of the Agent Core Service by creating
an experiment, starting it, checking its status, and stopping it.
"""

import grpc
import time
import os
import sys
from google.protobuf.struct_pb2 import Struct
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the generated proto files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the generated proto files
from proto import agent_pb2
from proto import agent_pb2_grpc

# Load environment variables from .env file
load_dotenv()

def run_test():
    """Run a test of the Agent Core Service."""
    # Connect to the Agent Core Service
    channel = grpc.insecure_channel('localhost:50051')
    stub = agent_pb2_grpc.AgentServiceStub(channel)
    
    print("Connected to Agent Core Service")
    
    # Get agent status
    try:
        agent_status = stub.GetAgentStatus(agent_pb2.Empty())
        print(f"Agent Status: {agent_status}")
    except Exception as e:
        print(f"Error getting agent status: {e}")
        return
    
    # Create an experiment
    try:
        # Create parameters as a Struct
        parameters = Struct()
        parameters.update({
            "topic": "Python Programming",
            "target_audience": "Beginners",
            "length": "10000 words",
            "include_code_examples": True
        })
        
        # Create the experiment definition
        experiment_def = agent_pb2.ExperimentDefinition(
            type=agent_pb2.ExperimentType.AI_DRIVEN_EBOOKS,
            name="Test Ebook Generator",
            description="A test of the ebook generator task",
            parameters=parameters
        )
        
        # Create the experiment
        create_response = stub.CreateExperiment(agent_pb2.CreateExperimentRequest(definition=experiment_def))
        experiment_id = create_response.id.id
        print(f"Created experiment with ID: {experiment_id}")
        print(f"Create Response: {create_response}")
    except Exception as e:
        print(f"Error creating experiment: {e}")
        return
    
    # Get experiment status
    try:
        status_response = stub.GetExperimentStatus(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Experiment Status: {status_response}")
    except Exception as e:
        print(f"Error getting experiment status: {e}")
        return
    
    # Start the experiment
    try:
        start_response = stub.StartExperiment(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Start Response: {start_response}")
    except Exception as e:
        print(f"Error starting experiment: {e}")
        return
    
    # Get experiment status again
    try:
        status_response = stub.GetExperimentStatus(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Experiment Status after starting: {status_response}")
    except Exception as e:
        print(f"Error getting experiment status: {e}")
        return
    
    # Wait for a bit to let the experiment run
    print("Waiting for 10 seconds...")
    time.sleep(10)
    
    # Get experiment status again
    try:
        status_response = stub.GetExperimentStatus(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Experiment Status after waiting: {status_response}")
    except Exception as e:
        print(f"Error getting experiment status: {e}")
        return
    
    # Stop the experiment
    try:
        stop_response = stub.StopExperiment(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Stop Response: {stop_response}")
    except Exception as e:
        print(f"Error stopping experiment: {e}")
        return
    
    # Get experiment status one more time
    try:
        status_response = stub.GetExperimentStatus(agent_pb2.ExperimentId(id=experiment_id))
        print(f"Experiment Status after stopping: {status_response}")
    except Exception as e:
        print(f"Error getting experiment status: {e}")
        return
    
    # Get agent status again
    try:
        agent_status = stub.GetAgentStatus(agent_pb2.Empty())
        print(f"Agent Status after test: {agent_status}")
    except Exception as e:
        print(f"Error getting agent status: {e}")
        return
    
    print("Test completed successfully!")

if __name__ == "__main__":
    run_test()
