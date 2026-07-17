import re

def extract_score(text: str) -> int:
    """
    Extracts a numeric score (out of 100) from the given text block.
    """
    if not text:
        return 75
    
    # 1. Match xx/100
    match = re.search(r'(\d{1,3})\s*/\s*100', text)
    if match:
        val = int(match.group(1))
        if 0 <= val <= 100:
            return val
            
    # 2. Match Score: xx
    match = re.search(r'(?:score|rating|ats|match|result)\b\s*[:\-\s]\s*(\d{1,3})', text, re.IGNORECASE)
    if match:
        val = int(match.group(1))
        if 0 <= val <= 100:
            return val
            
    # 3. Match any 2 digit number
    matches = re.findall(r'\b(\d{2})\b', text)
    for m in matches:
        val = int(m)
        if 50 <= val <= 100: # heuristic for realistic score
            return val
            
    return 75

def parse_list_items(text: str) -> list:
    """
    Extracts list items (indicated by -, *, or numbers) from a text block.
    """
    if not text:
        return []
    
    lines = text.strip().split("\n")
    items = []
    for line in lines:
        cleaned = line.strip()
        # Remove list markers
        cleaned = re.sub(r'^(?:\-\s*|\*\s*|\d+\.\s*|\u2022\s*)', '', cleaned)
        cleaned = cleaned.strip()
        if cleaned:
            # Strip bold formatting
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
            items.append(cleaned)
    return items

