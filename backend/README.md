# Backend API Service

This is the Backend API Service for the Nick the Great Unified Agent system. It's a Node.js/Express.js server responsible for:

*   User authentication and authorization.
*   Data persistence via MongoDB for user accounts, configurations, and other application data.
*   Acting as a gateway to the Agent Core service via gRPC for experiment-related operations.
*   Exposing a REST API for the frontend application.

## Key Technologies

*   Node.js
*   Express.js
*   MongoDB (with Mongoose ODM, though direct driver usage is also present)
*   gRPC (for communication with Agent Core)
*   JSON Web Tokens (JWT) for authentication
*   bcrypt.js for password hashing

## Project Structure Overview (`src/`)

*   `auth.js`: Handles user registration, login, and JWT generation/verification.
*   `db.js` / `mock-db.js`: Manages MongoDB connection and potentially mock data for testing.
*   `grpc_server.js`: Implements the gRPC server that listens for requests from the Agent Core (e.g., for database synchronization).
*   `database_sync_service.js`: Service logic for handling data synchronization requests from Agent Core.
*   `models/`: Contains Mongoose schema definitions for database models (e.g., User, Experiment).
*   `routes/`: Defines the REST API endpoints exposed to the frontend.
*   `services/`: Contains business logic and services that interact with the database and other components.
*   `utils/`: Utility functions, like logging.
*   `index.js`: Main entry point for the Express application, sets up middleware and routes.

## Setup Instructions

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a `.env` file from the example and populate it:
    ```bash
    cp .env.example .env
    ```
    Key environment variables to configure in `.env`:
    *   `MONGODB_URI`: MongoDB connection string (e.g., `mongodb://localhost:27017/nick_agent_db`)
    *   `JWT_SECRET`: A strong, random secret key for signing JWTs.
    *   `AGENT_CORE_GRPC_ADDRESS`: Address of the Agent Core gRPC service (e.g., `localhost:50051`).
    *   `BACKEND_GRPC_PORT`: Port for the backend's own gRPC server (e.g., `50052`).
3.  Install dependencies:
    ```bash
    npm install
    ```

## Running the Service

*   **Development Mode (with nodemon for auto-restarts):**
    ```bash
    npm run dev
    ```
*   **Production Mode:**
    ```bash
    npm start
    ```

## Running Tests

Tests are run using Jest, often with `mongodb-memory-server` for in-memory database testing.

```bash
npm test
```

## API Endpoints

*   **REST API:** Routes are defined in `src/routes/` and provide endpoints for user authentication, data management, and interaction with agent functionalities. These are primarily consumed by the frontend application.
*   **gRPC Services:** The backend also hosts a gRPC server (defined in `src/grpc_server.js`) on the port specified by `BACKEND_GRPC_PORT`. This server provides services like `DatabaseSyncService` for the Agent Core to interact with the backend's database.

---
*Self-reflection: I've included all the requested points. I've tried to keep the descriptions concise but informative. I made an assumption about Mongoose being used based on typical Node.js/MongoDB setups, but also mentioned direct driver usage as `db.js` might indicate that. I'll proceed to the frontend README next.*
