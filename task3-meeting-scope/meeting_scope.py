
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Meeting Scope Agent")

BASE_DIR = Path(__file__).parent


class MeetingRequest(BaseModel):
    notes: str


def analyze_meeting(notes: str):
    lines = [
        line.strip()
        for line in notes.splitlines()
        if line.strip()
    ]

    deliverables = []
    risks = []
    action_items = []
    requirements = []
    scope_changes = []

    for line in lines:
        lower_line = line.lower()

        # Detect possible scope changes
        if any(
            phrase in lower_line
            for phrase in [
                "scope change",
                "change request",
                "additional feature",
                "new requirement",
                "remove the feature",
                "instead of",
            ]
        ):
            scope_changes.append(line)

        if "deliverables:" in lower_line:
            deliverables.extend(
                item.strip()
                for item in line.split(":", 1)[1].split(",")
                if item.strip()
            )

        elif "risks:" in lower_line or "risk:" in lower_line:
            risks.append(line.split(":", 1)[1].strip())

        elif lower_line.startswith("action items:"):
            continue

        elif lower_line.startswith("- "):
            action_items.append(line[2:].strip())

        elif any(
            word in lower_line
            for word in ["agreed to", "should", "must", "need to"]
        ):
            requirements.append(line)

    project = next(
        (
            line.split(":", 1)[1].strip()
            for line in lines
            if line.lower().startswith("project:")
        ),
        "Unnamed Project",
    )

    deadline = next(
        (
            line.split(":", 1)[1].strip()
            for line in lines
            if line.lower().startswith("deadline:")
        ),
        "Not specified",
    )

    # Simple demonstration estimate, not a validated prediction
    estimated_hours = max(
        4,
        len(requirements) * 2
        + len(deliverables) * 3
        + len(action_items)
        + len(scope_changes) * 2,
    )

    return {
        "project": project,
        "requirements": requirements,
        "deliverables": deliverables,
        "risks": risks,
        "action_items": action_items,
        "deadline": deadline,
        "scope_changes": scope_changes,
        "effort_estimate": {
            "status": "Rough estimate only",
            "estimated_hours": estimated_hours,
            "note": (
                "Rule-based estimate for demonstration. "
                "Confirm complexity and dependencies with the project team."
            ),
        },
    }


@app.get("/")
def home():
    return {"message": "Meeting Scope Agent is running"}


@app.post("/analyze-meeting")
def analyze_meeting_endpoint(request: MeetingRequest):
    if not request.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Meeting notes cannot be empty",
        )

    return analyze_meeting(request.notes)


@app.post("/analyze-sample")
def analyze_sample():
    notes_path = BASE_DIR / "meeting_notes.txt"

    if not notes_path.exists():
        raise HTTPException(
            status_code=404,
            detail="meeting_notes.txt not found",
        )

    notes = notes_path.read_text(encoding="utf-8")
    return analyze_meeting(notes)
