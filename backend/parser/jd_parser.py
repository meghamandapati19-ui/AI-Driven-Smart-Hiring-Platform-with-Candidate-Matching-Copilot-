import re


# -----------------------------------
# Extract Required Skills
# -----------------------------------
def extract_jd_skills(text):

    skills_list = [
        "Python", "Java", "C", "C++", "SQL", "MySQL",
        "HTML", "CSS", "JavaScript", "React", "React.js",
        "FastAPI", "Flask", "Django", "Streamlit",
        "Machine Learning", "Deep Learning",
        "Artificial Intelligence",
        "Natural Language Processing",
        "NLP", "Generative AI", "OpenAI",
        "GPT", "LLM", "TensorFlow", "PyTorch",
        "Scikit-learn", "Pandas", "NumPy",
        "Docker", "Git", "GitHub", "Linux",
        "AWS", "Azure", "REST API",
        "Power BI", "Excel", "MongoDB", "SQLite"
    ]

    found_skills = []

    lower_text = text.lower()

    for skill in skills_list:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# -----------------------------------
# Extract Job Title
# -----------------------------------
def extract_job_title(text):

    match = re.search(
        r"job\s*title\s*:?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        if line.lower() == "job title" and i + 1 < len(lines):
            return lines[i + 1]

    return "Not Found"


# -----------------------------------
# Extract Company Name
# -----------------------------------
def extract_company_name(text):

    match = re.search(
        r"company(?:\s*name)?\s*:?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        if line.lower() in ["company", "company name"] and i + 1 < len(lines):
            return lines[i + 1]

    return "Not Found"


# -----------------------------------
# Extract Location
# -----------------------------------
def extract_location(text):

    match = re.search(
        r"location\s*:?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        if line.lower() == "location" and i + 1 < len(lines):
            return lines[i + 1]

    return "Not Found"


# -----------------------------------
# Extract Salary
# -----------------------------------
def extract_salary(text):

    match = re.search(
        r"salary\s*:?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        if line.lower() == "salary" and i + 1 < len(lines):
            return lines[i + 1]

    return "Not Found"


# -----------------------------------
# Extract Employment Type
# -----------------------------------
def extract_employment_type(text):

    match = re.search(
        r"employment\s*type\s*:?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    keywords = [
        "Full-Time",
        "Full Time",
        "Part-Time",
        "Part Time",
        "Internship",
        "Contract",
        "Remote",
        "Hybrid",
        "Permanent",
        "Temporary"
    ]

    for word in keywords:
        if word.lower() in text.lower():
            return word

    return "Not Found"


# -----------------------------------
# Extract Experience
# -----------------------------------
def extract_experience(text):

    patterns = [
        r"\d+\s*-\s*\d+\s*Years?",
        r"\d+\+?\s*Years?",
        r"\d+\s*-\s*\d+\s*Year",
        r"\d+\+?\s*Year"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group()

    return "Not Found"


# -----------------------------------
# Extract Education
# -----------------------------------
def extract_education(text):

    keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "Computer Science",
        "Information Technology",
        "Electronics",
        "Engineering",
        "Degree"
    ]

    for line in text.split("\n"):

        for word in keywords:

            if word.lower() in line.lower():
                return line.strip()

    return "Not Found"


# -----------------------------------
# Extract Responsibilities
# -----------------------------------
def extract_responsibilities(text):

    responsibilities = []
    collecting = False

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        upper = line.upper()

        if "RESPONSIBILITIES" in upper:
            collecting = True
            continue

        if collecting:

            if any(section in upper for section in [
                "PREFERRED",
                "BENEFITS",
                "QUALIFICATIONS",
                "REQUIREMENTS"
            ]):
                break

            line = line.replace("•", "")
            line = line.replace("", "")
            line = line.replace("-", "")
            line = line.strip()

            if line:
                responsibilities.append(line)

    return responsibilities


# -----------------------------------
# Parse Job Description
# -----------------------------------
def parse_jd(text):

    return {

        "job_title": extract_job_title(text),

        "company_name": extract_company_name(text),

        "location": extract_location(text),

        "salary": extract_salary(text),

        "employment_type": extract_employment_type(text),

        "skills": extract_jd_skills(text),

        "experience": extract_experience(text),

        "education": extract_education(text),

        "responsibilities": extract_responsibilities(text),

        "job_description": text
    }