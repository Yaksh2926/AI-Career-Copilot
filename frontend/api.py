"""
api.py
------
Thin HTTP client around the existing FastAPI backend.

This module does NOT invent new endpoints, does NOT change request/response
shapes, and does NOT touch backend code. It simply calls the routes exposed by
`app/routes/resume.py`:

    GET  /resume                -> health check
    POST /upload-resume         -> multipart file upload
    POST /ats-score             -> {filename, job_description}
    POST /career-roadmap        -> {filename, career_goal}
    POST /interview-questions   -> {filename, role}
    POST /cover-letter          -> {filename, company_name, job_role}
    POST /linkedin-profile      -> {filename}
    POST /career-chat           -> {question}

Every public function returns a tuple: (ok: bool, payload: dict | str)
- If ok is True, payload is the parsed JSON response from the backend.
- If ok is False, payload is a short, human-readable error message
  (never a raw traceback) suitable for display in the UI.
"""

from __future__ import annotations

import requests

from config import BACKEND_URL, REQUEST_TIMEOUT


class APIError(Exception):
    """Raised internally, always converted to a friendly message before returning."""


def _friendly_error(exc: Exception) -> str:
    """Translate low-level exceptions into short, user-safe messages."""
    if isinstance(exc, requests.exceptions.ConnectTimeout):
        return "The AI Career Copilot backend took too long to respond. Please try again."
    if isinstance(exc, requests.exceptions.ConnectionError):
        return (
            f"Couldn't reach the backend at {BACKEND_URL}. "
            "Make sure the FastAPI server is running."
        )
    if isinstance(exc, requests.exceptions.Timeout):
        return "The request timed out while the AI was thinking. Please try again."
    if isinstance(exc, requests.exceptions.HTTPError):
        return str(exc)
    return "Something went wrong while talking to the backend."


def _extract_detail(response: requests.Response) -> str:
    """Pull FastAPI's `detail` field out of an error response, if present."""
    try:
        body = response.json()
        if isinstance(body, dict) and "detail" in body:
            return str(body["detail"])
    except ValueError:
        pass
    return f"Request failed with status {response.status_code}."


def _get(path: str) -> tuple[bool, dict | str]:
    try:
        resp = requests.get(f"{BACKEND_URL}{path}", timeout=REQUEST_TIMEOUT)
        if not resp.ok:
            return False, _extract_detail(resp)
        return True, resp.json()
    except Exception as exc:  # noqa: BLE001 - we deliberately catch broadly here
        return False, _friendly_error(exc)


def _post_json(path: str, payload: dict) -> tuple[bool, dict | str]:
    try:
        resp = requests.post(
            f"{BACKEND_URL}{path}", json=payload, timeout=REQUEST_TIMEOUT
        )
        if not resp.ok:
            return False, _extract_detail(resp)
        return True, resp.json()
    except Exception as exc:  # noqa: BLE001
        return False, _friendly_error(exc)


def health_check() -> tuple[bool, dict | str]:
    """Ping the backend to confirm it's alive."""
    return _get("/resume")


def upload_resume(file_bytes: bytes, filename: str, content_type: str) -> tuple[bool, dict | str]:
    """Upload a PDF resume. Returns backend's {success, message, data:{filename, analysis}}."""
    try:
        files = {"file": (filename, file_bytes, content_type)}
        resp = requests.post(
            f"{BACKEND_URL}/upload-resume", files=files, timeout=REQUEST_TIMEOUT
        )
        if not resp.ok:
            return False, _extract_detail(resp)
        return True, resp.json()
    except Exception as exc:  # noqa: BLE001
        return False, _friendly_error(exc)


def ats_score(filename: str, job_description: str) -> tuple[bool, dict | str]:
    return _post_json(
        "/ats-score", {"filename": filename, "job_description": job_description}
    )


def career_roadmap(filename: str, career_goal: str) -> tuple[bool, dict | str]:
    return _post_json(
        "/career-roadmap", {"filename": filename, "career_goal": career_goal}
    )


def interview_questions(filename: str, role: str) -> tuple[bool, dict | str]:
    return _post_json(
        "/interview-questions", {"filename": filename, "role": role}
    )


def cover_letter(filename: str, company_name: str, job_role: str) -> tuple[bool, dict | str]:
    return _post_json(
        "/cover-letter",
        {"filename": filename, "company_name": company_name, "job_role": job_role},
    )


def linkedin_profile(filename: str) -> tuple[bool, dict | str]:
    return _post_json("/linkedin-profile", {"filename": filename})


def career_chat(question: str) -> tuple[bool, dict | str]:
    return _post_json("/career-chat", {"question": question})
