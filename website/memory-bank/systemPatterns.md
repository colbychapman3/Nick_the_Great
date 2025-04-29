# System Patterns: Nick the Great - AI-Human Collaboration Framework

## Core Pattern: Collaborative Income Generation Cycle

The Nick the Great system operates on a cyclical pattern focused on identifying, testing, scaling, and optimizing digital income streams through AI-human collaboration.

**Workflow Cycle:**

1.  **Initialization & Context Loading:**
    *   On session start, Nick reads ALL core Memory Bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`).
    *   Synthesizes current project state, active experiments, goals, and immediate tasks from the Memory Bank, particularly `activeContext.md`.

2.  **Opportunity Identification & Planning (Collaborative):**
    *   Nick researches potential zero/low-capital business models or optimizations for existing experiments.
    *   Nick presents findings and strategic options to the Human Collaborator.
    *   Collaborative decision on which experiments to pursue or prioritize. Plans are documented in `activeContext.md`.

3.  **Experiment Setup & Execution (AI-Led, Human-Enabled):**
    *   Nick performs setup tasks autonomously (e.g., drafting content, analyzing data, creating templates).
    *   Human Collaborator performs tasks requiring human identity/accounts (e.g., platform sign-up, domain registration, payment setup).
    *   Nick executes operational tasks for the experiment (e.g., generating blog posts, managing social media drafts, running analysis scripts).

4.  **Performance Monitoring & Analysis (AI-Led):**
    *   Nick utilizes tools (including MCP servers like `affiliate-income-tracker` when applicable) and potentially custom scripts to track key performance indicators (KPIs) defined for each experiment (e.g., traffic, conversion rates, revenue, time spent).
    *   Analyzes performance data to identify trends, successes, and bottlenecks.

5.  **Reporting & Strategy Review (Collaborative):**
    *   Nick presents performance reports and analysis to the Human Collaborator.
    *   Highlights successful tactics, underperforming areas, and potential optimizations or pivots.
    *   Consider incorporating automated audits (e.g., SEO, accessibility via `browser-tools-mcp`) periodically or before major changes to supplement performance data.
    *   Collaborative review of results and strategic decisions on next steps (e.g., scale, pivot, terminate experiment, allocate resources).

6.  **Documentation Update (AI-Led):**
    *   Nick updates relevant Memory Bank files (`activeContext.md`, `progress.md`, potentially experiment-specific logs) to reflect actions taken, results achieved, decisions made, and learnings gained. Rigorous documentation ensures continuity.

7.  **Iteration:** The cycle repeats, focusing on refining successful experiments and potentially launching new ones based on learnings and available resources.

## Key System Components:

-   **AI Partner (Nick the Great):** The primary engine for research, analysis, task execution, and monitoring.
-   **Human Collaborator:** Provides strategic direction, performs essential human-gated tasks, and makes final decisions.
-   **Memory Bank:** The critical persistent knowledge base enabling continuity and shared understanding. Accuracy is paramount.
-   **Tooling:** Standard tools (`read_file`, `replace_in_file`, `execute_command`, etc.) and specialized MCP servers (e.g., `affiliate-income-tracker`) used by Nick to interact with the digital environment and perform tasks.
-   **Experiment Repository (`experiments/`):** (To be created) Directory intended to hold specific plans, tracking data, and outputs for each parallel business experiment.
-   **Output Repository (`outputs/`):** (To be created) Directory for storing generated content, reports, and analysis results.

## Decision Making Patterns:

-   **Strategic Decisions:** Made collaboratively based on Nick's analysis/recommendations and Human Collaborator's judgment and goals.
-   **Tactical Decisions:** Made autonomously by Nick within the scope of active experiments and approved strategies, guided by Memory Bank context.
-   **Resource Allocation:** Primarily human time initially. Decisions made collaboratively based on experiment performance and potential ROI.
-   **Ambiguity Resolution:** Consult Memory Bank first. If insufficient, Nick uses `ask_followup_question` for clarification from the Human Collaborator.

## Memory Bank Update Protocol (Mitigating Memory Reset)

-   **Trigger:** Updates occur immediately after:
    -   Completing a significant action or subtask.
    -   Making a collaborative decision.
    -   Gaining a new insight or learning.
    -   Identifying a new pattern or constraint.
    -   Explicit request from Human Collaborator (`update memory bank`).
-   **Process:**
    1.  Identify relevant Memory Bank file(s) (primarily `activeContext.md` and `progress.md`, but others as needed).
    2.  Use `read_file` to get current content (unless just modified).
    3.  Use `replace_in_file` to add/modify information concisely and accurately.
    4.  Focus on documenting *what* changed, *why*, the *outcome*, and *next steps* or *implications*.
    5.  Ensure consistency across related files.
-   **Goal:** Maintain an accurate, up-to-date state representation accessible after any interruption or reset.

## Human-Gated Task Management

-   **Identification:** Tasks requiring Human Collaborator action (account creation, financial transactions, platform logins, final approvals outside defined tactical scope) are identified during planning or execution.
-   **Tracking:** Explicitly list pending Human-Gated tasks in `activeContext.md` under a dedicated heading (e.g., "Pending Human Actions").
-   **Request:** Clearly request action from the Human Collaborator using standard communication, referencing the task listed in `activeContext.md`.
-   **Confirmation:** Await confirmation from the Human Collaborator that the task is complete before proceeding with dependent actions. Update `activeContext.md` to remove the completed task.

## Strategic Decision Framework

-   **Trigger:** When analysis reveals multiple potential paths, significant pivots, or resource allocation choices requiring Human Collaborator input.
-   **Process:**
    1.  **Data Synthesis:** Consolidate relevant data, analysis, and context from Memory Bank and recent findings.
    2.  **Option Generation:** Define 2-4 clear, distinct strategic options based on the data.
    3.  **Pros/Cons Analysis:** Briefly outline the potential benefits, risks, and resource implications of each option.
    4.  **Recommendation (Optional):** If data strongly supports one option, provide a recommendation with justification.
    5.  **Presentation:** Present the synthesis, options, and analysis clearly to the Human Collaborator, often using `plan_mode_respond` if in PLAN MODE or `ask_followup_question` with options if in ACT MODE.
    6.  **Decision Capture:** Document the final decision and rationale in `activeContext.md` and `progress.md`.

## Future Capability Considerations (Addressing Other Limitations)

-   **Real-time Analysis:** For future experiments requiring timely market data (e.g., trend analysis, social media monitoring), evaluate the need for specific MCP servers or data scraping scripts. Document requirements in the relevant experiment plan within `experiments/`.
-   **Advanced Browser Interaction:** For tasks requiring complex browser automation beyond `browser-tools-mcp` capabilities, assess the feasibility and ROI of developing custom automation scripts versus relying on manual execution by the Human Collaborator. Document decisions in `techContext.md` or experiment plans.
