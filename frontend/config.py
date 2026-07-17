"""
config.py
---------
Central configuration for the AI Career Copilot frontend.
Holds the backend base URL, brand palette, and static page metadata.
No business logic lives here — only constants.
"""

import os

# ---------------------------------------------------------------------------
# Backend connection
# ---------------------------------------------------------------------------
# The FastAPI backend is NOT modified. We only point at wherever it's running.
# Override with an environment variable if the backend runs on another host/port,
# e.g. `export BACKEND_URL=http://127.0.0.1:8000`
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 180  # seconds — Gemini generations can take a while

# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------
APP_NAME = "AI Career Copilot"
APP_TAGLINE = "Build Your Career With AI"

# ---------------------------------------------------------------------------
# Color palette (kept in sync with assets/styles.css)
# ---------------------------------------------------------------------------
PALETTE = {
    "primary": "#7C3AED",
    "accent": "#A855F7",
    "secondary": "#06B6D4",
    "background": "#0F172A",
    "card": "rgba(255,255,255,.08)",
    "success": "#22C55E",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
}

# ---------------------------------------------------------------------------
# Navigation / Pages
# ---------------------------------------------------------------------------
# key -> (label, icon)  — order defines sidebar order
NAV_ITEMS = [
    ("dashboard", "Dashboard", "🏠"),
    ("resume", "Resume Analysis", "📄"),
    ("ats", "ATS Score", "🎯"),
    ("roadmap", "Career Roadmap", "🗺️"),
    ("interview", "Interview Prep", "🧠"),
    ("cover_letter", "Cover Letter", "✉️"),
    ("linkedin", "LinkedIn Optimizer", "💼"),
    ("chat", "Career Chat", "💬"),
]

SETTINGS_ITEM = ("settings", "Settings", "⚙️")
ABOUT_ITEM = ("about", "About", "ℹ️")

# Feature cards shown on the dashboard
FEATURE_CARDS = [
    {
        "key": "resume",
        "icon": "📄",
        "title": "Resume Analysis",
        "desc": "Deep AI review of your resume — strengths, weaknesses, and a score.",
    },
    {
        "key": "ats",
        "icon": "🎯",
        "title": "ATS Score",
        "desc": "Match your resume against a job description like a real ATS.",
    },
    {
        "key": "roadmap",
        "icon": "🗺️",
        "title": "Career Roadmap",
        "desc": "A month-by-month learning plan tailored to your goal.",
    },
    {
        "key": "interview",
        "icon": "🧠",
        "title": "Interview Questions",
        "desc": "HR, technical, coding, and scenario-based questions, auto-generated.",
    },
    {
        "key": "cover_letter",
        "icon": "✉️",
        "title": "Cover Letter",
        "desc": "A polished, role-specific cover letter in seconds.",
    },
    {
        "key": "linkedin",
        "icon": "💼",
        "title": "LinkedIn Optimizer",
        "desc": "Headline, About section, skills, and SEO keywords that get noticed.",
    },
    {
        "key": "chat",
        "icon": "💬",
        "title": "Career Chat",
        "desc": "Talk it through with an AI career mentor, anytime.",
    },
]
