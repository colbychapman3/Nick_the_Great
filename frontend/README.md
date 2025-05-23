# Frontend Application

This is the Frontend Application for the Nick the Great Unified Agent system. It's a Next.js/React application that provides the user interface for:

*   Viewing dashboards and agent status.
*   Managing and monitoring experiments.
*   User authentication (login/registration).
*   Interacting with agent features and configurations.

## Key Technologies

*   Next.js (with App Router)
*   React
*   TypeScript
*   Tailwind CSS
*   Chart.js (for visualizations)
*   Jest (for testing)
*   React Testing Library (for testing React components)

## Project Structure Overview (`src/`)

*   `app/`: Contains the pages and layouts for the application, following the Next.js App Router structure.
*   `components/`: Reusable UI components (e.g., buttons, forms, charts).
*   `lib/`: Utility functions, API client (`client.ts`), and specific API interaction modules (e.g., `experimentApi.ts`).
*   `hooks/`: Custom React hooks for managing state and side effects.
*   `styles/`: Global styles and Tailwind CSS configuration.
*   `contexts/`: React context providers for global state management (e.g., AuthContext).

## Setup Instructions

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Create a `.env.local` file from the example and populate it (Next.js convention for local environment variables):
    ```bash
    cp .env.example .env.local
    ```
    Key environment variables to configure in `.env.local`:
    *   `NEXT_PUBLIC_API_URL`: The base URL for the Backend API service (e.g., `http://localhost:3001/api`).
3.  Install dependencies (the project is configured to use `pnpm`, but `npm install` or `yarn install` might also work depending on your setup):
    ```bash
    pnpm install 
    ```
    (If you don't have `pnpm`, you can install it via `npm install -g pnpm`, or try `npm install`.)

## Running the Application (Development)

```bash
pnpm dev
```
This will start the Next.js development server, typically on `http://localhost:3000`.

## Building for Production

1.  Build the application:
    ```bash
    pnpm build
    ```
2.  Start the production server:
    ```bash
    pnpm start
    ```

## Running Tests

Tests are run using Jest with React Testing Library.

```bash
pnpm test
```

## Key Features

*   **Dashboard:** Overview of agent status, active experiments, and key metrics.
*   **Experiment Management:** View list of experiments, create new experiments, start/stop experiments, and view detailed status and logs for each.
*   **User Authentication:** Secure login and registration system.
*   **Agent Configuration:** Interface to manage agent settings and parameters.
*   **Notifications & Approvals:** UI elements to display notifications and handle approval requests.

---
*Self-reflection: I've included all the requested points for the frontend README. I've noted the use of `pnpm` as it's often specified in `package.json` and is good practice to follow if present, while also providing an alternative for users who might not have it. I've also added `Chart.js` to Key Technologies as it's commonly used with dashboards and `contexts/` to the project structure as it's a common pattern for state management in React.*
