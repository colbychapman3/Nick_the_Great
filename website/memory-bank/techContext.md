# Tech Context: Nick the Great Project

## Core Operating Environment

-   **Execution Environment:** VS Code Extension Host (providing tools and environment details).
-   **Communication Protocol:** Proprietary protocol between VS Code extension and backend model (Nick).
-   **Memory Bank Format:** Markdown (`.md`) files, critical for maintaining state.

## Development Setup

-   **Project Root:** `c:/Users/colby/Documents/Manus Downloads/Nick the Great/Nick_the_Great/`
-   **Current Experiment CWD:** `c:/Users/colby/Documents/Manus Downloads/Nick the Great/Nick_the_Great/website` (Tool paths are relative to this CWD unless specified otherwise).
-   **Operating System:** Windows 11 (Commands must be `cmd.exe` compatible).
-   **Shell:** `C:\Windows\System32\cmd.exe`.

## Current Experiment Tech Stack (The Indoor Eden Co. Website)

-   **Languages:** HTML5, CSS3 (potentially basic JavaScript later).
-   **Structure:** Static HTML files (`index.html`, `about.html`, etc.) linked via relative paths.
-   **Styling:** Single CSS file (`css/style.css`) using CSS variables for theming.
-   **Monetization:** Primarily Amazon Associates affiliate links (requires external account setup).
-   **Hosting:** Dual implementation:
    - Local files (static HTML) suitable for various hosting platforms (Netlify, Vercel, GitHub Pages, etc.)
    - Live WordPress site at https://theindooreden.wordpress.com/ (discovered and confirmed 4/12/2025)
-   **UI Replica:** Created `wordpress-replica.html` and `css/wordpress-style.css` to replicate the live WordPress site UI for reference purposes.

## Available Tools (Core - Nick's Capabilities)

-   `execute_command`: Run CLI commands (e.g., potentially build steps, git commands if repo initialized).
-   `read_file`: Read Memory Bank, HTML, CSS, and other project files.
-   `write_to_file`: Create new files (e.g., new blog posts, experiment logs) or overwrite existing ones.
-   `replace_in_file`: Make targeted edits to Memory Bank, HTML, CSS. Crucial for iterative development and documentation updates.
-   `search_files`: Find specific code patterns, content snippets, or references across the website files.
-   `list_files`: Explore directory structures (e.g., `img/`, `experiments/`).
-   `list_code_definition_names`: Less relevant for current static HTML/CSS site, but useful if JS or backend code is added.
-   `ask_followup_question`: Request clarification or necessary input from the Human Collaborator.
-   `attempt_completion`: Signal completion of a defined task or subtask.
-   `new_task`: Propose breaking down larger tasks.
-   `plan_mode_respond`: Used for collaborative planning (PLAN MODE only).
-   `load_mcp_documentation`: Available if needed to create new MCP tools.

## Available Tools (MCP - Specialized Capabilities)

-   **affiliate-income-tracker:** Highly relevant for monitoring website monetization success once Amazon Associates is active. Tools: `get_amazon_earnings`, `analyze_affiliate_performance`, `monitor_key_metrics`, `generate_income_report`, `optimize_affiliate_strategy`.
-   **financial-market-data:** Not directly relevant to the current website experiment.
-   **news-sentiment:** Not directly relevant to the current website experiment.
-   **github.com/AgentDeskAI/browser-tools-mcp:** **OPERATIONAL (4/12/2025).** Requires `@agentdeskai/browser-tools-server` (connector) to run on port 3025 (127.0.0.1:3025) and the Chrome extension to be properly installed. Successfully conducts accessibility and SEO audits on published websites only (cannot audit local development environments), though screenshot functionality still reports "Chrome extension not connected" errors.
    -   **Accessibility Audit Results:** Successfully tested on live WordPress site (https://theindooreden.wordpress.com/). Score 93/100 with only one critical issue: insufficient color contrast on the "Subscribe" button text.
    -   **SEO Audit Results:** Successfully tested on live WordPress site. Score 82/100 with two issues: missing meta description and non-descriptive link text.
-   *(Capability to create/install new MCP servers exists if specialized tools are required)*

## Constraints & Considerations

-   **Memory Reset:** Nick's state is lost between sessions; the Memory Bank is the *only* source of persistent context. Must be kept meticulously updated.
-   **Tool Atomicity:** Each tool use is discrete. Wait for confirmation/results before proceeding.
-   **Path Relativity:** File paths are relative to the CWD (`website/`). Use `../` or full paths if accessing files outside this directory (e.g., main project `README.md`).
-   **Auto-formatting:** Edits via `replace_in_file` or `write_to_file` might trigger auto-formatting. Always use the `final_file_content` from the tool result as the basis for subsequent `SEARCH` blocks.
-   **Command Execution:** Commands run in the CWD. Use `cd ... && ...` for other directories if needed.
-   **Human-Gated Tasks:** Nick cannot perform actions requiring human accounts (e.g., signing up for Amazon Associates, Google Analytics) or direct financial transactions. These require Human Collaborator action.
-   **Tool Reliability (`search_files`):** Encountered issues (4/12/2025) where `search_files` failed to find expected patterns (`href` attributes in `<a>` tags) in HTML files. Workaround: Use `read_file` on individual files and manually parse content when `search_files` yields unexpected negative results for known content.
-   **Visual Understanding:** Cannot visually interpret rendered web pages directly. Mitigation strategies:
    -   **For Published Site:** Use `github.com/AgentDeskAI/browser-tools-mcp` audit tools (accessibility, SEO, etc.) to objectively measure site quality on https://theindooreden.wordpress.com/. Confirmed working on 4/12/2025.
    -   **For Local Development:** Created WordPress UI replica (`wordpress-replica.html`) for reference, and rely on Human Collaborator feedback for visual assessment.
    -   **Screenshot Limitation:** Screenshot functionality remains non-operational despite multiple attempts and connector server running on port 3025 or 3026.
