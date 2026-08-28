import os
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from streamlit import json
import json as json_module
# =====================================================
# Resume Reader
# =====================================================

from services.resume_reader import (
    extract_pdf_text,
    extract_docx_text
)

from parser.resume_parser import parse_resume
from parser.jd_parser import parse_jd


# =====================================================
# Database
# =====================================================

from database.database import (
    create_tables,
    get_connection,
    add_candidate_id_to_users
)
from database.user_db import (
    create_users_table,
    create_user,
    get_user_by_email,
    authenticate_user,
    get_user_by_id,
    update_user_candidate_id
)

from database.candidate_db import (
    save_candidate,
    get_all_candidates,
    update_candidate_status,
    update_candidate_scores,
    update_candidate_profile
)
from database.application_db import (
    apply_for_job,
    get_candidate_applications,
    create_applications_table
)

from database.job_db import (
    save_job_description,
    get_all_job_descriptions,
    get_job_by_id,
    update_job_description,
    delete_job_description,
    get_all_jobs
)

# =====================================================
# Matching & Ranking
# =====================================================

from matcher.matcher import match_resume_with_jd
from ranking.ranking import rank_candidates


# =====================================================
# AI Features
# =====================================================

from interview.question_generator import generate_questions
from ai_email.email_generator import create_email
from services.groq_service import generate_response


# =====================================================
# Create FastAPI App
# =====================================================

app = FastAPI(
    title="AI Recruitment & Talent Management Copilot"
)


# =====================================================
# Create Existing Tables
# =====================================================

create_tables()
# Create user accounts table
create_users_table()
# Add candidate_id column to existing users table
add_candidate_id_to_users()
# Create applications table
create_applications_table()
# =====================================================
# USER REGISTRATION
# =====================================================

@app.post("/register")
def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):

    # -------------------------------------------------
    # Validate Role
    # -------------------------------------------------

    if role not in ["candidate", "recruiter"]:

        return {
            "success": False,
            "message": "Invalid role."
        }

    # -------------------------------------------------
    # Check Existing Email
    # -------------------------------------------------

    from database.user_db import get_user_by_email

    existing_user = get_user_by_email(email)

    if existing_user:

        return {
            "success": False,
            "message": "Email already registered."
        }

    # -------------------------------------------------
    # Create User
    # -------------------------------------------------

    result = create_user(
        name,
        email,
        password,
        role
    )

    if not result["success"]:

        return {
            "success": False,
            "message": result["error"]
        }

    # -------------------------------------------------
    # Success
    # -------------------------------------------------

    return {

        "success": True,

        "message":
        "Account created successfully.",

        "user_id":
        result["user_id"],

        "role":
        role

    }
# =====================================================
# USER LOGIN
# =====================================================

@app.post("/login")
def login_user(
    email: str = Form(...),
    password: str = Form(...)
):

    result = authenticate_user(
        email,
        password
    )

    if not result["success"]:

        return {
            "success": False,
            "message": result["error"]
        }

    user = result["user"]

    return {

        "success": True,

        "message": "Login successful.",

        "user_id": user["id"],

        "name": user["name"],

        "email": user["email"],

        "role": user["role"],

        "candidate_id": user.get("candidate_id")

    }
# =====================================================
# Create Milestone 4 Tables
# =====================================================

def create_milestone4_tables():

    conn = get_connection()
    cursor = conn.cursor()
    # =====================================================
    # Create Messages Table
    # =====================================================

    def create_messages_table():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER,
            subject TEXT,
            message TEXT NOT NULL,
            sender TEXT DEFAULT 'Recruiter',
            is_read INTEGER DEFAULT 0,
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()


    create_messages_table()

    # -------------------------------------------------
    # Interview Results Table
    # -------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        job_id INTEGER,
        question TEXT,
        answer TEXT,
        score REAL,
        feedback TEXT,
        created_at TEXT
    )
    """)

    # -------------------------------------------------
    # Voice Screening Results Table
    # -------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_screening_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        question TEXT,
        transcript TEXT,
        score REAL,
        feedback TEXT,
        created_at TEXT
    )
    """)

    # -------------------------------------------------
    # Screening Summary Table
    # -------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS screening_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        overall_score REAL,
        recommendation TEXT,
        strengths TEXT,
        improvement TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


create_milestone4_tables()


