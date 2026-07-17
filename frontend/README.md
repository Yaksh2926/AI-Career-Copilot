# AI Career Copilot — Frontend

A premium, Streamlit-only frontend for the existing AI Career Copilot FastAPI backend.
This project does **not** modify the backend, its endpoints, or its request/response formats — it only consumes them.

## 1. Install dependencies

```bash
cd frontend
pip install -r requirements.txt
```

## 2. Make sure the backend is running

The frontend expects the FastAPI backend at `http://127.0.0.1:8000` by default
(the standard `uvicorn app.main:app` address). If your backend runs elsewhere,
set the `BACKEND_URL` environment variable before launching Streamlit:

```bash
# Windows (PowerShell)
$env:BACKEND_URL = "http://127.0.0.1:8000"

# macOS / Linux
export BACKEND_URL=http://127.0.0.1:8000
```

## 3. Run the app

```bash
streamlit run frontend/app.py
```

The app opens at `http://localhost:8501`.

## Project structure

```
frontend/
├── app.py                 # Entry point — sidebar nav + page routing
├── config.py               # Backend URL, palette, nav/feature metadata
├── api.py                  # HTTP client for the FastAPI backend
├── theme.py                 # Injects the design system (CSS)
├── assets/
│   └── styles.css           # Dark glassmorphism design system
├── components/               # Reusable UI building blocks
│   ├── navbar.py
│   ├── hero.py
│   ├── feature_cards.py
│   ├── uploader.py
│   ├── result_view.py
│   ├── loading.py
│   └── footer.py
├── pages/                    # One module per feature
│   ├── dashboard.py
│   ├── resume.py
│   ├── ats.py
│   ├── roadmap.py
│   ├── interview.py
│   ├── cover_letter.py
│   ├── linkedin.py
│   └── chat.py
└── utils/
    └── helpers.py            # Session state + markdown parsing + export helpers
```

## Notes

- Upload your resume once on the Dashboard — every other page reuses the stored filename automatically.
- The backend's Gemini responses are free-form markdown; the frontend does best-effort parsing
  (scores, skill lists, month-by-month roadmap items, interview categories) and gracefully falls
  back to clean markdown rendering if a pattern isn't detected.
- Every generated result can be copied, downloaded as Markdown, or downloaded as PDF.
