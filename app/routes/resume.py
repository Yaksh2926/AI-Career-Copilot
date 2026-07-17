import os

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.logger import logger

from app.models import (
    JobDescriptionRequest,
    CareerRoadmapRequest,
    InterviewQuestionRequest,
    CoverLetterRequest,
    LinkedInRequest,
    ChatRequest,
)

from app.services.file_service import save_uploaded_file
from app.services.pdf_parser import extract_text_from_pdf

from app.services.gemini import (
    analyze_resume,
    ats_score,
    career_roadmap,
    interview_questions,
    generate_cover_letter,
    generate_linkedin_profile,
    career_chat,
)

router = APIRouter()


@router.get(
    "/resume",
    summary="Resume API Status",
    description="Check whether the Resume API is running.",
    tags=["Resume"],
)
def resume_home():
    """
    Health Check Endpoint
    """

    logger.info("Resume API Status Checked")

    return {
        "success": True,
        "message": "Resume API Working"
    }


@router.post(
    "/upload-resume",
    summary="Upload Resume",
    description="Upload a PDF resume and receive AI-powered resume analysis.",
    tags=["Resume"],
)
def upload_resume(file: UploadFile = File(...)):
    """
    Upload Resume
    Extract Resume Text
    Analyze Resume using Gemini
    """

    logger.info("Upload Resume API Called")

    if file.content_type != "application/pdf":
        logger.warning("Invalid file uploaded.")

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:

        file_path = save_uploaded_file(file)

        logger.info(f"Resume saved successfully: {file.filename}")

        extracted_text = extract_text_from_pdf(file_path)

        logger.info("Resume text extracted successfully.")

        analysis = analyze_resume(extracted_text)

        logger.info("Resume analysis completed.")

        return {
            "success": True,
            "message": "Resume uploaded successfully.",
            "data": {
                "filename": file.filename,
                "analysis": analysis
            }
        }

    except Exception as e:

        logger.exception("Resume Analysis Failed")

        raise HTTPException(
            status_code=500,
            detail=f"AI Analysis Failed: {str(e)}"
        )


@router.post(
    "/ats-score",
    summary="Generate ATS Score",
    description="Compare the uploaded resume with a job description.",
    tags=["ATS"],
)
def get_ats_score(request: JobDescriptionRequest):
    """
    Generate ATS Score
    """

    logger.info("ATS API Called")

    file_path = f"uploads/{request.filename}"

    if not os.path.exists(file_path):

        logger.warning(f"File not found: {request.filename}")

        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found."
        )

    extracted_text = extract_text_from_pdf(file_path)

    try:

        logger.info("Generating ATS Score...")

        result = ats_score(
            extracted_text,
            request.job_description
        )

        logger.info("ATS Score Generated Successfully.")

        return {
            "success": True,
            "message": "ATS Analysis Generated",
            "data": {
                "filename": request.filename,
                "ats_analysis": result
            }
        }

    except Exception as e:

        logger.exception("ATS Analysis Failed")

        raise HTTPException(
            status_code=500,
            detail=f"ATS Analysis Failed: {str(e)}"
        )


@router.post(
    "/career-roadmap",
    summary="Career Roadmap",
    description="Generate an AI-powered learning roadmap.",
    tags=["Career"],
)
def generate_career_roadmap(request: CareerRoadmapRequest):
    """
    Generate Career Roadmap
    """

    logger.info("Career Roadmap API Called")

    file_path = f"uploads/{request.filename}"

    if not os.path.exists(file_path):

        logger.warning(f"File not found: {request.filename}")

        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found."
        )

    extracted_text = extract_text_from_pdf(file_path)

    try:

        logger.info("Generating Career Roadmap...")

        result = career_roadmap(
            extracted_text,
            request.career_goal
        )

        logger.info("Career Roadmap Generated Successfully.")

        return {
            "success": True,
            "message": "Career Roadmap Generated",
            "data": {
                "filename": request.filename,
                "career_goal": request.career_goal,
                "roadmap": result
            }
        }

    except Exception as e:

        logger.exception("Career Roadmap Generation Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Career Roadmap Generation Failed: {str(e)}"
        )