# =====================================================
# Enable CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Home API
# =====================================================

@app.get("/")
def home():

    return {
        "message":
        "AI Recruitment & Talent Management Copilot Backend Running Successfully"
    }


# =====================================================
# Upload Resume
# =====================================================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    if file.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            file_path
        )

    else:

        return {
            "error":
            "Only PDF and DOCX files are supported."
        }

    candidate = parse_resume(
        resume_text
    )

    candidate["resume_text"] = resume_text

    save_candidate(
        candidate
    )

    return {

        "message":
        "Resume uploaded successfully.",

        "candidate_profile":
        candidate

    }
# =====================================================
# Candidate Upload / Update Resume
# =====================================================

@app.post("/candidate/{candidate_id}/upload-resume")
async def upload_candidate_resume(
    candidate_id: int,
    file: UploadFile = File(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    # -------------------------------------------------
    # Check file type
    # -------------------------------------------------

    if not file.filename.lower().endswith(
        (".pdf", ".docx")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # -------------------------------------------------
    # Save uploaded file
    # -------------------------------------------------

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    # -------------------------------------------------
    # Extract resume text
    # -------------------------------------------------

    if file.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            file_path
        )

    else:

        resume_text = extract_docx_text(
            file_path
        )

    # -------------------------------------------------
    # Parse resume
    # -------------------------------------------------

    candidate_data = parse_resume(
        resume_text
    )

    candidate_data["resume_text"] = resume_text

    # -------------------------------------------------
    # Update existing candidate
    # -------------------------------------------------

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET
            name = ?,
            email = ?,
            phone = ?,
            skills = ?,
            education = ?,
            experience = ?,
            resume_text = ?
        WHERE id = ?
        """,
        (
            candidate_data.get("name", ""),
            candidate_data.get("email", ""),
            candidate_data.get("phone", ""),
            json_module.dumps(candidate_data.get("skills", [])),
            json_module.dumps(candidate_data.get("education", [])),
            json_module.dumps(candidate_data.get("experience", [])),
            resume_text,
            candidate_id
        )
    )

    if cursor.rowcount == 0:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    conn.commit()

    conn.close()

    return {

        "message":
        "Resume uploaded and candidate profile updated successfully.",

        "candidate_id":
        candidate_id,

        "filename":
        file.filename,

        "candidate_profile":
        candidate_data
    }
# =====================================================
# Candidate Resume Analysis
# =====================================================

@app.get("/candidate/{candidate_id}/resume-analysis")
def candidate_resume_analysis(candidate_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------------------------
    # Get candidate resume
    # -------------------------------------------------

    cursor.execute(
        """
        SELECT
            name,
            skills,
            education,
            experience,
            resume_text
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    # -------------------------------------------------
    # Candidate not found
    # -------------------------------------------------

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    # -------------------------------------------------
    # Resume not uploaded
    # -------------------------------------------------

    resume_text = candidate["resume_text"]

    if not resume_text:

        raise HTTPException(
            status_code=400,
            detail="Please upload a resume first."
        )

    # -------------------------------------------------
    # AI Prompt
    # -------------------------------------------------

    prompt = f"""
You are an expert resume evaluator.

Analyze the following candidate resume.

RESUME:
{resume_text}

Return the result in EXACTLY this format:

SUMMARY:
Write a professional 3-4 sentence summary.

ATS_SCORE:
Give a score from 0 to 100.

SKILLS:
List the most important technical and professional skills separated by commas.

SUGGESTIONS:
Give exactly 4 practical suggestions for improving the resume.
Each suggestion should be on a separate line.

Evaluate the resume based on:
- clarity
- skills
- education
- projects
- experience
- technical relevance
- ATS friendliness
- overall professional presentation
"""

    # -------------------------------------------------
    # Generate AI response
    # -------------------------------------------------

    ai_response = generate_response(
        prompt
    )

    # -------------------------------------------------
    # Default values
    # -------------------------------------------------

    summary = ""
    ats_score = 0
    skills = []
    suggestions = []

    # -------------------------------------------------
    # Parse AI response
    # -------------------------------------------------

    lines = ai_response.splitlines()

    current_section = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.upper().startswith("SUMMARY:"):

            current_section = "summary"

            summary = line.split(
                ":",
                1
            )[1].strip()

        elif line.upper().startswith("ATS_SCORE:"):

            current_section = "ats_score"

            score_text = line.split(
                ":",
                1
            )[1].strip()

            try:

                ats_score = float(
                    score_text.replace(
                        "%",
                        ""
                    )
                )

            except:

                ats_score = 0

        elif line.upper().startswith("SKILLS:"):

            current_section = "skills"

            skill_text = line.split(
                ":",
                1
            )[1].strip()

            if skill_text:

                skills = [
                    skill.strip()
                    for skill in skill_text.split(",")
                    if skill.strip()
                ]

        elif line.upper().startswith("SUGGESTIONS:"):

            current_section = "suggestions"

        elif current_section == "summary":

            summary += " " + line

        elif current_section == "skills":

            skills.extend(
                [
                    skill.strip()
                    for skill in line.split(",")
                    if skill.strip()
                ]
            )

        elif current_section == "suggestions":

            suggestion = line.lstrip(
                "-•123456789. "
            ).strip()

            if suggestion:

                suggestions.append(
                    suggestion
                )

    # -------------------------------------------------
    # Limit score
    # -------------------------------------------------

    ats_score = min(
        max(
            ats_score,
            0
        ),
        100
    )

    # -------------------------------------------------
    # Return result
    # -------------------------------------------------

    return {

        "candidate_id":
        candidate_id,

        "candidate_name":
        candidate["name"],

        "summary":
        summary,

        "ats_score":
        ats_score,

        "skills":
        skills,

        "suggestions":
        suggestions
    }

# =====================================================
# Get All Candidates
# =====================================================

@app.get("/candidates")
def get_candidates():

    candidates = get_all_candidates()

    return {

        "total_candidates":
        len(candidates),

        "candidates":
        candidates

    }
# =====================================================
# Update Candidate Profile
# =====================================================

@app.put("/candidate/{candidate_id}/profile")
def update_candidate_profile_api(
    candidate_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    skills: str = Form(...),
    education: str = Form(...),
    experience: str = Form(...)
):

    update_candidate_profile(
        candidate_id,
        name,
        email,
        phone,
        skills.split(","),
        education.split(","),
        experience.split(",")
    )

    return {
        "message": "Candidate profile updated successfully",
        "candidate_id": candidate_id
    }
# =====================================================
# APPLY FOR JOB
# =====================================================

@app.post("/apply-job")
def apply_job_api(
    candidate_id: int = Form(...),
    job_id: int = Form(...)
):

    result = apply_for_job(
        candidate_id,
        job_id
    )

    return result

# ===================================================== 
# Update Application Status 
# ===================================================== 
 
@app.put("/application/{application_id}/status") 
def update_application_status( 
    application_id: int, 
    status: str = Form(...) 
): 
    conn = get_connection() 
    cursor = conn.cursor() 
 
    cursor.execute( 
        """ 
        UPDATE applications 
        SET status = ? 
        WHERE id = ? 
        """, 
        (status, application_id) 
    ) 
 
    if cursor.rowcount == 0: 
        conn.close() 
 
        raise HTTPException( 
            status_code=404, 
            detail="Application not found." 
        ) 
 
    conn.commit() 
    conn.close() 
 
    return { 
        "message": "Application status updated successfully.", 
        "application_id": application_id, 
        "status": status 
    }
# =====================================================
# GET CANDIDATE APPLICATIONS
# =====================================================

@app.get("/candidate/{candidate_id}/applications")
def get_candidate_applications_api(
    candidate_id: int
):

    applications = get_candidate_applications(
        candidate_id
    )

    return {
        "total_applications": len(applications),
        "applications": applications
    }
# =====================================================
# Upload Job Description
# =====================================================

@app.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    if file.filename.lower().endswith(".pdf"):

        jd_text = extract_pdf_text(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        jd_text = extract_docx_text(
            file_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    job = parse_jd(
        jd_text
    )

    save_job_description(
        job
    )

    return {

        "message":
        "Job Description uploaded successfully.",

        "job_description":
        job

    }


# =====================================================
# Get All Jobs
# =====================================================

@app.get("/jobs")
def get_jobs():

    jobs = get_all_job_descriptions()

    return {

        "total_jobs":
        len(jobs),

        "jobs":
        jobs

    }


# =====================================================
# Get One Job
# =====================================================

@app.get("/jobs/{job_id}")
def get_job(job_id: int):

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "message":
            "Job Description not found."

        }

    return job


# =====================================================
# Update Job
# =====================================================

@app.put("/jobs/{job_id}")
def update_job_api(
    job_id: int,
    job: dict
):

    existing_job = get_job_by_id(
        job_id
    )

    if existing_job is None:

        return {

            "message":
            "Job Description not found."

        }

    update_job_description(
        job_id,
        job
    )

    return {

        "message":
        "Job Description updated successfully."

    }


# =====================================================
# Delete Job
# =====================================================

@app.delete("/jobs/{job_id}")
def delete_job_api(
    job_id: int
):

    if delete_job_description(
        job_id
    ):

        return {

            "message":
            "Job deleted successfully."

        }

    return {

        "message":
        "Delete failed."

    }


# =====================================================
# Match Resume with Job Description
# =====================================================

@app.post("/match")
async def match_resume_and_jd(
    resume: UploadFile = File(...),
    job_id: int = Form(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    resume_path = os.path.join(
        upload_folder,
        resume.filename
    )

    with open(
        resume_path,
        "wb"
    ) as buffer:

        buffer.write(
            await resume.read()
        )

    if resume.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            resume_path
        )

    elif resume.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            resume_path
        )

    else:

        return {

            "error":
            "Resume must be PDF or DOCX."

        }

    resume_data = parse_resume(
        resume_text
    )

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "error":
            "Job Description not found."

        }

    jd_data = parse_jd(
        job["job_description"]
    )

    result = match_resume_with_jd(
        resume_data,
        jd_data
    )

    return result


# =====================================================
# Rank Candidates - Upload JD
# =====================================================

@app.post("/rank-candidates")
async def rank_all_candidates(
    file: UploadFile = File(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    if file.filename.lower().endswith(".pdf"):

        jd_text = extract_pdf_text(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        jd_text = extract_docx_text(
            file_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    job = parse_jd(
        jd_text
    )

    ranked_candidates = rank_candidates(
        job
    )

    return {

        "message":
        "Candidates ranked successfully.",

        "total_candidates":
        len(ranked_candidates),

        "ranking":
        ranked_candidates

    }


# =====================================================
# Rank Candidates using Job ID
# =====================================================

@app.post("/rank-candidates/{job_id}")
def rank_candidates_by_job(
    job_id: int
):

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "message":
            "Job not found."

        }

    ranked_candidates = rank_candidates(
        job
    )

    return {

        "message":
        "Candidates ranked successfully.",

        "total_candidates":
        len(ranked_candidates),

        "ranking":
        ranked_candidates

    }


# =====================================================
# Interview Question Generator
# =====================================================

@app.get("/generate-questions/{candidate_id}/{job_id}")
def interview_questions(
    candidate_id: int,
    job_id: int
):

    candidates = get_all_candidates()

    candidate = None

    for c in candidates:

        if c["id"] == candidate_id:

            candidate = c

            break

    if candidate is None:

        return {

            "message":
            "Candidate not found."

        }

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "message":
            "Job not found."

        }

    questions = generate_questions(
        candidate,
        job
    )

    return questions


# =====================================================
# Update Candidate Status
# =====================================================

@app.put("/candidate/{candidate_id}/status")
def change_candidate_status(
    candidate_id: int,
    status: str
):

    update_candidate_status(
        candidate_id,
        status
    )

    return {

        "message":
        "Candidate status updated successfully."

    }


# =====================================================
# AI Email Generator
# =====================================================

@app.get(
    "/generate-email/{candidate_id}/{job_id}/{email_type}"
)
def generate_email_api(
    candidate_id: int,
    job_id: int,
    email_type: str
):

    candidates = get_all_candidates()

    candidate = None

    for c in candidates:

        if c["id"] == candidate_id:

            candidate = c

            break

    if candidate is None:

        return {

            "message":
            "Candidate not found."

        }

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "message":
            "Job not found."

        }

    return create_email(
        candidate,
        job,
        email_type
    )
# =====================================================
# Send Recruiter Message to Candidate
# =====================================================

class MessageRequest(BaseModel):
    candidate_id: int
    job_id: int | None = None
    subject: str
    message: str


@app.post("/send-message")
def send_message(data: MessageRequest):

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether candidate exists
    cursor.execute(
        "SELECT id FROM candidates WHERE id = ?",
        (data.candidate_id,)
    )

    candidate = cursor.fetchone()

    if candidate is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    # Save message
    cursor.execute(
        """
        INSERT INTO messages
        (
            candidate_id,
            job_id,
            subject,
            message,
            sender,
            is_read,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.candidate_id,
            data.job_id,
            data.subject,
            data.message,
            "Recruiter",
            0,
            datetime.now().isoformat()
        )
    )

    message_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Message sent successfully.",
        "message_id": message_id,
        "candidate_id": data.candidate_id
    }

# =====================================================
# GET CANDIDATE MESSAGES
# =====================================================

@app.get("/candidate/{candidate_id}/messages")
def get_candidate_messages(candidate_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    # Get all messages for this candidate
    cursor.execute(
        """
        SELECT
            id,
            candidate_id,
            job_id,
            subject,
            message,
            sender,
            is_read,
            created_at
        FROM messages
        WHERE candidate_id = ?
        ORDER BY created_at DESC
        """,
        (candidate_id,)
    )

    messages = cursor.fetchall()

    conn.close()

    result = []

    for msg in messages:
        result.append({
            "id": msg[0],
            "candidate_id": msg[1],
            "job_id": msg[2],
            "subject": msg[3],
            "message": msg[4],
            "sender": msg[5],
            "is_read": msg[6],
            "created_at": msg[7]
        })

    return {
        "success": True,
        "messages": result
    }
# =====================================================
# AI Resume Summary
# =====================================================

@app.post("/resume-summary")
async def resume_summary(
    file: UploadFile = File(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    if file.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            file_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    prompt = f"""
Summarize the following resume professionally for a recruiter.

Resume:
{resume_text}
"""

    summary = generate_response(
        prompt
    )

    return {

        "summary":
        summary

    }


# =====================================================
# AI Resume vs Job Description Analysis
# =====================================================

@app.post("/resume-jd-analysis")
async def resume_jd_analysis(
    resume: UploadFile = File(...),
    job_id: int = Form(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    resume_path = os.path.join(
        upload_folder,
        resume.filename
    )

    with open(
        resume_path,
        "wb"
    ) as buffer:

        buffer.write(
            await resume.read()
        )

    if resume.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            resume_path
        )

    elif resume.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            resume_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "error":
            "Job Description not found."

        }

    jd_text = job["job_description"]

    prompt = f"""
You are an expert technical recruiter.

Analyze the candidate's resume against the job description.

Provide:

1. Overall Match Percentage
2. Strengths
3. Missing Skills
4. Weaknesses
5. Final Recommendation

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    analysis = generate_response(
        prompt
    )

    return {

        "analysis":
        analysis

    }


# =====================================================
# AI Interview Questions
# =====================================================

@app.post("/ai-interview-questions")
async def ai_interview_questions(
    resume: UploadFile = File(...),
    job_id: int = Form(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    resume_path = os.path.join(
        upload_folder,
        resume.filename
    )

    with open(
        resume_path,
        "wb"
    ) as buffer:

        buffer.write(
            await resume.read()
        )

    if resume.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            resume_path
        )

    elif resume.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            resume_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "error":
            "Job Description not found."

        }

    jd_text = job["job_description"]

    prompt = f"""
You are a Senior Technical Interviewer.

Using the resume and job description, generate:

1. Five Technical Questions

2. Three Project-based Questions

3. Three HR / Behavioural Questions

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    questions = generate_response(
        prompt
    )

    return {

        "interview_questions":
        questions

    }


# =====================================================
# AI Hiring Recommendation
# =====================================================

@app.post("/hiring-recommendation")
async def hiring_recommendation(
    resume: UploadFile = File(...),
    job_id: int = Form(...)
):

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    resume_path = os.path.join(
        upload_folder,
        resume.filename
    )

    with open(
        resume_path,
        "wb"
    ) as buffer:

        buffer.write(
            await resume.read()
        )

    if resume.filename.lower().endswith(".pdf"):

        resume_text = extract_pdf_text(
            resume_path
        )

    elif resume.filename.lower().endswith(".docx"):

        resume_text = extract_docx_text(
            resume_path
        )

    else:

        return {

            "error":
            "Only PDF and DOCX files are supported."

        }

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return {

            "error":
            "Job Description not found."

        }

    jd_text = job["job_description"]

    prompt = f"""
You are an experienced HR Manager.

Analyze the resume against the job description.

Return:

Hiring Decision

Confidence Score

Strengths

Weaknesses

Reason

Next Step

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    recommendation = generate_response(
        prompt
    )

    return {

        "hiring_recommendation":
        recommendation

    }


# =====================================================
# Interview Evaluation Request Model
# =====================================================

class InterviewRequest(BaseModel):

    candidate_id: int
    job_id: int
    answers: str


# =====================================================
# Evaluate Interview
# =====================================================

@app.post("/evaluate-interview")
def evaluate_interview(
    data: InterviewRequest
):

    candidates = get_all_candidates()

    candidate = None

    for c in candidates:

        if c["id"] == data.candidate_id:

            candidate = c

            break

    if candidate is None:

        return {

            "message":
            "Candidate not found"

        }

    job = get_job_by_id(
        data.job_id
    )

    if job is None:

        return {

            "message":
            "Job not found"

        }

    prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:
{candidate["resume_text"]}

Job Description:
{job["job_description"]}

Candidate Answers:
{data.answers}

Evaluate the answers and provide:

1. Technical Score (/10)
2. Communication Score (/10)
3. Problem Solving Score (/10)
4. Overall Interview Score (/100)
5. Hiring Decision
6. Explanation
7. Strengths
8. Improvement Areas
"""

    evaluation = generate_response(
        prompt
    )

    # -------------------------------------------------
    # Save overall interview evaluation
    # -------------------------------------------------

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_results
        (
            candidate_id,
            job_id,
            question,
            answer,
            score,
            feedback,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.candidate_id,
            data.job_id,
            "Interview Evaluation",
            data.answers,
            None,
            evaluation,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {

        "evaluation":
        evaluation,

        "database_saved":
        True

    }


# =====================================================
# Save Individual Interview Question & Answer
# =====================================================
class ScreeningSummaryRequest(BaseModel):
    candidate_id: int
    overall_score: float
    recommendation: str
    strengths: str
    improvement: str

class InterviewResultRequest(BaseModel):

    candidate_id: int
    job_id: int | None = None
    question: str
    answer: str
    score: float | None = None
    feedback: str | None = None


@app.post("/save-interview-result")
def save_interview_result(
    data: InterviewResultRequest
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_results
        (
            candidate_id,
            job_id,
            question,
            answer,
            score,
            feedback,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.candidate_id,
            data.job_id,
            data.question,
            data.answer,
            data.score,
            data.feedback,
            datetime.now().isoformat()
        )
    )

    result_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {

        "message":
        "Interview question and answer saved successfully.",

        "result_id":
        result_id

    }


# =====================================================
# Save Voice Screening Result
# =====================================================

class VoiceScreeningRequest(BaseModel):

    candidate_id: int
    question: str
    transcript: str
    score: float | None = None
    feedback: str | None = None


@app.post("/save-voice-screening-result")
def save_voice_screening_result(
    data: VoiceScreeningRequest
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO voice_screening_results
        (
            candidate_id,
            question,
            transcript,
            score,
            feedback,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.candidate_id,
            data.question,
            data.transcript,
            data.score,
            data.feedback,
            datetime.now().isoformat()
        )
    )

    result_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {

        "message":
        "Voice screening result saved successfully.",

        "result_id":
        result_id

    }


# =====================================================
# Save Final Screening Summary
# =====================================================

class ScreeningSummaryRequest(BaseModel):

    candidate_id: int
    overall_score: float
    recommendation: str
    strengths: str | None = None
    improvement: str | None = None

@app.post("/save-screening-summary")
def save_screening_summary(data: ScreeningSummaryRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO screening_summaries
            (
                candidate_id,
                overall_score,
                recommendation,
                strengths,
                improvement,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.candidate_id,
                data.overall_score,
                data.recommendation,
                data.strengths,
                data.improvement,
                datetime.now().isoformat()
            )
        )

        conn.commit()

        return {
            "message": "Screening summary saved successfully",
            "candidate_id": data.candidate_id
        }

    except Exception as e:
        conn.rollback()

        return {
            "message": "Failed to save screening summary",
            "error": str(e)
        }

    finally:
        conn.close()
@app.get("/screening-summary/{candidate_id}")
def get_screening_summary(candidate_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM screening_summaries
        WHERE candidate_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (candidate_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "message": "No screening summary found.",
            "summary": None
        }

    return {
        "summary": dict(row)
    }


# =====================================================
# Get Interview Results
# =====================================================

@app.get("/interview-results/{candidate_id}")
def get_interview_results(
    candidate_id: int
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interview_results
        WHERE candidate_id = ?
        ORDER BY id DESC
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {

        "candidate_id":
        candidate_id,

        "total_results":
        len(rows),

        "results":
        [dict(row) for row in rows]

    }
# =====================================================
# Get Interview Results
# =====================================================

@app.get("/interview-results/{candidate_id}")
def get_interview_results(
    candidate_id: int
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interview_results
        WHERE candidate_id = ?
        ORDER BY id DESC
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        "candidate_id": candidate_id,
        "total_results": len(rows),
        "results": [dict(row) for row in rows]
    }


# =====================================================
# Save Individual Voice Interview Result
# =====================================================

@app.post("/save-interview-result")
def save_interview_result(data: InterviewResultRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO interview_results
            (
                candidate_id,
                job_id,
                question,
                answer,
                score,
                feedback,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.candidate_id,
                data.job_id,
                data.question,
                data.answer,
                data.score,
                data.feedback,
                datetime.now().isoformat()
            )
        )

        conn.commit()

        return {
            "message": "Interview result saved successfully",
            "result_id": cursor.lastrowid
        }

    except Exception as e:

        conn.rollback()

        return {
            "message": "Failed to save interview result",
            "error": str(e)
        }

    finally:
        conn.close()
# =====================================================
# Get Screening Summary
# =====================================================

@app.get("/screening-summary/{candidate_id}")
def get_screening_summary(candidate_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM screening_summaries
        WHERE candidate_id = ?
        ORDER BY id DESC
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        "candidate_id": candidate_id,
        "total_results": len(rows),
        "results": [dict(row) for row in rows]
    }

# =====================================================
# Get Voice Screening Results
# =====================================================

@app.get("/voice-screening-results/{candidate_id}")
def get_voice_screening_results(
    candidate_id: int
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM voice_screening_results
        WHERE candidate_id = ?
        ORDER BY id DESC
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {

        "candidate_id":
        candidate_id,

        "total_results":
        len(rows),

        "results":
        [dict(row) for row in rows]

    }


# =====================================================
# Get Screening Summary
# =====================================================

@app.get("/screening-summary/{candidate_id}")
def get_screening_summary(
    candidate_id: int
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM screening_summaries
        WHERE candidate_id = ?
        ORDER BY id DESC
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {

        "candidate_id":
        candidate_id,

        "total_summaries":
        len(rows),

        "summaries":
        [dict(row) for row in rows]

    }


# =====================================================
# Recruiter Analytics
# =====================================================

@app.get("/analytics")
def recruiter_analytics():

    candidates = get_all_candidates()

    jobs = get_all_job_descriptions()

    total_candidates = len(
        candidates
    )

    total_jobs = len(
        jobs
    )

    match_scores = []

    shortlisted = 0

    rejected = 0

    for c in candidates:

        score = (
            c.get("match_score")
            or c.get("match_percentage")
            or c.get("compatibility_score")
        )

        if score:

            match_scores.append(
                float(score)
            )

        status = str(
            c.get("status", "")
        ).lower()

        if status in [
            "selected",
            "shortlisted",
            "hired"
        ]:

            shortlisted += 1

        elif status in [
            "rejected",
            "not selected"
        ]:

            rejected += 1

    if len(match_scores) > 0:

        avg_match = round(
            sum(match_scores) /
            len(match_scores),
            2
        )

    else:

        avg_match = 0

    return {

        "total_candidates":
        total_candidates,

        "total_jobs":
        total_jobs,

        "average_match_score":
        avg_match,

        "shortlisted_candidates":
        shortlisted,

        "rejected_candidates":
        rejected

    }
# ====================================================
# GET CANDIDATE PROFILE
# ====================================================

@app.get("/candidate/{candidate_id}")
def get_candidate_profile(candidate_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            phone,
            skills,
            education,
            experience
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "id": row[0],
        "name": row[1] or "",
        "email": row[2] or "",
        "phone": row[3] or "",
        "skills": row[4] or "",
        "education": row[5] or "",
        "experience": row[6] or ""
    }