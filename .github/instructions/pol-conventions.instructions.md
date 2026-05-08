---
applyTo: "src/**"
---
# Repository Coding Conventions

## Stack
- Backend: FastAPI (Python 3.9)
- In-memory storage (migrating to SQLite via issue #8)
- Frontend: Vanilla JS + static HTML/CSS served by FastAPI StaticFiles

## Patterns to follow
- Activity records always include: description, schedule, max_participants, participants, state, submitted_by, submitted_at, reviewed_by, reviewed_at, review_reason
- Activity states: `pending`, `approved`, `rejected`
- Public endpoints return only `approved` activities
- Admin endpoints are prefixed or named with `/admin`
- Use `HTTPException` for all error responses with appropriate status codes
- Pydantic models for all request bodies

## Git conventions
- Feature branches: `pol/<issue>-<desc>` (Pol agent) or `issue-<n>-<desc>` (manual)
- Commit messages: `feat: <description> (closes #<n>)`
- Never commit directly to `main`
- Push remote for this repo: `mine` (https://github.com/Edu-Velazquez/integrate-mcp-with-copilot.git)
