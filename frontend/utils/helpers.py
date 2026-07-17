"""
utils/helpers.py
-----------------
Shared, reusable logic used across pages:

- Session state initialization
- Lightweight markdown parsing (score extraction, section splitting,
  bullet extraction) so raw AI markdown can be rendered as rich UI
  (rings, chips, timelines, accordions) instead of a plain text dump.
- Markdown / PDF export helpers for the "Download" buttons.

The Gemini responses are free-form markdown, not structured JSON, so all
parsing here is best-effort regex. Every renderer that depends on this
falls back gracefully to plain markdown if a pattern isn't found.
"""

from __future__ import annotations

import io
import re
from typing import Optional

import streamlit as st

from config import NAV_ITEMS


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def init_session_state() -> None:
    defaults = {
        "page": "dashboard",
        "resume_filename": None,
        "resume_analysis": None,
        "ats_result": None,
        "roadmap_result": None,
        "interview_result": None,
        "cover_letter_result": None,
        "linkedin_result": None,
        "chat_history": [],  # list of {"role": "user"|"ai", "content": str}
        "backend_online": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page_key: str) -> None:
    st.session_state["page"] = page_key


def has_resume() -> bool:
    return bool(st.session_state.get("resume_filename"))


def nav_label(page_key: str) -> str:
    for key, label, icon in NAV_ITEMS:
        if key == page_key:
            return f"{icon} {label}"
    return page_key


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------
_SCORE_PATTERNS = [
    r"(?:ATS\s*Score|Resume\s*Score|Score)[^\d]{0,15}(\d{1,3})\s*/\s*100",
    r"(\d{1,3})\s*/\s*100",
    r"(?:ATS\s*Score|Resume\s*Score|Score)[^\d]{0,15}(\d{1,3})\s*(?:%|percent)",
]


def extract_score(text: str) -> Optional[int]:
    """Best-effort extraction of a 0-100 score from free-form markdown."""
    if not text:
        return None
    for pattern in _SCORE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = int(match.group(1))
                return max(0, min(100, value))
            except ValueError:
                continue
    return None


# Heading detection covers common Gemini output styles:
#   "## 1. Professional Summary"    (markdown h2 with numbering)
#   "**1. Professional Summary**"   (bold numbered line)
#   "### Professional Summary"      (markdown h3)
#   "1. Professional Summary"       (plain numbered line, own paragraph)
_HEADING_RE = re.compile(
    r"^(?:#{1,4}\s*)?(?:\*\*)?\s*(\d+)[\.\)]\s*([A-Za-z][^\n*]{2,60}?)\s*(?:\*\*)?\s*:?\s*$",
    re.MULTILINE,
)


def split_numbered_sections(text: str) -> list[tuple[str, str]]:
    """
    Split markdown into (heading, body) pairs based on numbered headings.
    Returns an empty list if no numbered headings are found, so callers can
    fall back to rendering the raw markdown.
    """
    if not text:
        return []

    matches = list(_HEADING_RE.finditer(text))
    if not matches:
        return []

    sections: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        heading = match.group(2).strip().rstrip(":").strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((heading, body))
    return sections


def find_section(sections: list[tuple[str, str]], *keywords: str) -> Optional[str]:
    """Find the first section body whose heading contains any of the keywords."""
    for heading, body in sections:
        lowered = heading.lower()
        if any(k.lower() in lowered for k in keywords):
            return body
    return None


_BULLET_RE = re.compile(r"^\s*[-*•]\s+(.*)$", re.MULTILINE)
_INLINE_LIST_SPLIT_RE = re.compile(r",|;|\n")


def extract_bullets(text: str, max_items: int = 25) -> list[str]:
    """Pull bullet points out of a markdown section; falls back to comma/line split."""
    if not text:
        return []

    bullets = [b.strip(" *`") for b in _BULLET_RE.findall(text)]
    bullets = [b for b in bullets if b]

    if not bullets:
        # Fall back to splitting a flat inline list like "Python, SQL, AWS"
        candidate = text.strip()
        if len(candidate) < 400:
            parts = [p.strip(" .*`") for p in _INLINE_LIST_SPLIT_RE.split(candidate)]
            bullets = [p for p in parts if p and len(p) < 60]

    return bullets[:max_items]


