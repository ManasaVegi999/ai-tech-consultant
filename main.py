import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

app = FastAPI(title="AI Tech Consultant")
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(PROJECT_ROOT / "task1-knowledge-brain"))
sys.path.insert(0, str(PROJECT_ROOT / "task2-inbox-agent"))
sys.path.insert(0, str(PROJECT_ROOT / "task3-meeting-scope"))

from knowledge_api import app as knowledge_app
from inbox_agent import app as inbox_app
from meeting_scope import app as meeting_app

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Tech Consultant is running!"}


@app.post("/ask")
def ask_ai(data: Question):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing. Check your .env file."
        )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=data.question
        )
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
app.mount("/knowledge", knowledge_app)
app.mount("/inbox", inbox_app)
app.mount("/meeting", meeting_app)