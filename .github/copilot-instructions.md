# Mergington High School Activity Platform

## Custom Agents
- **Pol** — autonomous issue implementation agent. Invoke with `@Pol <issue-number>` to have it fully implement a GitHub issue end-to-end.
- **Pol PR behavior** — when a `pol`-triggered draft PR already exists, Pol should reuse it, update the checklist as work progresses, add milestone comments when useful, and mark it ready for review when implementation is complete.

## Repository Layout
- `src/app.py` — FastAPI application, all routes and data
- `src/static/` — Frontend (index.html, app.js, styles.css)
- `requirements.txt` — Python dependencies
- `test/` — Tests and QA scripts

## Push Remote
This repository uses `mine` as the writable remote:
`https://github.com/Edu-Velazquez/integrate-mcp-with-copilot.git`
`origin` points to the read-only skills template.

## MCP Integration
The GitHub MCP server is configured in `.vscode/mcp.json` and provides GitHub API tools (issues, PRs, labels, milestones) directly inside the agent.
