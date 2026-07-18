# 🚀 AI Career Copilot

An AI-powered career assistant that helps students and professionals optimize their resumes, improve ATS scores, prepare for interviews, generate cover letters, enhance LinkedIn profiles, and receive personalized career guidance using Google Gemini AI.

---

## ✨ Features

### 📄 Resume Analysis
- Upload PDF resumes
- AI-powered resume evaluation
- Professional summary generation
- Strengths & weaknesses analysis
- Resume score (out of 100)
- Improvement suggestions

### 🎯 ATS Score Generator
- Compare resume with any Job Description
- ATS compatibility score
- Matching skills detection
- Missing skills & keywords
- Recommendations to improve ATS score

### 🛣 Career Roadmap
- Personalized learning roadmap
- Month-wise learning plan
- Skill gap analysis
- Recommended certifications
- Suggested projects
- Interview preparation guidance

### 💼 Interview Preparation
Generate:
- HR Questions
- Technical Questions
- Coding Questions
- Resume-based Questions
- Project-based Questions
- Scenario-based Questions

### 📝 Cover Letter Generator
Generate professional cover letters customized for:
- Company
- Job Role
- Resume

### 🔗 LinkedIn Profile Optimizer
Generate:
- Professional Headline
- About Section
- Top Skills
- SEO Keywords
- Networking Tips

### 🤖 AI Career Mentor
Interactive AI chat for:
- Career guidance
- Interview advice
- Learning recommendations
- Resume tips
- Placement preparation

### 🔐 Authentication
- Email & Password Login
- Google Sign-In
- Microsoft Sign-In
- Remember Me functionality
- Secure session management

---

# 🛠 Tech Stack

## Backend
- Python
- FastAPI
- Google Gemini API
- PyMuPDF
- Pydantic
- Uvicorn

## Frontend
- Streamlit
- HTML
- CSS
- JavaScript
- Custom Components

## AI
- Google Gemini

## Deployment
- Render
- Streamlit Community Cloud

## Version Control
- Git
- GitHub

---

# 📂 Project Structure

```
AI-Career-Copilot
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── models.py
│   ├── config.py
│   ├── logger.py
│   └── main.py
│
├── frontend/
│
├── uploads/
│
├── requirements.txt
│
├── .env.example
│
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Yaksh2926/AI-Career-Copilot.git
```

```bash
cd AI-Career-Copilot
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-3.5-flash
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Run Frontend

```bash
cd frontend
```

```bash
streamlit run app.py
```

---

# 📡 API Endpoints

| Endpoint | Description |
|-----------|-------------|
| `/upload-resume` | Resume Analysis |
| `/ats-score` | ATS Compatibility |
| `/career-roadmap` | Career Roadmap |
| `/interview-questions` | Interview Questions |
| `/cover-letter` | Cover Letter Generator |
| `/linkedin-profile` | LinkedIn Optimizer |
| `/career-chat` | AI Career Mentor |

---

# 📸 Screenshots

> Add screenshots here after deployment.

- Login Page
- Dashboard
- Resume Analysis
- ATS Score
- Career Roadmap
- Interview Questions
- Cover Letter
- LinkedIn Optimizer
- Career Chat

---

# 🎯 Future Improvements

- Resume History
- PDF Report Export
- Email Notifications
- Multiple Resume Management
- Job Recommendation Engine
- Resume Version Comparison
- Analytics Dashboard

---

# 👨‍💻 Author

**Yaksh Jindal**

Computer Science Undergraduate

Interested in:
- Artificial Intelligence
- Machine Learning
- Full Stack Development
- Generative AI

GitHub:
https://github.com/Yaksh2926

LinkedIn:
(Add your LinkedIn profile here)

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
