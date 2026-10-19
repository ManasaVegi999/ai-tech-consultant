import json
from datetime import datetime, timezone
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_FOLDER = PROJECT_ROOT / "task1-knowledge-brain"

load_dotenv(PROJECT_ROOT / ".env")

sys.path.insert(0, str(KNOWLEDGE_FOLDER))
from knowledge_brain import search_articles

app = FastAPI(title="AI Tech Consultant - Inbox Agent")


class EmailRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1, max_length=10000)


@app.get("/")
def home():
    return {"message": "Inbox Agent is running"}


@app.post("/draft-reply")
def draft_reply(email: EmailRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing from the project .env file",
        )

    query = f"{email.subject}\n{email.body}"
    articles = search_articles(query, limit=5)

    context = "\n\n".join(
        f"Title: {item['title']}\n"
        f"URL: {item['url']}\n"
        f"Content: {item['excerpt']}"
        for item in articles
    )

    if not context:
        context = "No matching support articles were found."

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=(
                "You are a customer support assistant for Brilliant Directories. "
                "Draft a polite, concise email reply to the customer. "
                "Use the support articles below only when relevant. "
                "Never invent product features, policies, prices, or completed actions. "
                "If information is insufficient, say the support team should confirm it. "
                "Do not send the email; return only a draft for human review.\n\n"
                f"Customer email subject: {email.subject}\n"
                f"Customer email body: {email.body}\n\n"
                f"Support articles:\n{context}"
            ),
        )

        return {
            "subject": email.subject,
            "draft_reply": response.text or "No draft was generated.",
            "requires_human_review": True,
            "sources": [
                {"title": item["title"], "url": item["url"]}
                for item in articles
            ],
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not generate a draft: {type(error).__name__}",
        )
FEEDBACK_FILE = Path(__file__).parent / "feedback.json"


class FeedbackRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=300)
    rating: str = Field(pattern="^(helpful|not_helpful)$")
    comments: str = Field(default="", max_length=2000)


@app.post("/feedback")
def save_feedback(feedback: FeedbackRequest):
    records = []

    if FEEDBACK_FILE.exists():
        try:
            records = json.loads(
                FEEDBACK_FILE.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            raise HTTPException(
                status_code=500,
                detail="Could not read the feedback file",
            )

    records.append({
        "subject": feedback.subject,
        "rating": feedback.rating,
        "comments": feedback.comments,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    FEEDBACK_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return {
        "message": "Feedback saved successfully",
        "feedback_count": len(records),
    }