# Persistent Storage Implementation for Nick the Great

This document describes the implementation of persistent storage for the Nick the Great project, which allows experiment data to be stored in MongoDB and synchronized between the Agent Core and Backend.

## Overview

The persistent storage implementation consists of the following components:

1. **MongoDB Schemas**: Defined in the backend for experiments, logs, and metrics.
2. **Backend API Endpoints**: Enhanced to use the MongoDB schemas for CRUD operations.
3. **Database Sync Service**: A gRPC service for synchronizing data between Agent Core and Backend.
4. **Agent Core Integration**: Updated to use the database sync service for persistence.

## Setup Instructions

### Prerequisites

- Node.js 14+ and npm
- Python 3.8+
- MongoDB 4.4+
- Protocol Buffer Compiler (protoc) 3.15+

### Generate gRPC Code

Run the following command from the project root to generate the gRPC code for both the backend and Agent Core:

```bash
chmod +x generate_protos.sh
./generate_protos.sh
```

### Backend Setup

1. Install dependencies:

```bash
cd backend
npm install
```

2. Set up environment variables:

Create a `.env` file in the `backend` directory with the following content:

```
MONGODB_URI=mongodb://localhost:27017/nick_agent
JWT_SECRET=your_jwt_secret
PORT=3001
GRPC_PORT=50052
SYNC_INTERVAL_MS=30000
SYSTEM_USER_ID=system
```

3. Test the database connection and experiment models:

```bash
npm run test:experiment
```

4. Test the database sync service:

```bash
npm run test:db-sync
```

### Agent Core Setup

1. Install dependencies:

```bash
cd agent_core
pip install -r requirements.txt
```

2. Set up environment variables:

Create a `.env` file in the `agent_core` directory with the following content:

```
BACKEND_HOST=localhost
BACKEND_GRPC_PORT=50052
DB_SYNC_ENABLED=true
```

3. Test the database client:

```bash
cd agent_core
python -m unittest tests/test_db_sync.py
```

## Running the System

1. Start the backend server:

```bash
cd backend
npm run dev
```

2. Start the Agent Core:

```bash
cd agent_core
python -m agent_core
```

## Architecture

### MongoDB Schemas

- **Experiment**: Stores experiment metadata, status, and metrics.
- **ExperimentLog**: Stores log entries for experiments.
- **ExperimentMetrics**: Stores historical metrics data for experiments.

### Database Sync Service

The database sync service is a gRPC service that provides the following methods:

- **RestoreExperiments**: Restores experiment data from the database to the Agent Core.
- **SyncExperimentStatus**: Syncs experiment status from Agent Core to the database.
- **SyncLogEntry**: Syncs log entries from Agent Core to the database.
- **SyncMetrics**: Syncs metrics from Agent Core to the database.

### Synchronization Flow

1. **Agent Core Startup**: On startup, the Agent Core calls `RestoreExperiments` to load experiment data from the database.
2. **Experiment Creation**: When an experiment is created, the Agent Core calls `SyncExperimentStatus` to store it in the database.
3. **Experiment Updates**: When an experiment's status changes, the Agent Core calls `SyncExperimentStatus` to update the database.
4. **Logging**: When a log entry is generated, the Agent Core calls `SyncLogEntry` to store it in the database.
5. **Metrics Updates**: When metrics are updated, the Agent Core calls `SyncMetrics` to store them in the database.

## Testing

### Backend Tests

- **test-experiment-db.js**: Tests the experiment models and database operations.
- **test-db-sync.js**: Tests the database sync service.

### Agent Core Tests

- **test_db_sync.py**: Tests the database client in the Agent Core.

## Troubleshooting

### Common Issues

1. **MongoDB Connection Errors**: Ensure MongoDB is running and the connection string is correct.
2. **gRPC Connection Errors**: Check that the backend gRPC server is running and the port is correct.
3. **Proto Generation Errors**: Ensure the protoc compiler is installed and the proto files are valid.

### Logs

- Backend logs are stored in `backend/logs`.
- Agent Core logs are output to the console.

## Future Improvements

1. **TLS for gRPC**: Add TLS encryption for secure communication between Agent Core and Backend.
2. **Authentication for gRPC**: Add authentication for gRPC calls.
3. **Metrics Aggregation**: Add aggregation for metrics data to reduce storage requirements.
4. **Backup and Recovery**: Add backup and recovery mechanisms for the database.
5. **Sharding**: Add sharding for horizontal scaling of the database.
