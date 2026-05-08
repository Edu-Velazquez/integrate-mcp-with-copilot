"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "state": "approved",
        "submitted_by": "system",
        "submitted_at": "2026-01-01T00:00:00Z",
        "reviewed_by": "system",
        "reviewed_at": "2026-01-01T00:00:00Z",
        "review_reason": "Seeded activity"
    }
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ActivitySubmission(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    schedule: str = Field(min_length=1)
    max_participants: int = Field(gt=0)
    submitted_by: str = Field(min_length=1)


class ActivityUpdateSubmission(BaseModel):
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = Field(default=None, gt=0)
    submitted_by: str = Field(min_length=1)


class ActivityReview(BaseModel):
    decision: Literal["approved", "rejected"]
    reviewed_by: str = Field(min_length=1)
    reason: str = ""


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return {name: details for name, details in activities.items() if details["state"] == "approved"}


@app.get("/activities/admin")
def get_all_activities_for_admin():
    return activities


@app.post("/activities/submit")
def submit_activity(activity: ActivitySubmission):
    if activity.name in activities:
        raise HTTPException(status_code=409, detail="Activity already exists")

    now = utc_now_iso()
    activities[activity.name] = {
        "description": activity.description,
        "schedule": activity.schedule,
        "max_participants": activity.max_participants,
        "participants": [],
        "state": "pending",
        "submitted_by": activity.submitted_by,
        "submitted_at": now,
        "reviewed_by": None,
        "reviewed_at": None,
        "review_reason": None,
    }
    return {
        "message": f"Submitted {activity.name} for approval",
        "state": "pending",
    }


@app.put("/activities/{activity_name}/submit-update")
def submit_activity_update(activity_name: str, update: ActivityUpdateSubmission):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if update.description is not None:
        activity["description"] = update.description
    if update.schedule is not None:
        activity["schedule"] = update.schedule
    if update.max_participants is not None:
        activity["max_participants"] = update.max_participants

    activity["state"] = "pending"
    activity["submitted_by"] = update.submitted_by
    activity["submitted_at"] = utc_now_iso()
    activity["reviewed_by"] = None
    activity["reviewed_at"] = None
    activity["review_reason"] = None

    return {
        "message": f"Submitted update for {activity_name} for approval",
        "state": "pending",
    }


@app.post("/activities/{activity_name}/review")
def review_activity(activity_name: str, review: ActivityReview):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    if review.decision == "rejected" and not review.reason.strip():
        raise HTTPException(status_code=400, detail="Reason is required when rejecting")

    activity = activities[activity_name]
    activity["state"] = review.decision
    activity["reviewed_by"] = review.reviewed_by
    activity["reviewed_at"] = utc_now_iso()
    activity["review_reason"] = review.reason.strip() or None

    return {
        "message": f"Activity {activity_name} {review.decision}",
        "state": review.decision,
        "reviewed_by": activity["reviewed_by"],
        "reviewed_at": activity["reviewed_at"],
        "review_reason": activity["review_reason"],
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Only approved activities are available publicly
    if activity["state"] != "approved":
        raise HTTPException(status_code=403, detail="Activity is not available for signup")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Only approved activities are available publicly
    if activity["state"] != "approved":
        raise HTTPException(status_code=403, detail="Activity is not available for unregister")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
