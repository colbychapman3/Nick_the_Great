# Design Plan: Nick the Great Unified Agent

This document outlines the proposed design for the unified Nick the Great agent, integrating the various components and frameworks identified during Phase 2. This plan adheres to the rules provided, referencing `researchstack.md` for technical details.

## 1. Goal

To create a unified agent system capable of:
- Managing and executing multiple digital business experiments in parallel.
- Leveraging AI (AbacusAI, potentially others) for tasks like content generation and analysis.
- Interacting with a human collaborator via Frontend/Mobile interfaces for oversight, approvals, and specific tasks.
- Adhering to predefined autonomy, legal, financial, and technical frameworks.
- Persisting data (experiments, results, strategies, user info) via the backend API and MongoDB.
- Progressively optimizing resource allocation based on experiment performance.

## 2. Proposed Architecture

We will adopt a modular architecture centered around the existing Backend API and a new **Agent Core Service**, communicating via gRPC.

```mermaid
graph TD
    subgraph "Human Interface Layer"
        UI_FE[Frontend (Next.js)]
        UI_MOB[Mobile App (React Native)]
    end

    subgraph "Backend Layer (Node.js/Express)"
        API[Backend API]
        DB[(MongoDB)]
    end

    subgraph "Agent Layer"
        AGENT_CORE[Agent Core Service (Python/gRPC)]
        EXP_MGMT[Experiment Management Module]
        AUTONOMY[Autonomy Framework Logic]
        TASK_EXEC[Task Execution Modules]
    end

    subgraph "External Services & Tools"
        ABACUS[AbacusAI]
        PINTEREST[Pinterest Automation]
        FREELANCE[Freelance Platforms (Fiverr/Upwork)]
        AFFILIATE[Affiliate Platforms]
        OTHER_TOOLS[...]
    end

    UI_FE -->|REST API| API
    UI_MOB -->|REST API| API
    API -->|Database Ops| DB
    API -->|gRPC| AGENT_CORE

    AGENT_CORE --> EXP_MGMT
    AGENT_CORE --> AUTONOMY
    AGENT_CORE --> TASK_EXEC

    TASK_EXEC -->|API Calls| ABACUS
    TASK_EXEC -->|Scripts/API| PINTEREST
    TASK_EXEC -->|Manual/API?| FREELANCE
    TASK_EXEC -->|Manual/API?| AFFILIATE
    TASK_EXEC -->|API/Lib| OTHER_TOOLS

    %% CLI Interaction
    CLI[Agent CLI (Python)] -->|gRPC| AGENT_CORE

```

**Component Breakdown:**

1.  **Human Interface Layer (Frontend/Mobile):**
    *   **Technology:** Next.js/React/TypeScript (Frontend), React Native (Mobile). See `researchstack.md`.
    *   **Responsibilities:** Display dashboards (experiment status, financials, tasks), allow human interaction (approvals, strategy input, manual tasks), communicate with Backend API.
    *   **Integration:** Via REST API calls to the Backend API.

2.  **Backend Layer (Node.js/Express/MongoDB):**
    *   **Technology:** Node.js/Express/MongoDB. See `researchstack.md`.
    *   **Responsibilities:** User authentication (JWTs), data persistence (users, strategies, resources, experiment metadata, results), expose REST API for interfaces, act as a gateway/proxy to the Agent Core Service via gRPC.
    *   **Integration:** Stores data in MongoDB, serves Frontend/Mobile via REST, communicates with Agent Core via gRPC.

