import json
import subprocess
import sys

REPO = "skills/integrate-mcp-with-copilot"

ISSUES = [
    (
        "Add authentication and session management",
        "Implement user login/logout with secure session handling so actions are tied to authenticated users.\n\n"
        "Acceptance criteria:\n"
        "- Login endpoint and UI form exist\n"
        "- Invalid credentials show clear error\n"
        "- Authenticated session persists across page refresh\n"
        "- Logout clears session\n",
    ),
    (
        "Implement role-based access control (admin, club leader, student)",
        "Add roles and permissions so privileged actions (manage activities/users) are restricted.\n\n"
        "Acceptance criteria:\n"
        "- Roles are stored per user\n"
        "- Unauthorized actions return 403\n"
        "- UI hides restricted controls for non-privileged users\n"
        "- At least one admin seed user exists\n",
    ),
    (
        "Create activity approval workflow",
        "Allow submitted activities or updates to be reviewed by admins before publication.\n\n"
        "Acceptance criteria:\n"
        "- New activity state includes pending/approved/rejected\n"
        "- Admin can approve/reject with reason\n"
        "- Only approved activities are visible publicly\n"
        "- Audit metadata is stored (who/when)\n",
    ),
    (
        "Build join and leave request flow for clubs",
        "Replace direct membership changes with request/approval flow for better control.\n\n"
        "Acceptance criteria:\n"
        "- Students can request join/leave\n"
        "- Admin/club leader can approve or reject\n"
        "- Request status is visible to requester\n"
        "- Membership updates only on approval\n",
    ),
    (
        "Add announcements and news module",
        "Create a school news/announcements section for events and updates.\n\n"
        "Acceptance criteria:\n"
        "- Admin can create/edit/delete announcements\n"
        "- Announcements are listed on homepage\n"
        "- Each item includes title, body, created date\n"
        "- Older announcements are still accessible\n",
    ),
    (
        "Add reporting dashboard for activities",
        "Provide summary metrics (enrollments, remaining slots, activity popularity).\n\n"
        "Acceptance criteria:\n"
        "- Dashboard endpoint returns aggregate stats\n"
        "- UI card(s) show top activities and enrollment counts\n"
        "- Data refreshes after signup/unregister actions\n"
        "- Empty-state handling is included\n",
    ),
    (
        "Add CSV export for participants and activities",
        "Allow admins to export activity and participant data for offline processing.\n\n"
        "Acceptance criteria:\n"
        "- Export endpoint returns CSV with headers\n"
        "- Supports exporting all activities and a single activity\n"
        "- Download action is available in UI\n"
        "- Character encoding is UTF-8\n",
    ),
    (
        "Persist data in a real database",
        "Migrate in-memory activities and participants to persistent storage (SQLite/Postgres).\n\n"
        "Acceptance criteria:\n"
        "- Data survives server restart\n"
        "- CRUD endpoints keep current behavior\n"
        "- Basic migrations or schema init included\n"
        "- README updated with setup instructions\n",
    ),
    (
        "Implement profile management for users",
        "Allow users to view and update profile details and preferences.\n\n"
        "Acceptance criteria:\n"
        "- Profile page with editable fields\n"
        "- Validation for required fields\n"
        "- Changes persist in backend\n"
        "- Unauthorized profile edits are blocked\n",
    ),
    (
        "Add bulk email notifications for activity updates",
        "Send notifications to participants when schedules or activity info changes.\n\n"
        "Acceptance criteria:\n"
        "- Admin can trigger email to activity participants\n"
        "- Email template supports activity name and schedule\n"
        "- Delivery result is logged (success/failure count)\n"
        "- Feature can be disabled via configuration\n",
    ),
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


existing_proc = run(["gh", "issue", "list", "--repo", REPO, "--limit", "200", "--json", "title,url"])
if existing_proc.returncode != 0:
    print(existing_proc.stderr.strip())
    sys.exit(existing_proc.returncode)

existing = {item["title"]: item["url"] for item in json.loads(existing_proc.stdout or "[]")}
created = []
skipped = []

for title, body in ISSUES:
    if title in existing:
        skipped.append((title, existing[title]))
        continue

    proc = run(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body])
    if proc.returncode != 0:
        print(f"ERROR creating: {title}\n{proc.stderr.strip()}")
        continue

    url = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    created.append((title, url))

print("CREATED")
for title, url in created:
    print(f"- {title} | {url}")

print("SKIPPED")
for title, url in skipped:
    print(f"- {title} | {url}")

# Final fresh list
final_proc = run(["gh", "issue", "list", "--repo", REPO, "--limit", "200", "--json", "number,title,url,state"])
print("FINAL")
print(final_proc.stdout.strip())
