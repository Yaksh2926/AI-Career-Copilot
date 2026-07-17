from fastapi import FastAPI
from app.routes.resume import router as resume_router

app = FastAPI(
    title="AI Career Copilot API",
    description="""
## 🚀 AI Career Copilot Backend

This API provides AI-powered career services including:

- Resume Analysis
- ATS Score
- Career Roadmap
- Interview Question Generator
- Cover Letter Generator
- LinkedIn Profile Generator
- AI Career Chat

Built with **FastAPI** and **Google Gemini AI**.
""",
    version="1.0.0",
    contact={
        "Name": "Yaksh Jindal",
        "Email": "yakshjindal29022008@gmail.com"
    }
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Career Copilot"
    }


app.include_router(resume_router)