3.  **Agent Layer:**
    *   **Agent Core Service:**
        *   **Technology:** Python. gRPC (`proto/agent.proto`) for communication interface.
        *   **Responsibilities:** Orchestrates the agent's lifecycle, manages experiment execution (start/stop/status), makes decisions based on autonomy frameworks, schedules tasks, communicates with Backend API (for data/notifications) and Task Execution Modules. Implements interruptibility ("kill switch").
        *   **Integration:** Implements the `AgentService` defined in `proto/agent.proto`. Communicates with other Agent Layer modules and Task Execution Modules. Listens for gRPC calls from Backend/CLI.
    *   **Experiment Management Module:**
        *   **Technology:** Python, part of Agent Core.
        *   **Responsibilities:** Implements logic from `experiments/` docs and `outputs/experiment_tracking_spreadsheet_template.md`. Tracks experiment status, metrics, calculates performance, recommends resource allocation based on `systemPatterns.md`.
        *   **Integration:** Called by Agent Core, reads/writes data via Backend API/DB.
    *   **Autonomy Framework Logic:**
        *   **Technology:** Python, part of Agent Core.
        *   **Responsibilities:** Implements rules from `autonomy/` framework documents (Decision Matrix, Notification/Approval, Legal, Financial, etc.). Determines when human interaction is needed. Considers rollback capabilities for decisions.
        *   **Integration:** Embedded within Agent Core's decision-making processes. Triggers notifications/approvals via Backend API.
    *   **Task Execution Modules:**
        *   **Technology:** Python (preferred), potentially others. Separate scripts or libraries.
        *   **Responsibilities:** Executes specific tasks related to experiments (e.g., calling AbacusAI, running Pinterest scripts, interacting with affiliate platforms). Designed for idempotency/reversibility where possible.
        *   **Integration:** Invoked by Agent Core (direct calls initially), interacts with External Services & Tools.

4.  **External Services & Tools:**
    *   **Technology:** Various (AbacusAI API, Pinterest API/scripts, etc.). See `researchstack.md`.
    *   **Responsibilities:** Provide the actual business functionalities.
    *   **Integration:** Accessed by Task Execution Modules via APIs or scripts.

5.  **CLI:**
    *   **Technology:** Python (`cli/agent_cli.py`).
    *   **Responsibilities:** Provides a command-line interface for interacting with the Agent Core Service.
    *   **Integration:** Communicates with Agent Core Service via gRPC.

## 3. Key Design Decisions & Considerations

*   **Agent Core Technology:** Python with gRPC interface.
*   **Backend vs. Agent Core Separation:** Clear separation maintained. Backend handles user-facing aspects and data; Agent Core handles autonomous logic.
*   **Communication:**
    *   UI <-> Backend: REST API.
    *   Backend <-> Agent Core: gRPC (secured with TLS).
    *   Agent Core <-> Task Modules: Direct Python calls initially, consider gRPC if needed later.
    *   Task Modules <-> External Services: Standard API calls (REST, SDKs).
*   **Experiment Definition Schema:** Defined as messages (potentially using enums) within `proto/agent.proto`.
*   **State Management:** Experiment state persisted in MongoDB via Backend API. Agent Core uses in-memory state during execution.
*   **Autonomy Implementation:** Logic from `autonomy/` docs implemented in Agent Core. Notification/Approval flow: Agent Core -> Backend (gRPC) -> UI (REST/WebSockets). Rollback mechanisms considered in task design and approval flows.
*   **Error Handling:** Robust, layered error handling required.
*   **Deployment:** Frontend (Vercel), Backend (Render). Agent Core Service: Initial plan is co-location with Backend on Render (e.g., separate process or Docker container), evaluate need for separate deployment based on scaling/resources.
*   **Security:**
    *   **API Keys/Secrets:** Use environment variables initially (not committed to git). Plan to integrate a secrets manager (Render secrets, Vault, etc.) for better security as the project scales.
    *   **Inter-component Auth:** Secure Backend <-> Agent Core gRPC communication using TLS. Pass short-lived JWTs (with refresh mechanism) in gRPC metadata for authenticated requests originating from the user via the Backend.
*   **Monitoring & Alerting:**
    *   **Phase 1:** Implement basic gRPC health checks in Agent Core.
    *   **Phase 2:** Leverage Render's built-in monitoring for Backend/Agent Core.
    *   **Phase 3 (Future):** Consider Prometheus/Grafana for advanced metrics if needed.
    *   **Key Metrics:** CPU, memory, gRPC request latency/error rates, task execution times, experiment progress metrics.
