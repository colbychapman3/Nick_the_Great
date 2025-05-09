# Nick the Great: Autonomous Income Generation Agent

Nick the Great is an autonomous AI agent system designed to maximize income generation through collaborative AI-human business building. Starting from a zero-capital position, the system aims to rapidly experiment with, develop, and scale multiple digital business ventures simultaneously, focusing progressively on those demonstrating the highest returns with the lowest overhead.

The project leverages AI for research, analysis, content creation, and strategy, while human collaboration is utilized for account management, financial decisions, and client interactions, aiming to establish a new paradigm for digital entrepreneurship.

## Architecture Overview

Nick the Great employs a modular architecture:

*   **Frontend (Web):** A Next.js application providing the user interface for dashboards, experiment management, and human interaction tasks.
*   **Mobile App:** A React Native application offering similar functionalities to the web frontend for mobile users.
*   **Backend API:** A Node.js/Express server that handles user authentication, data persistence (MongoDB), and acts as a gateway to the Agent Core Service.
*   **Agent Core Service:** A Python application using gRPC for communication. It orchestrates the agent's lifecycle, manages experiment execution, implements autonomy frameworks, and schedules tasks.
*   **Task Execution Modules:** Python scripts/libraries invoked by the Agent Core to perform specific business tasks (e.g., content generation with AbacusAI, Pinterest automation).
*   **MongoDB:** The primary database for storing user data, strategies, experiment details, and results.

For a detailed architecture diagram and component responsibilities, please see [design.md](design.md).

## Technologies Used

*   **Frontend (Web):** Next.js, React, TypeScript, Tailwind CSS
*   **Backend API:** Node.js, Express.js
*   **Agent Core Service:** Python, gRPC
*   **Mobile App:** React Native, TypeScript
*   **Database:** MongoDB
*   **AI/Task Modules:** AbacusAI (via ACI), Python for various automation scripts.

Refer to [researchstack.md](researchstack.md) for more details on specific libraries and versions.

## Project Structure

```
nick-the-great/
├── agent_core/         # Python gRPC Agent Core Service
│   ├── proto/          # Protocol Buffer definitions (shared)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── backend/            # Node.js/Express API server
│   ├── src/
│   ├── .env.example
│   └── package.json
├── frontend/           # Next.js web application
│   ├── src/
│   ├── .env.example
│   └── package.json
├── mobile/             # React Native mobile application
│   ├── src/
│   ├── .env.example
│   └── package.json
├── task_modules/       # Python modules for specific agent tasks
├── ebooks/             # Ebook generation related files
├── experiments/        # Experiment definitions and tracking
├── autonomy/           # Frameworks for agent autonomy and decision making
├── memory-bank/        # Core project documentation and context
├── cli/                # Command Line Interface for agent interaction
├── docker-compose.yml  # For local development environment
├── design.md           # Detailed system design
├── researchstack.md    # Technology research and documentation
└── README.md           # This file
```
*(Structure abridged for brevity. Refer to the file system for a complete view.)*

## Prerequisites