_MONTH_HEADING_RE = re.compile(
    r"(Month\s*\d+[^\n:]{0,40}|Week\s*\d+[^\n:]{0,40}|Phase\s*\d+[^\n:]{0,40})\s*:?",
    re.IGNORECASE,
)


def split_timeline(text: str) -> list[tuple[str, str]]:
    """Split roadmap markdown into (Month/Phase label, body) chunks."""
    if not text:
        return []
    matches = list(_MONTH_HEADING_RE.finditer(text))
    if not matches:
        return []

    chunks: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        label = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip(" :\n-")
        if body:
            chunks.append((label, body))
    return chunks


_INTERVIEW_CATEGORY_ALIASES = {
    "hr": ["hr question"],
    "technical": ["technical question"],
    "coding": ["coding question"],
    "resume": ["resume-based", "resume based"],
    "project": ["project-based", "project based"],
    "scenario": ["scenario-based", "scenario based"],
}


def categorize_interview_sections(
    sections: list[tuple[str, str]]
) -> dict[str, Optional[str]]:
    """Map parsed sections onto the fixed interview-question categories."""
    result: dict[str, Optional[str]] = {k: None for k in _INTERVIEW_CATEGORY_ALIASES}
    for heading, body in sections:
        lowered = heading.lower()
        for key, aliases in _INTERVIEW_CATEGORY_ALIASES.items():
            if any(alias in lowered for alias in aliases):
                result[key] = body
    return result


# ---------------------------------------------------------------------------
# Downloads
# ---------------------------------------------------------------------------
def markdown_bytes(text: str) -> bytes:
    return (text or "").encode("utf-8")


def pdf_bytes(text: str, title: str = "AI Career Copilot") -> bytes:
    """Render plain/markdown text into a simple, readable PDF document."""
    from fpdf import FPDF  # local import keeps startup fast if unused
    from fpdf.enums import XPos, YPos

    clean_lines = _markdown_to_plain_lines(text)

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 27, 75)
    pdf.multi_cell(0, 10, _latin1_safe(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    for line in clean_lines:
        if line["style"] == "h":
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(88, 28, 135)
            pdf.ln(3)
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 41, 59)

        prefix = "- " if line["style"] == "bullet" else ""
        content = _latin1_safe(f"{prefix}{line['text']}")
        if not content.strip():
            continue
        pdf.multi_cell(0, 6.5, content, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    output = pdf.output()
    return bytes(output)


_LATIN1_REPLACEMENTS = {
    "\u2022": "-",   # bullet
    "\u2018": "'", "\u2019": "'",  # smart single quotes
    "\u201c": '"', "\u201d": '"',  # smart double quotes
    "\u2013": "-", "\u2014": "-",  # en/em dash
    "\u2026": "...",  # ellipsis
}


def _latin1_safe(text: str) -> str:
    """fpdf core fonts only support latin-1; normalize common unicode punctuation
    to ASCII equivalents first, then degrade any remaining unsupported glyphs."""
    for target, replacement in _LATIN1_REPLACEMENTS.items():
        text = text.replace(target, replacement)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _markdown_to_plain_lines(text: str) -> list[dict]:
    lines = []
    for raw in (text or "").splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            lines.append({"style": "h", "text": stripped.lstrip("#").strip()})
        elif re.match(r"^\*\*.*\*\*:?$", stripped):
            lines.append({"style": "h", "text": stripped.strip("*: ")})
        elif re.match(r"^[-*•]\s+", stripped):
            lines.append({"style": "bullet", "text": re.sub(r"^[-*•]\s+", "", stripped)})
        else:
            lines.append({"style": "p", "text": re.sub(r"[*_`#]", "", stripped)})
    return lines