*   **Testing:**
    *   Implement unit tests (`pytest` for Python, `Jest` for Node/React).
    *   Implement integration tests for key workflows (e.g., UI triggers experiment -> Backend -> Agent Core -> Task Module).
    *   Utilize mocking libraries for external services and inter-component communication during tests.
    *   Plan for CI (e.g., GitHub Actions) to automate testing.
*   **Interruptibility & Rollback:**
    *   Implement an immediate "kill switch" mechanism (e.g., gRPC call `StopAgent()`, UI button) to halt all agent activities.
    *   Design Task Execution Modules for idempotency or reversibility where possible.
    *   Log all agent actions meticulously for audit and potential manual rollback.
    *   Utilize database transactions in the Backend for atomic data updates where applicable.
    *   Enforce stricter human approval (via Autonomy Framework) for high-risk or irreversible actions (especially financial).

## 4. Next Steps (Phase 4 Detailed Plan - Integration Plan)

1.  **Refine Agent Core Service Interface (`proto/agent.proto`):**
    *   Define `ExperimentDefinition`, `ExperimentStatus`, `AgentStatus`, `LogEntry`, `DecisionId`, `Status` messages. Use `enums` where appropriate (e.g., `ExperimentType`, `ExperimentState`).
    *   Define `AgentService` RPC methods: `CreateExperiment`, `StartExperiment`, `StopExperiment`, `GetExperimentStatus`, `GetAgentStatus`, `GetLogs` (server-streaming), `ApproveDecision`, `StopAgent` (kill switch).
    *   Generate Python and Node.js gRPC code using `grpc_tools.protoc` and `@grpc/proto-loader`.
2.  **Implement Agent Core Service (Python - Initial Setup):**
    *   Set up basic Python project structure for the agent service.
    *   Implement gRPC server using `grpcio`.
    *   Implement stubbed versions of all `AgentService` methods.
    *   Set up basic logging using the `logging` module.
    *   Configure secure loading of environment variables (e.g., for Backend API URL, potential future secrets).
    *   Containerize using Docker (create `Dockerfile`).
3.  **Implement Task Execution Module (Ebook Generation):**
    *   Refactor `ebooks/generate_book.py` into a class or functions within a module (e.g., `task_modules/ebook_generator.py`).
    *   Modify it to accept parameters (topic, audience, etc.) and return results/status.
    *   Ensure secure handling of the `ABACUSAI_API_KEY`.
    *   Add basic error handling.
    *   Agent Core calls this module directly.
4.  **Integrate Backend with Agent Core (Initial):**
    *   Add `@grpc/grpc-js`, `@grpc/proto-loader` to backend `package.json`.
    *   Implement gRPC client logic in the backend to connect to the Agent Core Service (address from env vars).
    *   Create a simple Backend API endpoint (e.g., `/api/agent/status`) that calls the `GetAgentStatus` gRPC method on the Agent Core and returns the result.
    *   Implement basic TLS for the gRPC connection.
5.  **Deployment (Initial):**
    *   Update Render deployment configuration (`render.yaml`?) to potentially run the Python Agent Core service alongside the Node.js backend service, or as a separate service. Ensure environment variables are set.
6.  **Update Frontend (Initial):**
    *   Add a simple section/page to the dashboard.
    *   Call the new `/api/agent/status` backend endpoint.
    *   Display the agent status received from the backend.
7.  **Testing (Initial):**
    *   Write basic unit tests for the refactored ebook generator module.
    *   Write an integration test for the `/api/agent/status` flow (Frontend -> Backend -> Agent Core).

This detailed plan provides the initial steps for Phase 4, focusing on setting up the core communication and integrating one task module. Subsequent steps will involve implementing the remaining agent logic, task modules, and UI features.