*   Node.js (v18 or higher recommended)
*   Python (v3.9 or higher recommended)
*   Docker & Docker Compose (for running services locally, especially Agent Core)
*   `npm` (for Node.js and React Native projects)
*   `pip` or `uv` (for Python projects)
*   Access to a MongoDB instance (local or Atlas)
*   API keys for any external services used (e.g., AbacusAI)

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd nick-the-great
    ```

2.  **Environment Variables:**
    *   This project uses `.env` files to manage environment-specific configurations.
    *   Copy the `.env.example` file to `.env` in each respective service directory (`backend/`, `frontend/`, `agent_core/`, `mobile/`) and populate them with the necessary values (API keys, database URIs, etc.).
    *   Refer to `env-variables.md` (if available) or individual service documentation for details on required variables.
    *   Example for backend:
        ```bash
        cp backend/.env.example backend/.env
        # Edit backend/.env with your MONGODB_URI, JWT_SECRET, etc.
        ```

3.  **Install Dependencies:**
    *   **Frontend:**
        ```bash
        cd frontend
        npm install
        cd ..
        ```
    *   **Backend:**
        ```bash
        cd backend
        npm install
        cd ..
        ```
    *   **Agent Core Service:**
        ```bash
        cd agent_core
        # Using pip:
        pip install -r requirements.txt
        # Or using uv (if project is set up for it):
        # uv sync
        cd ..
        ```
    *   **Mobile App:**
        ```bash
        cd mobile
        npm install
        cd ..
        ```

4.  **Generate gRPC Stubs (if necessary):**
    *   The gRPC client/server stubs are generated from `.proto` files located in `agent_core/proto/`.
    *   If you modify these files or they are not pre-generated, you may need to run a generation script. (Details of this script should be added if it exists, or manual `protoc` commands).
    *   For Python: `python -m grpc_tools.protoc -I./agent_core/proto --python_out=./agent_core --pyi_out=./agent_core --grpc_python_out=./agent_core ./agent_core/proto/agent.proto`
    *   For Node.js (Backend): The backend typically uses `@grpc/proto-loader` to load `.proto` files dynamically, so explicit generation might not be needed.

## Running the Application (Development)

It's recommended to run services in separate terminal windows.

1.  **Backend API:**
    ```bash
    cd backend
    npm run dev
    ```
    (Typically runs on `http://localhost:PORT` as defined in `backend/.env`)

2.  **Frontend Web Application:**
    ```bash
    cd frontend
    npm run dev
    ```
    (Typically runs on `http://localhost:3000`)

3.  **Agent Core Service:**
    *   **Directly:**
        ```bash
        cd agent_core
        python main.py
        ```
        (Listens on a gRPC port, e.g., `localhost:50051` as configured)
    *   **Via Docker (if `Dockerfile` is configured for development):**
        ```bash
        # (Build command if needed)
        docker run <agent-core-image-name>
        ```

4.  **Mobile App:**
    ```bash
    cd mobile
    # For Android:
    npm run android
    # For iOS (macOS only):
    npm run ios
    ```

5.  **Using Docker Compose (Recommended for integrated local development):**
    *   If a `docker-compose.yml` file is configured to run all services:
        ```bash
        docker-compose up --build
        ```

## Deployment

*   **Frontend (Web):** Deployed on [Vercel](https://vercel.com/).
*   **Backend API:** Deployed on [Render.com](https://render.com/).
*   **Agent Core Service:** Deployed on [Render.com](https://render.com/) (typically as a separate service or alongside the backend).

Configuration for deployments (build commands, start commands, environment variables) is managed within the respective hosting platforms. Refer to `render.yaml` for Render.com service configurations.

## Key Features

*   Autonomous management of digital business experiments.
*   AI-driven task execution for content creation, analysis, and more.
*   Collaborative workflow between AI and human operators.
*   Parallel experimentation and progressive resource optimization.
*   Comprehensive documentation and learning system.

## Documentation & Memory Bank

The `memory-bank/` directory is crucial for this project. It contains the core documentation, context, and evolving knowledge base that guides the AI and human collaborators. Key documents include:

*   [projectbrief.md](memory-bank/projectbrief.md): The foundational goals and requirements.
*   [productContext.md](memory-bank/productContext.md): The "why" behind the project.
*   [systemPatterns.md](memory-bank/systemPatterns.md): High-level architectural patterns.
*   [techContext.md](memory-bank/techContext.md): Technical stack and setup details.
*   [activeContext.md](memory-bank/activeContext.md): Current work focus and next steps.
*   [progress.md](memory-bank/progress.md): Overall project progress and status.

For detailed system architecture and design decisions, refer to [design.md](design.md).

## Contributing

(Details on contribution guidelines, code style, and pull request processes can be added here.)

---

This README provides a general overview. For specific details, please refer to the documents linked and the source code within each module.