def parse_resume_analysis(raw_text: str) -> dict:
    """
    Parses the raw Gemini response for resume analysis into sections.
    """
    sections = {
        "summary": "",
        "skills": [],
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "score": 75,
        "suggestions": []
    }
    
    if not raw_text:
        return sections

    # Normalize newlines
    text = raw_text.replace("\r\n", "\n")
    
    # Identify headings
    # We look for markdown headers like #, ##, ### or bold text headers like **1. Professional Summary**
    pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(?:\d+\.\s*)?(Professional\s+Summary|Technical\s+Skills|Strengths|Weaknesses|Missing\s+Skills|Resume\s+Score|Suggestions(?:\s+for\s+Improvement)?)(?:\s*\*+|\s*#+)?(?:\n|:|\s*\-\s*)'
    
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    if not matches:
        # Fallback if no clean section matching is found: let's try a simple split
        sections["summary"] = raw_text
        sections["score"] = extract_score(raw_text)
        return sections
        
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        section_name = match.group(1).lower()
        section_content = text[start:end].strip()
        
        if "summary" in section_name:
            sections["summary"] = section_content
        elif "technical" in section_name or "skills" in section_name:
            if "missing" not in section_name:
                sections["skills"] = parse_list_items(section_content)
        elif "strength" in section_name:
            sections["strengths"] = parse_list_items(section_content)
        elif "weakness" in section_name:
            sections["weaknesses"] = parse_list_items(section_content)
        elif "missing" in section_name:
            sections["missing_skills"] = parse_list_items(section_content)
        elif "score" in section_name:
            sections["score"] = extract_score(section_content)
        elif "suggestion" in section_name:
            sections["suggestions"] = parse_list_items(section_content)

    # Secondary sweep to extract score if it wasn't parsed correctly in the score section
    if sections["score"] == 75:
        sections["score"] = extract_score(raw_text)
        
    return sections

def parse_ats_score(raw_text: str) -> dict:
    """
    Parses the raw Gemini response for ATS score comparison.
    """
    sections = {
        "score": 70,
        "matching_skills": [],
        "missing_skills": [],
        "missing_keywords": [],
        "suggestions": []
    }
    
    if not raw_text:
        return sections
        
    text = raw_text.replace("\r\n", "\n")
    
    pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(?:\d+\.\s*)?(ATS\s+Score|Matching\s+Skills|Missing\s+Skills|Important\s+Keywords\s+Missing|Keywords|Suggestions(?:\s+to\s+Improve\s+ATS\s+Score)?)(?:\s*\*+|\s*#+)?(?:\n|:|\s*\-\s*)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    if not matches:
        sections["suggestions"] = [raw_text]
        sections["score"] = extract_score(raw_text)
        return sections
        
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        section_name = match.group(1).lower()
        section_content = text[start:end].strip()
        
        if "score" in section_name:
            sections["score"] = extract_score(section_content)
        elif "matching" in section_name:
            sections["matching_skills"] = parse_list_items(section_content)
        elif "missing" in section_name:
            sections["missing_skills"] = parse_list_items(section_content)
        elif "keyword" in section_name:
            sections["missing_keywords"] = parse_list_items(section_content)
        elif "suggestion" in section_name:
            sections["suggestions"] = parse_list_items(section_content)
            
    # Secondary sweep to extract score
    if sections["score"] == 70:
        sections["score"] = extract_score(raw_text)
        
    return sections

def parse_career_roadmap(raw_text: str) -> dict:
    """
    Parses the roadmap output to extract structured details and month-wise timeline.
    """
    sections = {
        "current_level": "Intermediate",
        "known_skills": [],
        "skills_to_learn": [],
        "timeline": [], # list of dicts: {"month": "Month X", "title": "Topic", "details": "Desc"}
        "projects": [],
        "certifications": [],
        "interview_tips": []
    }
    
    if not raw_text:
        return sections
        
    text = raw_text.replace("\r\n", "\n")
    
    pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(?:\d+\.\s*)?(Current\s+Skill\s+Level|Skills\s+Already\s+Known|Skills\s+to\s+Learn|Learning\s+Roadmap|Recommended\s+Projects|Projects|Certifications|Interview\s+Preparation\s+Tips|Tips)(?:\s*\*+|\s*#+)?(?:\n|:|\s*\-\s*)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    # Extract Roadmap months if present
    # Usually: "Month 1: HTML & CSS" or "Month 1 (Foundation):"
    month_pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(Month\s+\d+[:\-\s(]*[^:\n)]*[\)]?)(?:\n|:|\s*\-\s*)([\s\S]*?)(?=(?:\n#+|\n\*+\s*Month\s+\d+|\Z))'
    
    if not matches:
        # Parse timeline anyway
        timeline_matches = re.findall(month_pattern, text)
        for month_title, details in timeline_matches:
            sections["timeline"].append({
                "month": month_title.strip(),
                "details": details.strip()
            })
        return sections
        
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        section_name = match.group(1).lower()
        section_content = text[start:end].strip()
        
        if "current" in section_name:
            sections["current_level"] = section_content
        elif "known" in section_name:
            sections["known_skills"] = parse_list_items(section_content)
        elif "learn" in section_name:
            sections["skills_to_learn"] = parse_list_items(section_content)
        elif "roadmap" in section_name:
            # Parse month-wise timeline from within this section content
            roadmap_content = section_content
            timeline_matches = re.findall(r'(?:^|\n)(?:-|\*|\d+\.)?\s*(?:#+|\*+)?(Month\s+\d+.*?)(?::|\s*-|\n)([\s\S]*?)(?=(?:\n(?:-|\*|\d+\.)?\s*(?:#+|\*+)?Month\s+\d+|$))', roadmap_content, re.IGNORECASE)
            
            for month_title, details in timeline_matches:
                sections["timeline"].append({
                    "month": month_title.replace("**", "").replace("#", "").strip(),
                    "details": details.strip()
                })
            
            # If sub-parsing failed, do a general sweep on the whole text
            if not sections["timeline"]:
                timeline_matches = re.findall(month_pattern, text)
                for month_title, details in timeline_matches:
                    sections["timeline"].append({
                        "month": month_title.strip(),
                        "details": details.strip()
                    })
        elif "project" in section_name:
            sections["projects"] = parse_list_items(section_content)
        elif "certification" in section_name:
            sections["certifications"] = parse_list_items(section_content)
        elif "tip" in section_name or "interview" in section_name:
            sections["interview_tips"] = parse_list_items(section_content)
            
    return sections

def parse_interview_questions(raw_text: str) -> dict:
    """
    Parses the generated interview questions into categorised list items.
    Categories: hr, technical, coding, resume, project, scenario
    """
    sections = {
        "hr": [],
        "technical": [],
        "coding": [],
        "resume": [],
        "project": [],
        "scenario": []
    }
    
    if not raw_text:
        return sections
        
    text = raw_text.replace("\r\n", "\n")
    
    pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(?:\d+\.\s*)?(HR\s+Questions|Technical\s+Questions|Coding\s+Questions|Resume-Based\s+Questions|Project-Based\s+Questions|Scenario-Based\s+Questions)(?:\s*\*+|\s*#+)?(?:\n|:|\s*\-\s*)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    if not matches:
        # Fallback to general lines
        sections["technical"] = parse_list_items(raw_text)
        return sections
        
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        section_name = match.group(1).lower()
        section_content = text[start:end].strip()
        
        items = parse_list_items(section_content)
        
        if "hr" in section_name:
            sections["hr"] = items
        elif "technical" in section_name:
            sections["technical"] = items
        elif "coding" in section_name:
            sections["coding"] = items
        elif "resume" in section_name:
            sections["resume"] = items
        elif "project" in section_name:
            sections["project"] = items
        elif "scenario" in section_name:
            sections["scenario"] = items
            
    return sections

def parse_linkedin_profile(raw_text: str) -> dict:
    """
    Parses LinkedIn optimization details.
    """
    sections = {
        "headline": "",
        "about": "",
        "skills": [],
        "improvements": [],
        "keywords": [],
        "networking": []
    }
    
    if not raw_text:
        return sections
        
    text = raw_text.replace("\r\n", "\n")
    
    pattern = r'(?:^|\n)(?:#+\s*|\*+\s*)?(?:\d+\.\s*)?(Professional\s+LinkedIn\s+Headline|Headline|About\s+Section|Top\s+15\s+Skills|Skills|Improvements\s+to\s+Experience\s+Section|Experience\s+Improvements|SEO\s+Keywords\s+Recruiters\s+Search\s+For|SEO\s+Keywords|Keywords|Networking\s+Tips)(?:\s*\*+|\s*#+)?(?:\n|:|\s*\-\s*)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    if not matches:
        sections["about"] = raw_text
        return sections
        
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        section_name = match.group(1).lower()
        section_content = text[start:end].strip()
        
        if "headline" in section_name:
            sections["headline"] = section_content.replace('"', '').strip()
        elif "about" in section_name:
            sections["about"] = section_content
        elif "skills" in section_name:
            sections["skills"] = parse_list_items(section_content)
        elif "improvement" in section_name or "experience" in section_name:
            sections["improvements"] = parse_list_items(section_content)
        elif "seo" in section_name or "keyword" in section_name:
            sections["keywords"] = parse_list_items(section_content)
        elif "network" in section_name:
            sections["networking"] = parse_list_items(section_content)
            
    return sections