@router.post(
    "/interview-questions",
    summary="Interview Questions",
    description="Generate HR, technical, coding and project-based interview questions.",
    tags=["Interview"],
)
def generate_interview_questions(request: InterviewQuestionRequest):
    """
    Generate Interview Questions
    """

    logger.info("Interview Questions API Called")

    file_path = f"uploads/{request.filename}"

    if not os.path.exists(file_path):

        logger.warning(f"File not found: {request.filename}")

        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found."
        )

    extracted_text = extract_text_from_pdf(file_path)

    try:

        logger.info("Generating Interview Questions...")

        result = interview_questions(
            extracted_text,
            request.role
        )

        logger.info("Interview Questions Generated Successfully.")

        return {
            "success": True,
            "message": "Interview Questions Generated",
            "data": {
                "filename": request.filename,
                "role": request.role,
                "questions": result
            }
        }

    except Exception as e:

        logger.exception("Interview Question Generation Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Interview Question Generation Failed: {str(e)}"
        )


@router.post(
    "/cover-letter",
    summary="Generate Cover Letter",
    description="Generate a professional cover letter using the uploaded resume.",
    tags=["Cover Letter"],
)
def cover_letter(request: CoverLetterRequest):
    """
    Generate Cover Letter
    """

    logger.info("Cover Letter API Called")

    file_path = f"uploads/{request.filename}"

    if not os.path.exists(file_path):

        logger.warning(f"File not found: {request.filename}")

        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found."
        )

    extracted_text = extract_text_from_pdf(file_path)

    try:

        logger.info("Generating Cover Letter...")

        result = generate_cover_letter(
            extracted_text,
            request.company_name,
            request.job_role
        )

        logger.info("Cover Letter Generated Successfully.")

        return {
            "success": True,
            "message": "Cover Letter Generated",
            "data": {
                "company": request.company_name,
                "role": request.job_role,
                "cover_letter": result
            }
        }

    except Exception as e:

        logger.exception("Cover Letter Generation Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Cover Letter Generation Failed: {str(e)}"
        )


@router.post(
    "/linkedin-profile",
    summary="Generate LinkedIn Profile",
    description="Generate a LinkedIn headline, About section, skills and SEO keywords.",
    tags=["LinkedIn"],
)
def linkedin_profile(request: LinkedInRequest):
    """
    Generate LinkedIn Profile
    """

    logger.info("LinkedIn Profile API Called")

    file_path = f"uploads/{request.filename}"

    if not os.path.exists(file_path):

        logger.warning(f"File not found: {request.filename}")

        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found."
        )

    extracted_text = extract_text_from_pdf(file_path)

    try:

        logger.info("Generating LinkedIn Profile...")

        result = generate_linkedin_profile(extracted_text)

        logger.info("LinkedIn Profile Generated Successfully.")

        return {
            "success": True,
            "message": "LinkedIn Profile Generated",
            "data": {
                "filename": request.filename,
                "linkedin_profile": result
            }
        }

    except Exception as e:

        logger.exception("LinkedIn Profile Generation Failed")

        raise HTTPException(
            status_code=500,
            detail=f"LinkedIn Profile Generation Failed: {str(e)}"
        )


@router.post(
    "/career-chat",
    summary="Career Chat",
    description="Ask career-related questions to the AI Career Mentor.",
    tags=["AI Chat"],
)
def chat(request: ChatRequest):
    """
    AI Career Chat
    """

    logger.info("Career Chat API Called")

    try:

        logger.info("Generating AI Career Advice...")

        result = career_chat(request.question)

        logger.info("Career Chat Completed Successfully.")

        return {
            "success": True,
            "message": "Career Advice Generated",
            "data": {
                "question": request.question,
                "answer": result
            }
        }

    except Exception as e:

        logger.exception("Career Chat Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Career Chat Failed: {str(e)}"
        )