# Agent Core Service

The Agent Core Service is the central component of the Nick the Great Unified Agent system. It is responsible for managing experiments, executing tasks, and implementing the autonomy framework.

## Architecture

The Agent Core Service is implemented as a gRPC server in Python. It exposes a set of methods for creating, starting, stopping, and monitoring experiments. It also provides methods for getting the overall agent status and streaming logs.

### Key Components

- **AgentServiceServicer**: The main gRPC service implementation that handles all API requests.
- **Task Modules**: Specialized modules for executing different types of experiments (e.g., ebook generation, Pinterest strategy).
- **Autonomy Framework**: A system for determining when the agent can act autonomously and when it needs human approval.
- **Metrics Tracking**: A system for tracking experiment progress and resource usage.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- gRPC and Protocol Buffers
- Other dependencies listed in `requirements.txt`

### Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure the Protocol Buffer files have been generated:

```bash
cd ..
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/agent.proto
```

## Running the Service

To start the Agent Core Service:

```bash
python main.py
```

By default, the service will listen on port 50051. You can change this by setting the `AGENT_CORE_PORT` environment variable.

## Testing

To test the Agent Core Service, you can use the provided test script:

```bash
python test_agent_core.py
```

This script will create a test experiment, start it, check its status, and stop it.

## API Reference

The Agent Core Service exposes the following gRPC methods:

- **CreateExperiment**: Create a new experiment with the specified definition.
- **StartExperiment**: Start an existing experiment.
- **StopExperiment**: Stop a running experiment.
- **GetExperimentStatus**: Get the current status of an experiment.
- **GetAgentStatus**: Get the overall status of the agent.
- **GetLogs**: Stream logs from the agent.
- **ApproveDecision**: Approve or reject a decision that requires human approval.
- **StopAgent**: Stop the agent (kill switch).

## Experiment Types

The Agent Core Service supports the following experiment types:

- **AI_DRIVEN_EBOOKS**: Generate and sell ebooks using AI.
- **FREELANCE_WRITING**: Manage freelance writing projects.
- **NICHE_AFFILIATE_WEBSITE**: Create and manage niche affiliate websites.
- **PINTEREST_STRATEGY**: Implement Pinterest marketing strategies.

## Autonomy Framework

The Agent Core Service includes an autonomy framework that determines when the agent can act autonomously and when it needs human approval. The framework consists of:

- **Decision Matrix**: Defines when the agent can act autonomously based on the type of action and context.
- **Notification System**: Sends notifications to humans when needed.
- **Approval Workflow**: Manages the process of requesting and processing human approvals.

## Metrics Tracking

The Agent Core Service tracks the following metrics for each experiment:

- **Progress**: The percentage of the experiment that has been completed.
- **Elapsed Time**: The time elapsed since the experiment was started.
- **Estimated Remaining Time**: The estimated time remaining until the experiment is completed.
- **CPU Usage**: The CPU usage of the experiment.
- **Memory Usage**: The memory usage of the experiment.
- **Error Count**: The number of errors encountered during the experiment.

## Future Enhancements

- **Persistent Storage**: Replace the in-memory storage with a persistent database (e.g., MongoDB).
- **Enhanced Autonomy Framework**: Implement a more sophisticated decision matrix based on machine learning.
- **Task Cancellation**: Improve the task cancellation mechanism to handle more complex tasks.
- **Metrics Visualization**: Add a dashboard for visualizing experiment metrics.
- **Security Enhancements**: Add authentication and authorization to the gRPC API.
