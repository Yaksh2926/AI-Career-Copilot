from google import genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_resume(resume_text: str):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze this resume and provide:

1. Professional Summary
2. Technical Skills
3. Strengths
4. Weaknesses
5. Missing Skills
6. Resume Score (out of 100)
7. Suggestions for Improvement

Resume:

{resume_text}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text


def ats_score(resume_text: str, job_description: str):

    prompt = f"""
You are an ATS (Applicant Tracking System).

Compare the Resume with the Job Description.

Return the following:

1. ATS Score (out of 100)
2. Matching Skills
3. Missing Skills
4. Important Keywords Missing
5. Suggestions to Improve ATS Score

Resume:

{resume_text}

Job Description:

{job_description}

Return the answer in clean markdown.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text

def career_roadmap(resume_text: str, career_goal: str):

    prompt = f"""
You are an experienced career mentor.

Based on the resume below and the user's career goal,
create a detailed learning roadmap.

Career Goal:
{career_goal}

Resume:
{resume_text}

Include:

1. Current Skill Level
2. Skills Already Known
3. Skills to Learn
4. Learning Roadmap (Month-wise)
5. Recommended Projects
6. Certifications
7. Interview Preparation Tips
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text

def interview_questions(resume_text: str, role: str):

    prompt = f"""
You are an experienced technical interviewer.

Based on the following resume and target role, generate interview questions.

Role:
{role}

Resume:
{resume_text}

Generate:

1. HR Questions (5)

2. Technical Questions (10)

3. Coding Questions (5)

4. Resume-Based Questions

5. Project-Based Questions

6. Scenario-Based Questions

Provide the questions in a clean markdown format.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text

def generate_cover_letter(
    resume_text: str,
    company_name: str,
    job_role: str
):

    prompt = f"""
You are an expert career coach.

Write a professional cover letter.

Company:
{company_name}

Job Role:
{job_role}

Resume:

{resume_text}

Instructions:

1. Address the hiring manager professionally.
2. Highlight relevant skills and experience.
3. Explain why the candidate fits the role.
4. Keep the tone professional.
5. Keep it around 350–450 words.
6. End with a strong closing.

Return only the cover letter.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text

def generate_linkedin_profile(resume_text: str):

    prompt = f"""
You are a LinkedIn Profile Optimization Expert.

Based on the resume below, generate:

1. Professional LinkedIn Headline

2. About Section (Around 250 words)

3. Top 15 Skills

4. Improvements to Experience Section

5. SEO Keywords Recruiters Search For

6. Networking Tips

Resume:

{resume_text}

Return everything in professional markdown.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text

def career_chat(question: str):

    prompt = f"""
You are an AI Career Mentor.

Answer the following career question in a clear, practical, and encouraging way.

Question:
{question}

Guidelines:
- Give actionable advice.
- Use simple language.
- Include examples when useful.
- Keep the response well-structured using markdown.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text