import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


# -----------------------------------
# Extract Candidate Name
# -----------------------------------
def extract_name(text):

    lines = text.split("\n")

    for i, line in enumerate(lines):

        if "@" in line:

            for j in range(max(0, i - 3), i):

                candidate = lines[j].strip()

                candidate = (
                    candidate.replace("📍", "")
                             .replace("📧", "")
                             .replace("📱", "")
                             .replace("🔗", "")
                             .strip()
                )

                words = candidate.split()

                if (
                    2 <= len(words) <= 4
                    and all(word.replace(".", "").isalpha() for word in words)
                ):
                    return candidate.title()

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Not Found"


# -----------------------------------
# Extract Email
# -----------------------------------
def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


# -----------------------------------
# Extract Phone Number
# -----------------------------------
def extract_phone(text):

    pattern = r"(\+91[- ]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


# -----------------------------------
# Extract Skills
# -----------------------------------
def extract_skills(text):

    skills_list = [

        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "MySQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "React.js",
        "FastAPI",
        "Flask",
        "Django",
        "Streamlit",

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Natural Language Processing",
        "NLP",
        "Generative AI",
        "OpenAI",
        "GPT",
        "LLM",

        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Pandas",
        "NumPy",

        "Git",
        "GitHub",
        "Docker",
        "Linux",

        "Arduino",
        "Embedded C",
        "PCB Design",
        "Altium",
        "MATLAB",
        "DBMS",

        "REST API",
        "AWS",
        "Azure",

        "Problem Solving",
        "Leadership",
        "Communication",
        "Teamwork",
        "Time Management"
    ]

    found = []

    lower = text.lower()

    for skill in skills_list:

        if skill.lower() in lower:

            found.append(skill)

    return sorted(list(set(found)))
# -----------------------------------
# Split Resume into Sections
# -----------------------------------
def split_resume_sections(text):

    sections = {
        "objective": "",
        "education": "",
        "internship": "",
        "projects": "",
        "skills": "",
        "certifications": "",
        "languages": ""
    }

    current = None


    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue


        upper = line.upper()


        # Remove bullet symbols for heading detection
        clean = upper.replace("","").replace("•","").strip()


        if "OBJECTIVE" in clean:
            current = "objective"
            continue


        elif "EDUCATION" in clean:
            current = "education"
            continue


        elif "INTERNSHIP" in clean:
            current = "internship"
            continue


        elif "PROJECTS" in clean:
            current = "projects"
            continue


        elif "TECHNICAL SKILLS" in clean:
            current = "skills"
            continue


        elif "CERTIFICATION" in clean:
            current = "certifications"
            continue


        elif "LANGUAGE" in clean:
            current = "languages"
            continue


        elif (
            "CO-CURRICULAR" in clean
            or "ACHIEVEMENT" in clean
        ):
            current = None
            continue


        if current:
            sections[current] += line + "\n"


    return sections

# -----------------------------------
# Extract Education
# -----------------------------------
def extract_education(text):

    education = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            education.append(line)

    return education


# -----------------------------------
# Extract Experience
# -----------------------------------
import re

def extract_experience(text):

    experience = []

    started = False

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Start only from internship title
        if (
            "Artificial Intelligence Virtual Internship" in line
            or "Infosys Springboard" in line
        ):
            started = True

        if not started:
            continue

        if re.match(r"^\d+\)", line):
            break

        if line not in ["•", ""]:
            experience.append(line)

    return experience


# -----------------------------------
# Extract Projects
# -----------------------------------
def extract_projects(text):

    projects = []

    current = ""

    for line in text.split("\n"):

        line=line.strip()

        if not line:
            continue


        if re.match(r"^\d+\)", line):

            if current:
                projects.append(current.strip())

            current=line


        else:

            if current:
                current += "\n" + line


    if current:
        projects.append(current.strip())


    return projects
# -----------------------------------
# Extract Certifications
# -----------------------------------
def extract_certifications(text):

    certifications = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # remove bullet symbols
        line = line.replace("•", "").replace("", "").strip()

        if line:
            certifications.append(line)

    return certifications
# -----------------------------------
# Extract Languages
# -----------------------------------
def extract_languages(text):

    languages=[]

    for line in text.split("\n"):

        line=line.strip()

        if (
            "English" in line
            or "Telugu" in line
            or "Hindi" in line
        ):
            languages.append(line)


    return languages
# -----------------------------------
# Parse Resume
# -----------------------------------
# -----------------------------------
# Parse Resume
# -----------------------------------
# -----------------------------------
# Parse Resume
# -----------------------------------

def parse_resume(text):

    # Split resume into sections
    sections = split_resume_sections(text)

    # Debug section extraction
    print("\n========== SECTIONS ==========")
    print(sections)


    # Combine text for skill extraction
    all_skill_text = (
        sections["skills"] +
        sections["internship"] +
        sections["projects"] +
        sections["certifications"]
    )


    project_text = (
        sections["projects"] +
        "\n" +
        sections["internship"]
    )


    candidate = {
        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(all_skill_text),

        "education": extract_education(
            sections["education"]
        ),

        "experience": extract_experience(
            sections["internship"]
        ),

        "projects": extract_projects(
            project_text
        ),

        "certifications": extract_certifications(
            sections["certifications"]
        ),

        "languages": extract_languages(
            sections["languages"]
        )
    }
    # Debug final extracted data
    print("\n========== CANDIDATE DATA ==========")
    print(candidate)


    return candidate