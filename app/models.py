from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    filename: str
    job_description: str

class CareerRoadmapRequest(BaseModel):
    filename: str
    career_goal: str

class InterviewQuestionRequest(BaseModel):
    filename: str
    role: str

class CoverLetterRequest(BaseModel):
    filename: str
    company_name: str
    job_role: str

class LinkedInRequest(BaseModel):
    filename: str

class ChatRequest(BaseModel):
    question: str