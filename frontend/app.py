import streamlit as st
import requests
import pandas as pd
import io
import os
from urllib.parse import quote

from docx import Document
from dotenv import load_dotenv
from groq import Groq

if "page" not in st.session_state:
    st.session_state.page = "landing"

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

# ============================================================
# GROQ CLIENT
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    groq_client = Groq(
        api_key=GROQ_API_KEY
    )
else:
    groq_client = None

# ----------------------------------------------------
# FastAPI Backend URL
# ----------------------------------------------------

API_URL = "http://127.0.0.1:8000"



# ----------------------------------------------------
# CSS andPage Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Recruitment & Talent Management Copilot",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
"""
<style>

.main {
    background-color:#f7f9fc;
}



h1 {
    color:#0b3d91;
}



.stButton button {

    background-color:#0b3d91;

    color:white;

    border-radius:10px;

    height:40px;

}



.stMetric {

    background:white;

    padding:15px;

    border-radius:15px;

    color:black;

}



.stMetric label {

    color:black !important;

    font-size:16px;

}



.stMetric div {

    color:black !important;

    font-size:28px;

    font-weight:bold;

}

</style>

""",
unsafe_allow_html=True
)
# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "role" not in st.session_state:
    st.session_state.role = None

if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ============================================================
# CANDIDATE AI VOICE INTERVIEW SESSION STATE
# ============================================================
_candidate_voice_defaults = {
    "candidate_voice_questions": [],
    "candidate_voice_question_index": 0,
    "candidate_voice_answers": [],
    "candidate_voice_scores": [],
    "candidate_voice_evaluations": [],
    "candidate_voice_started": False,
    "candidate_voice_finished": False,
    "candidate_voice_candidate_id": None,
    "candidate_voice_job_id": None,
    "candidate_voice_job_title": "",
    "candidate_voice_transcript": "",
    "candidate_voice_overall_analysis": "",
    "candidate_voice_overall_feedback": "",
    "candidate_voice_overall_strengths": [],
    "candidate_voice_overall_improvement": "",
    "candidate_voice_overall_suggestions": "",
    "candidate_voice_summary_saved": False,
}

for _state_key, _state_value in _candidate_voice_defaults.items():
    if _state_key not in st.session_state:
        st.session_state[_state_key] = (
            _state_value.copy()
            if isinstance(_state_value, list)
            else _state_value
        )
# ============================================================
# LANDING PAGE FUNCTION
# ============================================================

def landing_page():

    st.markdown("""
<style>
.landing-container {
    text-align: center;
    padding: 60px 20px 30px 20px;
}

.landing-title {
    font-size: 45px;
    font-weight: 800;
    color: #2563EB;
    margin-bottom: 15px;
}

.landing-subtitle {
    font-size: 22px;
    color: #374151;
    margin-bottom: 20px;
}

.landing-description {
    font-size: 17px;
    color: #6B7280;
    max-width: 750px;
    margin: auto;
    line-height: 1.7;
}

.feature-box {
    padding: 25px 15px;
    border-radius: 12px;
    background-color: #F8FAFC;
    border: 1px solid #E5E7EB;
    text-align: center;
    min-height: 120px;
}

.feature-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 10px;
}

.feature-text {
    color: #6B7280;
    font-size: 15px;
    line-height: 1.5;
}

.get-started-container {
    text-align: center;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)

    # ========================================================
    # HERO SECTION
    # ========================================================

    st.markdown("""
<div class="landing-container">

<div class="landing-title">
🤖 AI Recruitment & Talent Management Copilot
</div>

<div class="landing-subtitle">
Intelligent Hiring. Faster Recruitment. Better Decisions.
</div>

<div class="landing-description">
An AI-powered recruitment assistant that helps recruiters
analyze resumes, match candidates with job descriptions,
rank candidates, generate interview questions and perform
AI-based candidate screening.
</div>

</div>
""", unsafe_allow_html=True)

    st.write("")

    # ========================================================
    # FEATURES
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
<div class="feature-box">
<div class="feature-title">
📄 Resume Analysis
</div>

<div class="feature-text">
Upload and analyze candidate resumes using AI.
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="feature-box">
<div class="feature-title">
🎯 Candidate Matching
</div>

<div class="feature-text">
Match candidates with job descriptions and calculate
compatibility scores.
</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
<div class="feature-box">
<div class="feature-title">
🎤 AI Screening
</div>

<div class="feature-text">
Conduct AI-powered interview and voice screening.
</div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ========================================================
    # GET STARTED BUTTON
    # ========================================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🚀 Get Started",
            use_container_width=True
        ):
            st.session_state.page = "signup"
            st.rerun()
# ============================================================
# SIGN UP PAGE FUNCTION
# ============================================================

def signup_page():

    st.markdown(
        """
        <style>
        .signup-title {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            color: #2563EB;
            margin-top: 40px;
        }

        .signup-subtitle {
            text-align: center;
            color: #6B7280;
            font-size: 16px;
            margin-bottom: 30px;
        }
        </style>

        <div class="signup-title">
            📝 Create Your Account
        </div>

        <div class="signup-subtitle">
            Join AI Recruitment & Talent Management Copilot
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # ----------------------------------------------------
        # INPUT FIELDS
        # ----------------------------------------------------

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="signup_name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm_password"
        )

        # ----------------------------------------------------
        # ROLE SELECTION
        # ----------------------------------------------------

        role = st.selectbox(
            "Select Your Role",
            ["Candidate", "Recruiter"],
            key="signup_role"
        )

        st.write("")

        # ----------------------------------------------------
        # CREATE ACCOUNT
        # ----------------------------------------------------

        if st.button(
            "Create Account",
            use_container_width=True,
            key="create_account_button"
        ):

            # ------------------------------------------------
            # CLEAN INPUT
            # ------------------------------------------------

            name = name.strip()
            email = email.strip().lower()

            # ------------------------------------------------
            # CHECK EMPTY FIELDS
            # ------------------------------------------------

            if (
                not name
                or not email
                or not password
                or not confirm_password
            ):

                st.error(
                    "⚠️ Please fill in all fields."
                )

            # ------------------------------------------------
            # CHECK EMAIL
            # ------------------------------------------------

            elif "@" not in email or "." not in email:

                st.error(
                    "⚠️ Please enter a valid email address."
                )

            # ------------------------------------------------
            # CHECK PASSWORD LENGTH
            # ------------------------------------------------

            elif len(password) < 6:

                st.error(
                    "⚠️ Password must contain at least 6 characters."
                )

            # ------------------------------------------------
            # CHECK PASSWORD CONFIRMATION
            # ------------------------------------------------

            elif password != confirm_password:

                st.error(
                    "⚠️ Passwords do not match."
                )

            # ------------------------------------------------
            # REGISTER USER
            # ------------------------------------------------

            else:

                try:

                    # Convert UI role to backend role
                    selected_role = role.lower()

                    # ----------------------------------------
                    # Send registration request to FastAPI
                    # ----------------------------------------

                    response = requests.post(
                        "http://127.0.0.1:8000/register",
                        data={
                            "name": name,
                            "email": email,
                            "password": password,
                            "role": selected_role
                        }
                    )

                    # ----------------------------------------
                    # Backend response
                    # ----------------------------------------

                    if response.status_code == 200:

                        data = response.json()

                        # ------------------------------------
                        # Registration successful
                        # ------------------------------------

                        if data.get("success"):

                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.info(
                                "Please login using your email and password."
                            )

                            # Store basic user information
                            st.session_state.user_name = name
                            st.session_state.user_email = email
                            st.session_state.role = selected_role

                            # --------------------------------
                            # Go to Login page
                            # --------------------------------

                            st.session_state.page = "login"

                            st.rerun()

                        # ------------------------------------
                        # Registration failed
                        # ------------------------------------

                        else:

                            st.error(
                                f"❌ {data.get('message', 'Registration failed.')}"
                            )

                    else:

                        st.error(
                            "❌ Unable to create account. "
                            f"Backend returned status "
                            f"{response.status_code}."
                        )

                # --------------------------------------------
                # Backend connection error
                # --------------------------------------------

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Backend is not running. "
                        "Please start FastAPI first."
                    )

                # --------------------------------------------
                # Other errors
                # --------------------------------------------

                except Exception as e:

                    st.error(
                        f"❌ Error: {str(e)}"
                    )

        st.write("")

        # ----------------------------------------------------
        # ALREADY HAVE AN ACCOUNT
        # ----------------------------------------------------

        st.write("Already have an account?")

        if st.button(
            "🔐 Login",
            use_container_width=True,
            key="go_to_login_button"
        ):

            st.session_state.page = "login"
            st.rerun()

        st.write("")

        # ----------------------------------------------------
        # BACK TO HOME
        # ----------------------------------------------------

        if st.button(
            "⬅️ Back to Home",
            use_container_width=True,
            key="back_to_home_button"
        ):

            st.session_state.page = "landing"
            st.rerun()



# ============================================================
# LOGIN PAGE FUNCTION
# ============================================================

def login_page():

    st.title("🔐 Login")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        key="login_button"
    ):

        email = email.strip()

        if not email or not password:

            st.error(
                "⚠️ Please enter email and password."
            )

        else:

            try:

                # =================================================
                # CHECK USER FROM USERS TABLE
                # =================================================

                response = requests.post(
                    "http://127.0.0.1:8000/login",
                    data={
                        "email": email,
                        "password": password
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    if data.get("success"):

                        # -----------------------------------------
                        # Store logged-in user information
                        # -----------------------------------------

                        st.session_state.user_id = data.get("user_id")
                        st.session_state.user_name = data.get("name")
                        st.session_state.user_email = data.get("email")
                        st.session_state.role = data.get("role")
                        st.session_state.candidate_id = data.get("candidate_id")

                        # -----------------------------------------
                        # Go to Admin / System Overview
                        # -----------------------------------------
                        # Every authenticated user first sees the
                        # system overview. From there the user chooses
                        # Recruiter Dashboard or Candidate Dashboard.
                        st.success(
                            "✅ Login successful!"
                        )

                        st.session_state.page = "admin"
                        st.rerun()

                    else:

                        st.error(
                            "❌ " +
                            data.get(
                                "message",
                                "Invalid email or password."
                            )
                        )

                else:

                    st.error(
                        "❌ Login failed. Please check the backend."
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend is not running. "
                    "Please start FastAPI first."
                )

    # ============================================================
    # CREATE ACCOUNT
    # ============================================================

    if st.button(
        "Create an account",
        key="login_create_account"
    ):

        st.session_state.page = "signup"

        st.rerun()

# ============================================================
# CHOOSE ROLE PAGE
# ============================================================

def choose_role_page():

    st.markdown(
        """
        <div style="text-align:center; padding:40px 20px 20px 20px;">
            <h1 style="color:#2563EB;">Choose Your Role</h1>

            <p style="font-size:18px; color:#666;">
                Select how you want to use the AI Recruitment System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # ROLE SELECTION COLUMNS
    # ========================================================

    if st.session_state.get("role") == "admin":
        col1, col2, col3 = st.columns(3)
    else:
        col1, col2 = st.columns(2)

    # ========================================================
    # RECRUITER
    # ========================================================

    with col1:

        st.markdown("### 👨‍💼 Recruiter")

        st.write(
            "Manage candidates, job descriptions, "
            "candidate ranking and AI interview evaluation."
        )

        if st.button(
            "Continue as Recruiter",
            use_container_width=True,
            key="continue_recruiter"
        ):

            st.session_state.role = "recruiter"

            st.session_state.page = "dashboard"

            st.rerun()

    # ========================================================
    # CANDIDATE
    # ========================================================

    with col2:

        st.markdown("### 👨‍🎓 Candidate")

        st.write(
            "View your profile, applied jobs, "
            "application status and interview performance."
        )

        if st.button(
            "Continue as Candidate",
            use_container_width=True,
            key="continue_candidate"
        ):

            st.session_state.role = "candidate"

            st.session_state.page = "candidate_dashboard"

            st.rerun()



    # ========================================================
    # ADMIN
    # ========================================================

    if st.session_state.get("role") == "admin":

        with col3:

            st.markdown("### 🛡️ Admin")

            st.write(
                "Monitor candidates, job openings and system activity."
            )

            if st.button(
                "Continue as Admin",
                use_container_width=True,
                key="continue_admin"
            ):
                st.session_state.role = "admin"
                st.session_state.page = "admin"
                st.rerun()



# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_page():

    st.title("🛡️ Admin Dashboard")
    st.write(
        "Monitor the recruitment system, candidates, jobs and interview activity."
    )
    st.divider()

    if not st.session_state.get("user_id"):
        st.error("❌ Please login first.")
        return

    st.caption(
        f"Logged in as: {st.session_state.get('user_name', 'User')} "
        f"({st.session_state.get('user_email', 'N/A')})"
    )

    # ========================================================
    # SYSTEM OVERVIEW
    # ========================================================
    st.subheader("📚 Project Overview")

    st.markdown("""
    **AI Recruitment & Talent Management Copilot** is an AI-powered
    recruitment platform that supports the hiring workflow:
    resume analysis, job description management, candidate matching,
    ranking, AI interview generation, voice screening and interview
    performance evaluation.
    """)

    overview_col1, overview_col2, overview_col3 = st.columns(3)

    with overview_col1:
        st.markdown("### 📄 Resume & Candidate Management")
        st.write(
            "Upload PDF/DOCX resumes, parse candidate information, "
            "store candidate profiles and manage candidate status."
        )

    with overview_col2:
        st.markdown("### 🎯 Job & Matching")
        st.write(
            "Upload job descriptions, view job openings, compare resumes "
            "with jobs and calculate matching, ATS and hiring scores."
        )

    with overview_col3:
        st.markdown("### 🤖 AI Recruitment")
        st.write(
            "Generate resume summaries, JD analysis, interview questions, "
            "hiring recommendations and voice interview evaluations."
        )

    st.divider()
    st.subheader("🧩 Project Modules")

    module_data = [
        ("1", "Resume Upload", "Upload and parse PDF/DOCX candidate resumes."),
        ("2", "Job Description Upload", "Create and manage job openings from uploaded JDs."),
        ("3", "Candidate Profiles", "View candidate details, skills, education and experience."),
        ("4", "Resume–JD Matching", "Compare a resume against a selected job."),
        ("5", "Candidate Ranking", "Rank candidates using match, ATS, compatibility and hiring scores."),
        ("6", "Recruiter Dashboard", "Recruitment KPIs, candidate pipeline and analytics."),
        ("7", "AI Features", "Resume summary, JD analysis, interview questions and hiring recommendation."),
        ("8", "Voice Screening", "Five-question AI voice interview with speech-to-text and evaluation."),
        ("9", "Interview Performance", "Overall score, strengths, improvement and question-wise evaluation."),
        ("10", "Candidate Portal", "Profile, jobs, applications, interview and performance views."),
    ]

    st.dataframe(
        pd.DataFrame(
            module_data,
            columns=["#", "Module", "Basic Idea"]
        ),
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("🚀 Choose Dashboard")

    st.write(
        "Choose the dashboard you want to use. The Recruiter Dashboard "
        "contains the recruitment management features. The Candidate "
        "Dashboard contains the candidate workflow and AI voice interview."
    )

    dash_col1, dash_col2 = st.columns(2)

    with dash_col1:
        st.markdown("### 👨‍💼 Recruiter Dashboard")
        st.write(
            "Manage resumes, job descriptions, candidates, matching, "
            "ranking, analytics and AI/voice screening."
        )

        if st.button(
            "➡️ Open Recruiter Dashboard",
            use_container_width=True,
            key="admin_open_recruiter"
        ):
            st.session_state.role = "recruiter"
            st.session_state.page = "dashboard"
            st.rerun()

    with dash_col2:
        st.markdown("### 👨‍🎓 Candidate Dashboard")
        st.write(
            "Manage your profile, browse/apply for jobs, track applications "
            "and complete the five-question AI voice interview."
        )

        if st.button(
            "➡️ Open Candidate Dashboard",
            use_container_width=True,
            key="admin_open_candidate"
        ):
            st.session_state.role = "candidate"
            st.session_state.page = "candidate_dashboard"
            st.rerun()

    st.divider()
    st.subheader("📊 Current System Data")

    candidates = []
    jobs = []

    # ========================================================
    # LOAD CANDIDATES
    # ========================================================
    try:
        response = requests.get(
            f"{API_URL}/candidates",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            candidates = (
                data.get("candidates", [])
                if isinstance(data, dict)
                else data
            )

            if not isinstance(candidates, list):
                candidates = []

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Backend is not running. Please start FastAPI first."
        )
    except Exception as e:
        st.warning(f"Unable to load candidates: {e}")

    # ========================================================
    # LOAD JOBS
    # ========================================================
    try:
        response = requests.get(
            f"{API_URL}/jobs",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, dict):
                jobs = data.get("jobs", [])
            else:
                jobs = data

            if not isinstance(jobs, list):
                jobs = []

    except Exception as e:
        st.warning(f"Unable to load jobs: {e}")

    valid_candidates = [
        c for c in candidates
        if isinstance(c, dict)
    ]

    valid_jobs = [
        j for j in jobs
        if isinstance(j, dict)
    ]

    # ========================================================
    # ADMIN METRICS
    # ========================================================
    total_candidates = len(valid_candidates)
    total_jobs = len(valid_jobs)

    shortlisted = sum(
        1
        for candidate in valid_candidates
        if str(candidate.get("status", "")).lower()
        == "shortlisted"
    )

    selected = sum(
        1
        for candidate in valid_candidates
        if str(candidate.get("status", "")).lower()
        in ["selected", "hired"]
    )

    rejected = sum(
        1
        for candidate in valid_candidates
        if str(candidate.get("status", "")).lower()
        == "rejected"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Candidates", total_candidates)

    with col2:
        st.metric("💼 Job Openings", total_jobs)

    with col3:
        st.metric("⭐ Shortlisted", shortlisted)

    with col4:
        st.metric("✅ Selected", selected)

    with col5:
        st.metric("❌ Rejected", rejected)

    # ========================================================
    # CANDIDATES
    # ========================================================
    st.divider()
    st.subheader("👥 Candidate Management")

    if valid_candidates:
        candidate_columns = [
            "id",
            "name",
            "email",
            "phone",
            "status",
            "match_score",
            "ats_score",
            "hiring_score"
        ]

        available_columns = [
            column
            for column in candidate_columns
            if any(column in row for row in valid_candidates)
        ]

        st.dataframe(
            pd.DataFrame(valid_candidates)[available_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No candidates found.")

    # ========================================================
    # JOB OPENINGS
    # ========================================================
    st.divider()
    st.subheader("💼 Job Openings")

    if valid_jobs:
        st.dataframe(
            pd.DataFrame(valid_jobs),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No job openings found.")

    # ========================================================
    # LOGOUT
    # ========================================================
    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="admin_logout"
    ):
        st.session_state.role = None
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.session_state.candidate_id = None
        st.session_state.page = "landing"
        st.rerun()





# ============================================================
# CANDIDATE AI VOICE INTERVIEW
# ============================================================

def candidate_voice_interview_page():
    """Run a five-question AI voice interview for the logged-in candidate."""

    st.subheader("🎤 AI Voice Interview")
    st.write(
        "The AI asks exactly 5 questions based on your candidate profile "
        "and selected job. Record each answer with your microphone. "
        "Groq Whisper converts speech to text and Groq AI evaluates it."
    )

    if groq_client is None:
        st.error("GROQ_API_KEY is not configured.")
        st.info(
            "Add GROQ_API_KEY to your .env file and restart Streamlit."
        )
        return

    candidate_id = st.session_state.get("candidate_id")
    if not candidate_id:
        st.warning(
            "⚠️ Candidate ID was not returned during login. "
            "Please logout and login again."
        )
        return

    def parse_evaluation(text_value):
        result = {
            "feedback": "",
            "strengths": [],
            "improvement": "",
            "suggestions": ""
        }
        current = None

        for raw_line in str(text_value or "").splitlines():
            line = raw_line.strip()
            if not line:
                continue

            upper = line.upper()

            if upper.startswith("FEEDBACK:"):
                current = "feedback"
                result["feedback"] = line.split(":", 1)[1].strip()
                continue

            if upper.startswith("STRENGTHS:"):
                current = "strengths"
                continue

            if upper.startswith("IMPROVEMENT:"):
                current = "improvement"
                result["improvement"] = line.split(":", 1)[1].strip()
                continue

            if upper.startswith("SUGGESTIONS:"):
                current = "suggestions"
                result["suggestions"] = line.split(":", 1)[1].strip()
                continue

            if current == "feedback":
                result["feedback"] += (" " if result["feedback"] else "") + line
            elif current == "strengths":
                result["strengths"].append(line.lstrip("-• ").strip())
            elif current == "improvement":
                result["improvement"] += (" " if result["improvement"] else "") + line
            elif current == "suggestions":
                result["suggestions"] += (" " if result["suggestions"] else "") + line

        return result

    def reset_interview():
        st.session_state.candidate_voice_questions = []
        st.session_state.candidate_voice_question_index = 0
        st.session_state.candidate_voice_answers = []
        st.session_state.candidate_voice_scores = []
        st.session_state.candidate_voice_evaluations = []
        st.session_state.candidate_voice_started = False
        st.session_state.candidate_voice_finished = False
        st.session_state.candidate_voice_candidate_id = None
        st.session_state.candidate_voice_job_id = None
        st.session_state.candidate_voice_job_title = ""
        st.session_state.candidate_voice_transcript = ""
        st.session_state.candidate_voice_overall_analysis = ""
        st.session_state.candidate_voice_overall_feedback = ""
        st.session_state.candidate_voice_overall_strengths = []
        st.session_state.candidate_voice_overall_improvement = ""
        st.session_state.candidate_voice_overall_suggestions = ""
        st.session_state.candidate_voice_summary_saved = False

    try:
        # ------------------------------------------------------------
        # CANDIDATE PROFILE
        # ------------------------------------------------------------
        candidate_response = requests.get(
            f"{API_URL}/candidates",
            timeout=10
        )

        if candidate_response.status_code != 200:
            st.error(
                f"Unable to retrieve candidate profile. "
                f"Backend returned {candidate_response.status_code}."
            )
            return

        candidate_data = candidate_response.json()
        candidate_list = (
            candidate_data.get("candidates", [])
            if isinstance(candidate_data, dict)
            else candidate_data
        )

        candidate = next(
            (
                item for item in candidate_list
                if isinstance(item, dict)
                and str(item.get("id")) == str(candidate_id)
            ),
            None
        )

        if candidate is None:
            st.warning("Your candidate profile could not be found.")
            return

        # ------------------------------------------------------------
        # APPLICATIONS
        # ------------------------------------------------------------
        applications_response = requests.get(
            f"{API_URL}/candidate/{candidate_id}/applications",
            timeout=10
        )

        if applications_response.status_code != 200:
            st.error("Unable to retrieve your job applications.")
            return

        application_data = applications_response.json()
        applications = (
            application_data.get("applications", [])
            if isinstance(application_data, dict)
            else application_data
        )

        if not applications:
            st.info(
                "📭 You have not applied for any jobs yet. "
                "Apply for a job first and return here."
            )
            return

        eligible_statuses = {
            "shortlisted",
            "interview",
            "interview scheduled",
            "selected",
            "hired"
        }

        eligible = [
            app for app in applications
            if str(app.get("status", "Applied")).lower()
            in eligible_statuses
        ]

        # If the backend has not updated the status yet, allow the
        # interview so the complete AI workflow can still be demonstrated.
        interview_applications = eligible if eligible else applications

        labels = []
        lookup = {}

        for app in interview_applications:
            job_id = app.get("job_id", app.get("id"))
            label = (
                f"{app.get('job_title', 'Job')} — "
                f"{app.get('company_name', 'Company')} "
                f"(Job ID: {job_id})"
            )
            labels.append(label)
            lookup[label] = app

        selected_label = st.selectbox(
            "💼 Select Job for Interview",
            labels,
            key="candidate_voice_application_select"
        )
        selected_application = lookup[selected_label]
        selected_job_id = selected_application.get(
            "job_id",
            selected_application.get("id")
        )

        def stringify(value):
            if isinstance(value, list):
                return ", ".join(str(v) for v in value)
            return str(value or "N/A")

        candidate_profile = f"""
Name: {candidate.get("name", "N/A")}
Email: {candidate.get("email", "N/A")}
Phone: {candidate.get("phone", "N/A")}
Skills: {stringify(candidate.get("skills", []))}
Education: {stringify(candidate.get("education", []))}
Experience: {stringify(candidate.get("experience", []))}
Projects: {stringify(candidate.get("projects", []))}
Certifications: {stringify(candidate.get("certifications", []))}
Languages: {stringify(candidate.get("languages", []))}
Resume:
{candidate.get("resume_text", "")}
"""

        job_information = f"""
Job Title: {selected_application.get("job_title", "N/A")}
Company: {selected_application.get("company_name", "N/A")}
Location: {selected_application.get("location", "N/A")}
Salary: {selected_application.get("salary", "N/A")}
Employment Type: {selected_application.get("employment_type", "N/A")}
Experience: {selected_application.get("experience", "N/A")}
Education: {selected_application.get("education", "N/A")}
Skills: {stringify(selected_application.get("skills", []))}
Responsibilities: {stringify(selected_application.get("responsibilities", []))}
Job Description:
{selected_application.get("job_description", "")}
"""

        st.divider()

        # ------------------------------------------------------------
        # START
        # ------------------------------------------------------------
        if not st.session_state.candidate_voice_started:
            st.info(
                "Interview flow: 5 AI questions → voice answer → "
                "speech-to-text → AI evaluation → final performance report."
            )

            if st.button(
                "🚀 Start 5-Question AI Voice Interview",
                use_container_width=True,
                key="candidate_start_voice_interview"
            ):
                with st.spinner("Generating exactly 5 interview questions..."):
                    try:
                        prompt = f"""
You are an expert technical recruitment interviewer.

Generate exactly 5 interview questions for this candidate and job.

CANDIDATE:
{candidate_profile}

JOB:
{job_information}

Requirements:
- Exactly 5 questions.
- Relevant to the candidate and job.
- Include technical questions.
- Include project/experience questions.
- Include practical/problem-solving questions.
- Include one behavioral question.
- Do not provide answers.
- Return only the five numbered questions.
"""

                        completion = groq_client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are an expert recruitment interviewer."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=0.2
                        )

                        raw_questions = (
                            completion.choices[0].message.content or ""
                        )
                        questions = []

                        for raw_line in raw_questions.splitlines():
                            line = raw_line.strip()
                            if not line:
                                continue

                            cleaned = line
                            parts = cleaned.split(".", 1)
                            if len(parts) == 2 and parts[0].strip().isdigit():
                                cleaned = parts[1].strip()
                            else:
                                parts = cleaned.split(")", 1)
                                if len(parts) == 2 and parts[0].strip().isdigit():
                                    cleaned = parts[1].strip()

                            if cleaned:
                                questions.append(cleaned)

                        questions = questions[:5]

                        if len(questions) != 5:
                            st.error(
                                "The AI did not return exactly 5 questions. "
                                "Please click the start button again."
                            )
                        else:
                            st.session_state.candidate_voice_questions = questions
                            st.session_state.candidate_voice_question_index = 0
                            st.session_state.candidate_voice_answers = []
                            st.session_state.candidate_voice_scores = []
                            st.session_state.candidate_voice_evaluations = []
                            st.session_state.candidate_voice_candidate_id = candidate_id
                            st.session_state.candidate_voice_job_id = selected_job_id
                            st.session_state.candidate_voice_job_title = (
                                selected_application.get("job_title", "Job")
                            )
                            st.session_state.candidate_voice_transcript = ""
                            st.session_state.candidate_voice_overall_analysis = ""
                            st.session_state.candidate_voice_summary_saved = False
                            st.session_state.candidate_voice_started = True
                            st.session_state.candidate_voice_finished = False
                            st.rerun()

                    except Exception as e:
                        st.error(f"Question generation error: {e}")

        # ------------------------------------------------------------
        # ACTIVE INTERVIEW
        # ------------------------------------------------------------
        if (
            st.session_state.candidate_voice_started
            and not st.session_state.candidate_voice_finished
        ):
            questions = st.session_state.candidate_voice_questions
            index = st.session_state.candidate_voice_question_index

            if index < len(questions):
                question = questions[index]

                st.subheader(
                    f"🎤 Question {index + 1} of {len(questions)}"
                )
                st.progress((index + 1) / len(questions))
                st.info(question)

                st.write(
                    "🎙️ Record your answer using the microphone."
                )

                audio_value = st.audio_input(
                    "🎙️ Record your answer",
                    key=f"candidate_voice_audio_{index}"
                )

                if audio_value is not None:
                    st.audio(audio_value)
                    st.success("Audio recorded successfully.")

                    if st.button(
                        "📝 Convert Speech to Text",
                        use_container_width=True,
                        key=f"candidate_transcribe_{index}"
                    ):
                        try:
                            with st.spinner("Converting speech to text..."):
                                transcription = (
                                    groq_client.audio.transcriptions.create(
                                        file=(
                                            "candidate_answer.wav",
                                            audio_value.getvalue()
                                        ),
                                        model="whisper-large-v3-turbo",
                                        language="en",
                                        temperature=0
                                    )
                                )

                                transcript = (
                                    getattr(transcription, "text", "") or ""
                                ).strip()

                                if not transcript:
                                    st.warning(
                                        "No speech was detected. "
                                        "Please record again."
                                    )
                                else:
                                    st.session_state.candidate_voice_transcript = transcript
                                    st.rerun()

                        except Exception as e:
                            st.error(f"Speech-to-text error: {e}")

                transcript = st.session_state.candidate_voice_transcript

                if transcript:
                    st.subheader("📝 Transcribed Answer")
                    st.text_area(
                        "Your answer",
                        transcript,
                        height=180,
                        disabled=True,
                        key=f"candidate_transcript_display_{index}"
                    )

                    if st.button(
                        "🤖 Evaluate Answer & Continue",
                        use_container_width=True,
                        key=f"candidate_evaluate_{index}"
                    ):
                        with st.spinner("AI is evaluating your answer..."):
                            try:
                                evaluation_prompt = f"""
You are an objective expert recruitment interviewer.

JOB:
{job_information}

QUESTION:
{question}

CANDIDATE ANSWER:
{transcript}

Evaluate only the candidate's actual answer.

Consider technical correctness, relevance, completeness,
clarity, practical knowledge and communication.

Return EXACTLY:

SCORE: <0-100>
FEEDBACK:
<2-3 specific sentences>
STRENGTHS:
- <specific strength>
- <specific strength>
IMPROVEMENT:
<specific weakness or improvement area>
SUGGESTIONS:
<one practical suggestion>
"""

                                evaluation_completion = (
                                    groq_client.chat.completions.create(
                                        model="openai/gpt-oss-20b",
                                        messages=[
                                            {
                                                "role": "system",
                                                "content": (
                                                    "You are an objective "
                                                    "technical interviewer."
                                                )
                                            },
                                            {
                                                "role": "user",
                                                "content": evaluation_prompt
                                            }
                                        ],
                                        temperature=0.2
                                    )
                                )

                                evaluation_text = (
                                    evaluation_completion
                                    .choices[0]
                                    .message
                                    .content
                                    or ""
                                )

                                score = 0.0
                                for raw_line in evaluation_text.splitlines():
                                    if raw_line.strip().upper().startswith("SCORE:"):
                                        try:
                                            score = float(
                                                raw_line.split(":", 1)[1]
                                                .strip()
                                                .replace("%", "")
                                            )
                                        except Exception:
                                            score = 0.0
                                        break

                                score = max(0.0, min(100.0, score))

                                st.session_state.candidate_voice_answers.append(
                                    {
                                        "question": question,
                                        "answer": transcript
                                    }
                                )
                                st.session_state.candidate_voice_scores.append(score)
                                st.session_state.candidate_voice_evaluations.append(
                                    evaluation_text
                                )

                                try:
                                    save_response = requests.post(
                                        f"{API_URL}/save-interview-result",
                                        json={
                                            "candidate_id": int(candidate_id),
                                            "job_id": selected_job_id,
                                            "question": question,
                                            "answer": transcript,
                                            "score": score,
                                            "feedback": evaluation_text
                                        },
                                        timeout=10
                                    )
                                    if save_response.status_code not in [200, 201]:
                                        st.warning(
                                            "Question evaluation completed, but "
                                            "the database save failed."
                                        )
                                except Exception as save_error:
                                    st.warning(
                                        f"Could not save question result: {save_error}"
                                    )

                                st.session_state.candidate_voice_transcript = ""
                                st.session_state.candidate_voice_question_index += 1

                                if (
                                    st.session_state.candidate_voice_question_index
                                    >= len(questions)
                                ):
                                    st.session_state.candidate_voice_finished = True

                                st.rerun()

                            except Exception as e:
                                st.error(f"AI evaluation error: {e}")

        # ------------------------------------------------------------
        # FINAL RESULT
        # ------------------------------------------------------------
        if st.session_state.candidate_voice_finished:
            questions = st.session_state.candidate_voice_questions
            answers = st.session_state.candidate_voice_answers
            scores = st.session_state.candidate_voice_scores
            evaluations = st.session_state.candidate_voice_evaluations

            final_score = (
                sum(scores) / len(scores)
                if scores else 0.0
            )

            st.divider()
            st.title("🏆 AI Voice Interview Result")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("🎯 Final Score", f"{final_score:.1f}%")
            with c2:
                st.metric("📋 Questions", len(questions))
            with c3:
                st.metric("✅ Answered", len(answers))

            st.progress(min(max(final_score / 100.0, 0.0), 1.0))

            # Overall analysis is generated only once per interview.
            if not st.session_state.candidate_voice_overall_analysis:
                summary_text = ""

                for i, evaluation in enumerate(evaluations):
                    parsed = parse_evaluation(evaluation)
                    summary_text += f"""
Question {i + 1}
Score: {scores[i]:.1f}%
Feedback: {parsed["feedback"]}
Strengths: {", ".join(parsed["strengths"])}
Improvement: {parsed["improvement"]}
Suggestions: {parsed["suggestions"]}
"""

                overall_prompt = f"""
You are a senior recruitment evaluator.

Analyze this complete five-question voice interview.

JOB:
{job_information}

FINAL SCORE:
{final_score:.1f}%

QUESTION-WISE EVALUATIONS:
{summary_text}

Return EXACTLY:

RECOMMENDATION:
<Strong Candidate OR Suitable Candidate OR Needs Further Review OR Weak Candidate>

FEEDBACK:
<2-3 sentences>

STRENGTHS:
- <strength 1>
- <strength 2>
- <strength 3>

IMPROVEMENT:
<specific areas to improve>

SUGGESTIONS:
<practical suggestions for future interviews>
"""

                try:
                    overall_completion = (
                        groq_client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a senior recruitment evaluator."
                                },
                                {
                                    "role": "user",
                                    "content": overall_prompt
                                }
                            ],
                            temperature=0.2
                        )
                    )
                    st.session_state.candidate_voice_overall_analysis = (
                        overall_completion
                        .choices[0]
                        .message
                        .content
                        or ""
                    )
                except Exception as e:
                    st.session_state.candidate_voice_overall_analysis = (
                        f"FEEDBACK: Interview completed with a final score of "
                        f"{final_score:.1f}%."
                    )
                    st.warning(f"Overall analysis error: {e}")

            overall = parse_evaluation(
                st.session_state.candidate_voice_overall_analysis
            )

            recommendation = ""
            for raw_line in str(
                st.session_state.candidate_voice_overall_analysis
            ).splitlines():
                if raw_line.strip().upper().startswith("RECOMMENDATION:"):
                    recommendation = raw_line.split(":", 1)[1].strip()
                    break

            if not recommendation:
                if final_score >= 80:
                    recommendation = "Strong Candidate"
                elif final_score >= 65:
                    recommendation = "Suitable Candidate"
                elif final_score >= 50:
                    recommendation = "Needs Further Review"
                else:
                    recommendation = "Weak Candidate"

            st.subheader("🤖 AI Recommendation")
            if "Strong" in recommendation:
                st.success(f"🌟 {recommendation}")
            elif "Suitable" in recommendation:
                st.success(f"✅ {recommendation}")
            elif "Review" in recommendation:
                st.warning(f"⚠️ {recommendation}")
            else:
                st.error(f"❌ {recommendation}")

            st.subheader("💬 Overall Feedback")
            st.info(overall["feedback"] or "No overall feedback available.")

            st.subheader("💪 Overall Strengths")
            if overall["strengths"]:
                for strength in overall["strengths"]:
                    st.success(f"✓ {strength}")
            else:
                st.info("No strengths identified.")

            st.subheader("📈 Areas for Improvement")
            st.warning(
                overall["improvement"] or "No improvement areas available."
            )

            st.subheader("💡 Suggestions")
            st.info(
                overall["suggestions"]
                or "Continue practising technical, project and behavioural answers."
            )

            # --------------------------------------------------------
            # SAVE SCREENING SUMMARY
            # --------------------------------------------------------
            if not st.session_state.candidate_voice_summary_saved:
                combined_improvement = overall["improvement"]
                if overall["suggestions"]:
                    combined_improvement += (
                        "\nSuggestions: " + overall["suggestions"]
                    )

                try:
                    summary_response = requests.post(
                        f"{API_URL}/save-screening-summary",
                        json={
                            "candidate_id": int(candidate_id),
                            "overall_score": float(final_score),
                            "recommendation": recommendation,
                            "strengths": "\n".join(overall["strengths"]),
                            "improvement": combined_improvement
                        },
                        timeout=10
                    )

                    if summary_response.status_code in [200, 201]:
                        st.session_state.candidate_voice_summary_saved = True
                        st.success(
                            "✅ Interview performance saved successfully."
                        )
                    else:
                        st.warning(
                            "Interview finished, but the final screening "
                            "summary was not saved by the backend."
                        )
                except Exception as e:
                    st.warning(
                        f"Final screening summary save error: {e}"
                    )

            # --------------------------------------------------------
            # QUESTION-WISE EVALUATION
            # --------------------------------------------------------
            st.divider()
            st.subheader("📋 Question-wise Evaluation")

            for i, answer_data in enumerate(answers):
                score_value = scores[i] if i < len(scores) else 0.0
                parsed = (
                    parse_evaluation(evaluations[i])
                    if i < len(evaluations)
                    else {}
                )

                with st.expander(
                    f"Question {i + 1} — Score: {score_value:.1f}%"
                ):
                    st.markdown("**Question:**")
                    st.write(answer_data.get("question", "N/A"))

                    st.markdown("**Candidate Answer:**")
                    st.write(answer_data.get("answer", "N/A"))

                    st.metric(
                        "Question Score",
                        f"{score_value:.1f}%"
                    )

                    st.markdown("**🤖 AI Feedback:**")
                    st.info(
                        parsed.get("feedback", "")
                        or "No feedback available."
                    )

                    st.markdown("**💪 Strengths:**")
                    if parsed.get("strengths"):
                        for strength in parsed["strengths"]:
                            st.success(f"✓ {strength}")
                    else:
                        st.write("No specific strengths identified.")

                    st.markdown("**📈 Improvement:**")
                    st.warning(
                        parsed.get("improvement", "")
                        or "No improvement suggestion available."
                    )

                    st.markdown("**💡 Suggestion:**")
                    st.info(
                        parsed.get("suggestions", "")
                        or "Keep answers specific, relevant and structured."
                    )

            st.divider()

            if st.button(
                "🔄 Start New AI Voice Interview",
                use_container_width=True,
                key="candidate_restart_voice_interview"
            ):
                reset_interview()
                st.rerun()

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend is not running. Please start FastAPI first.")
    except Exception as e:
        st.error(f"❌ Candidate AI interview error: {e}")



# ============================================================
# CANDIDATE DASHBOARD
# ============================================================

def candidate_dashboard():

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="text-align:center; padding:30px 20px 20px 20px;">
            <h1 style="color:#2563EB;">
                👨‍🎓 Candidate Dashboard
            </h1>
            <p style="font-size:18px; color:#666;">
                Manage your profile, applications and interview performance
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.title("👨‍🎓 Candidate Menu")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "👤 My Profile",
            "📤 Upload Resume",
            "🔎 Available Jobs",
            "💼 Applied Jobs",
            "📋 Application Status",
            "📩 Messages",
            "🎤 Interview",
            "🤖 AI Interview Questions",
            "📊 Interview Performance",
            "💬 Contact Recruiter"
        ]
    )
    # ====================================================
    # MESSAGES / INBOX
    # ====================================================

    if menu == "📩 Messages":

        st.title("📩 Messages")
        st.subheader("Recruiter Messages")

        # Get logged-in candidate ID
        candidate_id = st.session_state.get("candidate_id")

        if not candidate_id:

            st.error("❌ Candidate ID not found. Please login again.")

        else:

            try:

                response = requests.get(
                    f"{API_URL}/candidate/{candidate_id}/messages",
                    timeout=30
                )

                if response.status_code == 200:

                    data = response.json()
                    messages = data.get("messages", [])

                    if messages:

                        st.success(
                            f"📬 You have {len(messages)} recruiter message(s)."
                        )

                        for msg in messages:

                            subject = msg.get("subject") or "No Subject"
                            message_text = msg.get("message") or ""
                            sender = msg.get("sender") or "Recruiter"
                            created_at = msg.get("created_at") or ""

                            with st.expander(f"📩 {message_text}"):

                                st.write(f"**From:** {sender}")
                                st.write(f"**Date:** {created_at}")

                                st.divider()

                                
                                st.write(f"**Message:** {message_text}")

                    else:

                        st.info("📭 No recruiter messages available.")

                        st.write(
                            "Messages from recruiters will appear here when a recruiter "
                            "sends you a message."
                        )

                else:

                    st.error(
                        f"❌ Unable to fetch messages. Status code: "
                        f"{response.status_code}"
                    )

                    try:
                        st.error(response.json().get("detail", "Unknown error"))
                    except:
                        pass

            except Exception as e:

                st.error(f"❌ Error connecting to backend: {e}")
    # ====================================================
    # MY PROFILE
    # ====================================================

    elif menu == "👤 My Profile":

        st.title("👤 My Profile")
        candidate_id = st.session_state.get("candidate_id")
        if not candidate_id:
            st.error("❌ Candidate ID not found. Please login again.")
        else:
            st.success(f"🆔 Candidate ID: {candidate_id}")

        

            try:

                response = requests.get(
                    f"{API_URL}/candidate/{candidate_id}",
                    timeout=10
                )

                if response.status_code == 200:

                    candidate = response.json()

                    name = candidate.get("name", "")
                    email = candidate.get("email", "")
                    phone = candidate.get("phone", "")
                    skills = candidate.get("skills", "")
                    education = candidate.get("education", "")
                    experience = candidate.get("experience", "")

                else:

                    st.error(
                        f"❌ Could not load profile: {response.text}"
                    )

                    name = ""
                    email = ""
                    phone = ""
                    skills = ""
                    education = ""
                    experience = ""

            except Exception as e:

                st.error(
                    f"❌ Error loading profile: {str(e)}"
                )

                name = ""
                email = ""
                phone = ""
                skills = ""
                education = ""
                experience = ""


            # ====================================================
            # PROFILE FORM
            # ====================================================

            full_name = st.text_input(
                "Full Name",
                value=name,
                key="profile_name"
            )

            phone_input = st.text_input(
                "Phone",
                value=phone,
                key="profile_phone"
            )

            email_input = st.text_input(
                "Email",
                value=email,
                key="profile_email"
            )

            skills_input = st.text_input(
                "Skills",
                value=skills,
                key="profile_skills"
            )

            education_input = st.text_area(
                "Education",
                value=education,
                key="profile_education"
            )

            experience_input = st.text_area(
                "Experience",
                value=experience,
                key="profile_experience"
            )

            # ====================================================
            # SAVE PROFILE
            # ====================================================

            if st.button(
                "💾 Save Profile",
                use_container_width=True
            ):

                try:

                    profile_data = {
                        "name": full_name,
                        "email": email_input,
                        "phone": phone_input,
                        "skills": skills_input,
                        "education": education_input,
                        "experience": experience_input
                    }

                    response = requests.put(
                        f"{API_URL}/candidate/{candidate_id}/profile",
                        data=profile_data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:

                        st.success(
                            "✅ Profile saved successfully!"
                        )

                    else:

                        st.error(
                            f"❌ Failed to save profile: {response.text}"
                        )

                except Exception as e:

                    st.error(
                        f"❌ Error saving profile: {str(e)}"
                    )
    # ==================================================== 
    # UPLOAD RESUME 
    # ==================================================== 
 
    elif menu == "📤 Upload Resume": 
 
        st.title("📤 Upload Resume") 
 
        st.write( 
            "Upload your latest resume to update your candidate profile." 
        ) 
 
        uploaded_resume = st.file_uploader( 
            "Choose your Resume", 
            type=["pdf", "docx"], 
            key="candidate_resume_upload" 
        ) 
 
        if uploaded_resume is not None: 
 
            st.success( 
                f"Selected Resume: {uploaded_resume.name}" 
            ) 
 
            if st.button( 
                "📤 Upload & Update Resume", 
                use_container_width=True 
            ): 
 
                try: 
 
                    candidate_id = st.session_state.get( 
                        "candidate_id" 
                    ) 
 
                    if not candidate_id: 
 
                        st.error( 
                            "❌ Candidate ID not found. Please login again." 
                        ) 
 
                    else: 
 
                        files = { 
                            "file": ( 
                                uploaded_resume.name, 
                                uploaded_resume.getvalue(), 
                                uploaded_resume.type 
                            ) 
                        } 
 
                        response = requests.post( 
                            f"{API_URL}/candidate/{candidate_id}/upload-resume", 
                            files=files, 
                            timeout=30 
                        ) 
 
                        if response.status_code == 200: 
 
                            result = response.json() 
 
                            st.success( 
                                "✅ Resume uploaded and profile updated successfully!" 
                            ) 
 
                        else: 
 
                            st.error( 
                                f"❌ Upload failed: {response.text}" 
                            ) 
 
                except Exception as e: 
 
                    st.error( 
                        f"❌ Error uploading resume: {str(e)}" 
                    ) 
 
 


    # ========================================================
    # 2. AVAILABLE JOBS
    # ========================================================

    elif menu == "🔎 Available Jobs":

        st.subheader("🔎 Available Jobs")

        st.write(
            "Browse available job openings and apply for a position."
        )

        # ----------------------------------------------------
        # Get logged-in candidate ID
        # ----------------------------------------------------

        candidate_id = st.session_state.get(
            "candidate_id"
        )

        if not candidate_id:

            st.warning(
                "⚠️ Candidate information not found. "
                "Please login again."
            )

        else:

            try:

                # ------------------------------------------------
                # Get jobs from backend
                # ------------------------------------------------

                response = requests.get(
                    "http://127.0.0.1:8000/jobs"
                )

                # ------------------------------------------------
                # Successful response
                # ------------------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    jobs = data.get(
                        "jobs",
                        []
                    )

                    # --------------------------------------------
                    # No jobs
                    # --------------------------------------------

                    if not jobs:

                        st.info(
                            "📭 No jobs are available at the moment."
                        )

                    # --------------------------------------------
                    # Display jobs
                    # --------------------------------------------

                    else:

                        st.success(
                            f"💼 {len(jobs)} job openings available."
                        )

                        for job in jobs:

                            st.markdown("---")

                            # ------------------------------------
                            # Job title
                            # ------------------------------------

                            st.markdown(
                                f"### 💼 {job.get('job_title', 'Not Available')}"
                            )

                            # ------------------------------------
                            # Job information
                            # ------------------------------------

                            col1, col2 = st.columns(2)

                            with col1:

                                st.write(
                                    f"🏢 **Company:** "
                                    f"{job.get('company_name', 'N/A')}"
                                )

                                st.write(
                                    f"📍 **Location:** "
                                    f"{job.get('location', 'N/A')}"
                                )

                                st.write(
                                    f"💰 **Salary:** "
                                    f"{job.get('salary', 'N/A')}"
                                )

                            with col2:

                                st.write(
                                    f"🕐 **Employment Type:** "
                                    f"{job.get('employment_type', 'N/A')}"
                                )

                                st.write(
                                    f"📚 **Experience:** "
                                    f"{job.get('experience', 'N/A')}"
                                )

                                st.write(
                                    f"🎓 **Education:** "
                                    f"{job.get('education', 'N/A')}"
                                )

                            # ------------------------------------
                            # Skills
                            # ------------------------------------

                            skills_list = job.get(
                                "skills",
                                []
                            )

                            if skills_list:

                                st.write(
                                    "🛠️ **Required Skills:**"
                                )

                                if isinstance(
                                    skills_list,
                                    list
                                ):

                                    st.write(
                                        ", ".join(
                                            str(skill)
                                            for skill in skills_list
                                        )
                                    )

                                else:

                                    st.write(
                                        str(skills_list)
                                    )

                            # ------------------------------------
                            # Responsibilities
                            # ------------------------------------

                            responsibilities = job.get(
                                "responsibilities",
                                []
                            )

                            if responsibilities:

                                with st.expander(
                                    "📋 View Responsibilities"
                                ):

                                    if isinstance(
                                        responsibilities,
                                        list
                                    ):

                                        for responsibility in responsibilities:

                                            st.write(
                                                f"• {responsibility}"
                                            )

                                    else:

                                        st.write(
                                            str(responsibilities)
                                        )

                            # ------------------------------------
                            # Full Job Description
                            # ------------------------------------

                            job_description = job.get(
                                "job_description",
                                ""
                            )

                            if job_description:

                                with st.expander(
                                    "📄 View Full Job Description"
                                ):

                                    st.write(
                                        job_description
                                    )

                            # ------------------------------------
                            # APPLY NOW
                            # ------------------------------------

                            job_id = job.get(
                                "id"
                            )

                            if st.button(
                                "📨 Apply Now",
                                key=f"apply_job_{job_id}",
                                use_container_width=True
                            ):

                                try:

                                    apply_response = requests.post(
                                        "http://127.0.0.1:8000/apply-job",
                                        data={
                                            "candidate_id": candidate_id,
                                            "job_id": job_id
                                        }
                                    )

                                    if apply_response.status_code == 200:

                                        apply_data = (
                                            apply_response.json()
                                        )

                                        if apply_data.get(
                                            "success",
                                            True
                                        ):

                                            st.success(
                                                "✅ Application submitted successfully!"
                                            )

                                        else:

                                            st.warning(
                                                f"⚠️ "
                                                f"{apply_data.get(
                                                    'message',
                                                    'Unable to apply.'
                                                )}"
                                            )

                                    else:

                                        st.error(
                                            "❌ Unable to submit application. "
                                            f"Backend returned status "
                                            f"{apply_response.status_code}."
                                        )

                                except requests.exceptions.ConnectionError:

                                    st.error(
                                        "❌ Backend is not running. "
                                        "Please start FastAPI first."
                                    )

                                except Exception as e:

                                    st.error(
                                        f"❌ Error while applying: {str(e)}"
                                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend is not running. "
                    "Please start FastAPI first."
                )

            except Exception as e:

                st.error(
                    f"❌ Error while loading jobs: {str(e)}"
                )

    # ========================================================
    # 3. APPLIED JOBS
    # ========================================================

    elif menu == "💼 Applied Jobs":

        st.subheader("💼 Applied Jobs")

        st.write(
            "View jobs that you have applied for."
        )

        # ----------------------------------------------------
        # Get logged-in candidate ID
        # ----------------------------------------------------

        candidate_id = st.session_state.get(
            "candidate_id"
        )

        if not candidate_id:

            st.warning(
                "⚠️ Candidate information not found. "
                "Please login again."
            )

        else:

            try:

                response = requests.get(
                    f"http://127.0.0.1:8000/candidate/{candidate_id}/applications"
                )

                if response.status_code == 200:

                    data = response.json()

                    applications = data.get(
                        "applications",
                        []
                    )

                    # ----------------------------------------
                    # No applications
                    # ----------------------------------------

                    if not applications:

                        st.info(
                            "📭 You have not applied for any jobs yet."
                        )

                    # ----------------------------------------
                    # Display applications
                    # ----------------------------------------

                    else:

                        st.success(
                            f"📋 Total Applications: "
                            f"{len(applications)}"
                        )

                        for application in applications:

                            st.markdown("---")

                            st.markdown(
                                f"""
                                ### 💼 {application.get("job_title", "N/A")}

                                **🏢 Company:**  
                                {application.get("company_name", "N/A")}

                                **📍 Location:**  
                                {application.get("location", "N/A")}

                                **💰 Salary:**  
                                {application.get("salary", "N/A")}

                                **🕐 Employment Type:**  
                                {application.get("employment_type", "N/A")}

                                **📚 Experience:**  
                                {application.get("experience", "N/A")}

                                **📊 Application Status:**  
                                🟢 {application.get("status", "Applied")}

                                **📅 Applied On:**  
                                {application.get("applied_at", "N/A")}
                                """
                            )

                else:

                    st.error(
                        f"❌ Unable to load applications. "
                        f"Backend returned status "
                        f"{response.status_code}."
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend is not running. "
                    "Please start FastAPI first."
                )

            except Exception as e:

                st.error(
                    f"❌ Error while loading applications: {str(e)}"
                )

    # ========================================================
    # 4. APPLICATION STATUS
    # ========================================================

    # ========================================================
    # 4. APPLICATION STATUS
    # ========================================================
    elif menu == "📋 Application Status":
        st.subheader("📋 Application Status")
        st.write(
            "Track the status of your job applications."
        )
        # ----------------------------------------------------
        # Get logged-in candidate ID
        # ----------------------------------------------------
        candidate_id = st.session_state.get("candidate_id")
        if not candidate_id:
            st.warning(
                "⚠️ Candidate information not found. "
                "Please login again."
            )
        else:
            try:
                # ------------------------------------------------
                # Get candidate's current recruiter status
                # ------------------------------------------------
                candidate_status = None
                candidate_response = requests.get(
                    f"{API_URL}/candidates",
                    timeout=10
                )

                if candidate_response.status_code == 200:
                    candidate_items = candidate_response.json()
                    candidate_items = (
                        candidate_items.get("candidates", [])
                        if isinstance(candidate_items, dict)
                        else candidate_items
                    )

                    for item in candidate_items:
                        if str(item.get("id")) == str(candidate_id):
                            candidate_status = item.get("status")
                            break

                # ------------------------------------------------
                # Get logged-in candidate applications from backend
                # ------------------------------------------------
                response = requests.get(
                    f"{API_URL}/candidate/{candidate_id}/applications",
                    timeout=10
                )
                if response.status_code == 200: 
                    data = response.json() 
                    applications = data.get( 
                        "applications", 
                        [] 
                    ) 
                    # ------------------------------------------------ 
                    # No applications 
                    # ------------------------------------------------ 
                    if not applications: 
                        st.info( 
                            "📭 You have not applied for any jobs yet." 
                        ) 

                    # ------------------------------------------------ 
                    # Display application status 
                    # ------------------------------------------------ 
                    else: 
                        st.success( 
                            f"📋 {len(applications)} application(s) found." 
                    ) 

                    for application in applications: 

                        st.markdown("---") 

                        job_title = application.get( 
                            "job_title", 
                            "N/A" 
                        ) 

                        company_name = application.get( 
                            "company_name", 
                            "N/A" 
                        ) 

                        location = application.get( 
                            "location", 
                            "N/A" 
                        ) 

                        application_status = application.get(
                            "status",
                            "Applied"
                        )

                        # Recruiter decisions are saved through the
                        # candidate status endpoint. Use that status for
                        # the candidate portal when the application itself
                        # has not yet received a final status.
                        final_candidate_statuses = {
                            "hired",
                            "selected",
                            "shortlisted",
                            "rejected"
                        }

                        if (
                            candidate_status
                            and str(application_status).lower()
                            not in final_candidate_statuses
                        ):
                            status = candidate_status
                        else:
                            status = application_status

                        applied_at = application.get( 
                            "applied_at", 
                            "N/A" 
                        ) 

                        # ---------------------------------------- 
                        # Status display 
                        # ---------------------------------------- 

                        status_lower = str( 
                            status 
                        ).lower() 

                        if status_lower == "selected": 

                            status_display = "🟢 Selected" 

                        elif status_lower == "shortlisted": 

                            status_display = "🔵 Shortlisted" 

                        elif status_lower == "rejected": 

                            status_display = "🔴 Rejected" 

                        elif status_lower in [ 
                            "interview", 
                            "interview scheduled" 
                        ]: 

                            status_display = "🟣 Interview Scheduled" 

                        else: 

                            status_display = "🟡 Applied" 

                        # ---------------------------------------- 
                        # Application card 
                        # ---------------------------------------- 

                        st.markdown( 
                            f""" 
                            ### 💼 {job_title} 

                            **🏢 Company:**   
                            {company_name} 

                            **📍 Location:**   
                            {location} 

                            **📊 Application / Hiring Status:**   
                            {status_display} 

                            **👨‍💼 Recruiter Decision:**   
                            {status_display if str(status).lower() in ["hired", "selected", "shortlisted", "rejected"] else "⏳ Under Review"}

                            **📅 Applied On:**   
                            {applied_at} 
                            """ 
                        ) 
                else: 
                    st.error( 
                        f"❌ Unable to load application status. " 
                        f"Backend returned status " 
                        f"{response.status_code}." 
                    ) 
            except requests.exceptions.ConnectionError: 
                st.error( 
                    "❌ Backend is not running. " 
                    "Please start FastAPI first." 
                ) 
            except Exception as e: 
                st.error( 
                    f"❌ Error while loading application status: {str(e)}" 
                ) 



    # ======================================================== 
    # 5. INTERVIEW 
    # ======================================================== 
    elif menu == "🎤 Interview": 
        candidate_voice_interview_page() 

    # ============================================================ 
    # INTERVIEW PERFORMANCE 
    # ============================================================ 
    elif menu == "🤖 AI Interview Questions":

        st.title("🤖 AI Interview Questions & Practice")
        st.write(
            "Use this page before the real interview to practice questions "
            "based on your resume and the selected job. The live Voice Interview "
            "does not reveal the sample answers."
        )

        st.info(
            "🎯 Purpose: prepare for the interview. Each question includes "
            "what the interviewer is probing and, in Practice Mode, a sample "
            "answer/key points."
        )

        candidate_resume = st.file_uploader(
            "📄 Upload Your Resume",
            type=["pdf", "docx"],
            key="candidate_ai_interview_resume"
        )

        candidate_job_id = st.number_input(
            "💼 Enter Job ID",
            min_value=1,
            step=1,
            key="candidate_ai_interview_job_id"
        )

        if "practice_interview_items" not in st.session_state:
            st.session_state.practice_interview_items = []

        if st.button(
            "🤖 Generate Interview Questions",
            use_container_width=True,
            key="candidate_generate_interview_questions"
        ):
            if candidate_resume is None:
                st.warning("Please upload your resume first.")
            else:
                try:
                    with st.spinner("Generating interview questions..."):
                        response = requests.post(
                            f"{API_URL}/ai-interview-questions",
                            files={
                                "resume": (
                                    candidate_resume.name,
                                    candidate_resume.getvalue(),
                                    candidate_resume.type
                                )
                            },
                            data={"job_id": candidate_job_id},
                            timeout=30
                        )

                    if response.status_code == 200:
                        result = response.json()
                        raw_questions = result.get(
                            "interview_questions",
                            result.get("questions", [])
                        )

                        if isinstance(raw_questions, str):
                            raw_questions = [
                                line.strip(" -•")
                                for line in raw_questions.splitlines()
                                if line.strip()
                            ]

                        questions = [str(q).strip() for q in raw_questions if str(q).strip()]
                        questions = questions[:10]

                        if not questions:
                            st.warning("The backend returned no interview questions.")
                        else:
                            # Build practice guidance. This is deliberately separate
                            # from the live voice interview so answers are never
                            # exposed while the candidate is being evaluated.
                            items = []
                            for question in questions:
                                items.append({
                                    "question": question,
                                    "probing": "The interviewer is checking whether you understand the concept, can explain it clearly, and can connect it to the job or your project experience.",
                                    "answer": ""
                                })

                            # Ask Groq for preparation guidance when available.
                            if groq_client is not None:
                                prep_prompt = f"""
You are an expert technical interview coach.

For each interview question below, provide:
1. WHAT_IT_PROBES: what skill, knowledge or evidence the interviewer is checking.
2. SAMPLE_ANSWER: a concise model answer or key answer points suitable for a fresher.

Questions:
{chr(10).join(f'{i+1}. {q}' for i, q in enumerate(questions))}

Return exactly in this format for every question:
QUESTION 1
WHAT_IT_PROBES: ...
SAMPLE_ANSWER: ...

QUESTION 2
WHAT_IT_PROBES: ...
SAMPLE_ANSWER: ...

Continue for all questions. Do not invent personal experience for the candidate.
"""
                                try:
                                    prep_completion = groq_client.chat.completions.create(
                                        model="openai/gpt-oss-20b",
                                        messages=[
                                            {
                                                "role": "system",
                                                "content": "You are a professional interview preparation coach."
                                            },
                                            {
                                                "role": "user",
                                                "content": prep_prompt
                                            }
                                        ],
                                        temperature=0.2
                                    )
                                    prep_text = (
                                        prep_completion.choices[0].message.content or ""
                                    )

                                    current_index = None
                                    for line in prep_text.splitlines():
                                        stripped = line.strip()
                                        upper = stripped.upper()

                                        if upper.startswith("QUESTION "):
                                            try:
                                                number = int(
                                                    stripped.split()[1].rstrip(":")
                                                )
                                                current_index = number - 1
                                            except Exception:
                                                current_index = None

                                        elif current_index is not None and 0 <= current_index < len(items):
                                            if upper.startswith("WHAT_IT_PROBES:"):
                                                items[current_index]["probing"] = stripped.split(":", 1)[1].strip()
                                            elif upper.startswith("SAMPLE_ANSWER:"):
                                                items[current_index]["answer"] = stripped.split(":", 1)[1].strip()
                                            elif items[current_index]["answer"] and not upper.startswith("QUESTION "):
                                                # Continue a multi-line sample answer.
                                                items[current_index]["answer"] += " " + stripped
                                except Exception as prep_error:
                                    st.warning(
                                        f"Questions were generated, but preparation guidance could not be created: {prep_error}"
                                    )

                            st.session_state.practice_interview_items = items
                            st.success("✅ Interview questions generated successfully.")
                    else:
                        st.error(
                            "Unable to generate interview questions. "
                            f"Backend status: {response.status_code}"
                        )
                        try:
                            st.json(response.json())
                        except Exception:
                            st.write(response.text)

                except requests.RequestException as e:
                    st.error(f"Unable to connect to the backend: {e}")
                except Exception as e:
                    st.error(f"Interview question generation error: {e}")

        items = st.session_state.get("practice_interview_items", [])

        if items:
            st.divider()
            st.subheader("📝 Generated Interview Questions")
            st.caption(
                "These are preparation materials. During the actual Voice Interview, "
                "the candidate answers without seeing the sample answers."
            )

            show_answers = st.checkbox(
                "👁️ Show sample answers and what the interviewer is probing",
                value=False,
                key="show_interview_practice_answers"
            )

            for number, item in enumerate(items, start=1):
                with st.container(border=True):
                    st.markdown(f"### Question {number}")
                    st.write(item["question"])

                    if show_answers:
                        st.markdown("**🔍 What is the interviewer probing?**")
                        st.write(item.get("probing") or "Concept understanding, relevance, clarity and practical application.")

                        st.markdown("**✅ Sample answer / key points**")
                        st.write(
                            item.get("answer")
                            or "Prepare a concise answer using the concept, an example, and how it relates to the job."
                        )

                    st.markdown("**💡 Preparation tip:**")
                    st.write(
                        "Answer in your own words. For technical questions, explain the concept, "
                        "give a small example, and connect it to your project or coursework when relevant."
                    )

            st.divider()
            st.success(
                "🎤 Ready for the real interview? Open **Interview** from the candidate menu. "
                "The live interview records your answer, converts speech to text and evaluates it."
            )

    elif menu == "📊 Interview Performance": 

        st.title("📊 Interview Performance") 
        st.write( 
            "View your AI-powered voice interview performance " 
            "and detailed evaluation." 
        ) 

        candidate_id = st.session_state.get("candidate_id") 
        

        if not candidate_id: 
            st.info("📋 No interview performance is available yet.") 
            st.write( 
                "Complete a Voice-Based Screening interview " 
                "to view your interview performance here." 
            ) 
        else: 
            try: 
                # ==================================================== 
                # GET SCREENING SUMMARY 
                # ==================================================== 
                response = requests.get( 
                    f"{API_URL}/screening-summary/{candidate_id}", 
                    timeout=10 
                ) 

                

                if response.status_code != 200: 
                    st.error( 
                        "Unable to retrieve interview performance " 
                        "from the backend." 
                    ) 
                else: 
                    data = response.json() 
                    latest_result = data.get("summary") 

                    if not latest_result: 
                        st.info( 
                            "📋 No interview performance is available yet." 
                        ) 
                    else: 
                        # ==================================================== 
                        # GET QUESTION-WISE DATABASE RESULTS 
                        # ==================================================== 
                        interview_response = requests.get( 
                            f"{API_URL}/interview-results/{candidate_id}", 
                            timeout=10 
                        ) 

                        if interview_response.status_code == 200: 
                            interview_data = interview_response.json() 
                            interview_results = interview_data.get( 
                                "results", [] 
                            ) 
                        else: 
                            interview_results = [] 

                        # Protect against malformed API data. 
                        interview_results = [ 
                            result 
                            for result in interview_results 
                            if isinstance(result, dict) 
                        ] 

                        # ==================================================== 
                        # USE SAVED DATABASE SUMMARY 
                        # ==================================================== 
                        final_score = float( 
                            latest_result.get("overall_score", 0.0) or 0.0 
                        ) 

                        recommendation = latest_result.get( 
                            "recommendation", "N/A" 
                        ) or "N/A" 

                        overall_strengths = latest_result.get( 
                            "strengths", "" 
                        ) or "" 

                        overall_improvement = latest_result.get( 
                            "improvement", "" 
                        ) or "" 

                        # ==================================================== 
                        # GET CANDIDATE NAME 
                        # ==================================================== 
                        candidate_name = st.session_state.get( 
                            "voice_candidate_name", "" 
                        ) 

                        if not candidate_name: 
                            try: 
                                candidate_response = requests.get( 
                                    f"{API_URL}/candidates", 
                                    timeout=10 
                                ) 
                                if candidate_response.status_code == 200: 
                                    candidate_data = candidate_response.json() 
                                    candidate_list = ( 
                                        candidate_data.get("candidates", []) 
                                        if isinstance(candidate_data, dict) 
                                        else candidate_data 
                                    ) 
                                    if isinstance(candidate_list, list): 
                                        for candidate in candidate_list: 
                                            if ( 
                                                isinstance(candidate, dict) 
                                                and str(candidate.get("id")) 
                                                == str(candidate_id) 
                                            ): 
                                                candidate_name = candidate.get( 
                                                    "name", "" 
                                                ) 
                                                break 
                            except Exception: 
                                pass 

                        if not candidate_name: 
                            candidate_name = "N/A" 

                        # ==================================================== 
                        # GET JOB ID FROM DATABASE RESULT 
                        # ==================================================== 
                        job_id = st.session_state.get( 
                            "voice_job_id", "" 
                        ) 

                        if not job_id and interview_results: 
                            job_id = interview_results[0].get( 
                                "job_id", "N/A" 
                            ) 

                        if not job_id: 
                            job_id = "N/A" 

                        # ==================================================== 
                        # BUILD QUESTION-WISE DATA 
                        # ==================================================== 
                        questions = [ 
                            result.get("question", "") 
                            for result in interview_results 
                        ] 

                        answers = [ 
                            result.get("answer", "") 
                            for result in interview_results 
                        ] 

                        scores = [] 
                        for result in interview_results: 
                            try: 
                                scores.append( 
                                    float(result.get("score", 0) or 0) 
                                ) 
                            except (TypeError, ValueError): 
                                scores.append(0.0) 

                        evaluations = [ 
                            result.get("feedback", "") 
                            for result in interview_results 
                        ] 

                        # ==================================================== 
                        # CANDIDATE INFORMATION 
                        # ==================================================== 
                        st.subheader("👤 Candidate Information") 

                        info_col1, info_col2 = st.columns(2) 

                        with info_col1: 
                            st.write( 
                                "**Candidate:**", 
                                candidate_name 
                            ) 

                        with info_col2: 
                            st.write( 
                                "**Job ID:**", 
                                job_id 
                            ) 

                        st.divider() 

                        # ==================================================== 
                        # VOICE INTERVIEW PERFORMANCE 
                        # ==================================================== 
                        st.subheader("🎤 Voice Interview Performance") 

                        st.metric( 
                            "🎯 Final Voice Screening Score", 
                            f"{final_score:.1f}%" 
                        ) 

                        st.write( 
                            "**Recommendation:**", 
                            recommendation 
                        ) 

                        if overall_strengths: 
                            st.write( 
                                "**Strengths:**", 
                                overall_strengths 
                            ) 

                        if overall_improvement: 
                            st.write( 
                                "**Improvement:**", 
                                overall_improvement 
                            ) 

                        st.divider() 

                        # ==================================================== 
                        # OVERALL SCORE 
                        # ==================================================== 
                        st.subheader("🎯 Overall Interview Performance") 

                        score_col1, score_col2, score_col3 = st.columns(3) 

                        with score_col1: 
                            st.metric( 
                                "Overall Score", 
                                f"{final_score:.1f}%" 
                            ) 

                        with score_col2: 
                            st.metric( 
                                "Questions", 
                                len(questions) 
                            ) 

                        with score_col3: 
                            st.metric( 
                                "Answered", 
                                len(answers) 
                            ) 

                        st.progress( 
                            min(max(final_score / 100, 0.0), 1.0) 
                        ) 

                        st.caption( 
                            f"Your overall voice interview score is " 
                            f"{final_score:.1f}%" 
                        ) 

                        # ==================================================== 
                        # AI RECOMMENDATION 
                        # ==================================================== 
                        st.subheader("🤖 AI Recommendation") 

                        if recommendation: 
                            if "Strong" in recommendation: 
                                st.success(f"🌟 {recommendation}") 
                            elif "Suitable" in recommendation or "Hire" in recommendation: 
                                st.success(f"✅ {recommendation}") 
                            elif "Review" in recommendation: 
                                st.warning(f"⚠️ {recommendation}") 
                            else: 
                                st.info(f"Recommendation: {recommendation}") 
                        else: 
                            st.info("No recommendation available.") 

                        # ==================================================== 
                        # STRENGTHS 
                        # ==================================================== 
                        if overall_strengths: 
                            st.subheader("💪 Strengths") 
                            st.success(overall_strengths) 

                        # ==================================================== 
                        # IMPROVEMENT 
                        # ==================================================== 
                        if overall_improvement: 
                            st.subheader("📈 Areas for Improvement") 
                            st.warning(overall_improvement) 

                        # ==================================================== 
                        # QUESTION-WISE PERFORMANCE 
                        # ==================================================== 
                        st.subheader("📋 Question-wise Performance") 

                        if interview_results: 
                            for i, result in enumerate( 
                                interview_results, 
                                start=1 
                            ): 
                                question_text = result.get( 
                                    "question", "N/A" 
                                ) 
                                answer_text = result.get( 
                                    "answer", "N/A" 
                                ) 

                                try: 
                                    score_value = float( 
                                        result.get("score", 0) or 0 
                                    ) 
                                except (TypeError, ValueError): 
                                    score_value = 0.0 

                                feedback_text = result.get( 
                                    "feedback", "" 
                                ) 

                                with st.expander( 
                                    f"Question {i} — " 
                                    f"Score: {score_value:.1f}%" 
                                ): 
                                    st.markdown( 
                                        f"**Question:** {question_text}" 
                                    ) 
                                    st.markdown( 
                                        f"**Answer:** {answer_text}" 
                                    ) 
                                    st.markdown( 
                                        f"**Score:** {score_value:.1f}%" 
                                    ) 
                                    st.markdown( 
                                        "**🤖 AI Feedback:**" 
                                    ) 
                                    st.write(feedback_text) 
                        else: 
                            st.info( 
                                "No question-wise results available." 
                            ) 

                        # ==================================================== 
                        # PERFORMANCE SUMMARY 
                        # ==================================================== 
                        st.divider() 
                        st.subheader("📊 Performance Summary") 

                        if scores: 
                            average_score = sum(scores) / len(scores) 

                            summary_col1, summary_col2 = st.columns(2) 

                            with summary_col1: 
                                st.metric( 
                                    "Average Question Score", 
                                    f"{average_score:.1f}%" 
                                ) 

                            with summary_col2: 
                                st.metric( 
                                    "Completed Questions", 
                                    f"{len(answers)} / {len(questions)}" 
                                ) 
                        else: 
                            st.info("No question scores available.") 

                        st.divider() 
                        st.info( 
                            "💡 Complete another Voice-Based Screening " 
                            "interview to update your performance results." 
                        ) 

            except requests.exceptions.ConnectionError: 
                st.error( 
                    "❌ Backend is not running. " 
                    "Please start FastAPI first." 
                ) 

            except Exception as e: 
                st.error( 
                    f"Error loading interview performance: {e}" 
                ) 

    # ======================================================== 
    # 7. CONTACT RECRUITER 
    # ======================================================== 

    elif menu == "💬 Contact Recruiter": 

        st.subheader("💬 Contact Recruiter") 

        subject = st.text_input( 
            "Subject", 
            placeholder="Enter message subject" 
        ) 

        message = st.text_area( 
            "Message", 
            placeholder="Type your message to the recruiter..." 
        ) 

        if st.button( 
            "📨 Send Message", 
            use_container_width=True, 
            key="send_recruiter_message" 
        ): 

            if subject.strip() and message.strip(): 

                st.success( 
                    "✅ Message submitted successfully!" 
                ) 

                st.info( 
                    "Message storage/sending will be connected " 
                    "to the backend later." 
                ) 

            else: 

                st.warning( 
                    "⚠️ Please enter both subject and message." 
                ) 

    # ======================================================== 
    # LOGOUT 
    # ======================================================== 

    st.sidebar.divider() 

    if st.sidebar.button( 
        "🚪 Logout", 
        use_container_width=True, 
        key="candidate_logout" 
    ): 

        st.session_state.role = None 
        st.session_state.user_id = None 
        st.session_state.user_name = "" 
        st.session_state.user_email = "" 
        st.session_state.candidate_id = None 
        st.session_state.page = "landing" 

        st.rerun() 



# ============================================================ 
# SHOW LOGIN PAGE 
# ============================================================ 

if st.session_state.page == "login": 
    login_page() 
    st.stop() 
# ============================================================ 
# SHOW CHOOSE ROLE PAGE 
# ============================================================ 

if st.session_state.page == "choose_role": 
    choose_role_page() 
    st.stop() 
# ============================================================ 
# SHOW ADMIN DASHBOARD 
# ============================================================ 

if st.session_state.page == "admin": 
    if not st.session_state.get("user_id"): 
        st.session_state.page = "login" 
        st.rerun() 
    admin_page() 
    st.stop() 

# ============================================================ 
# SHOW CANDIDATE DASHBOARD 
# ============================================================ 

if st.session_state.page == "candidate_dashboard": 
    if st.session_state.role != "candidate": 
        st.session_state.page = "choose_role" 
        st.rerun()  
    candidate_dashboard() 
    st.stop() 

# ============================================================ 
# SHOW SIGN UP PAGE 
# ============================================================ 

if st.session_state.page == "signup": 
    signup_page() 
    st.stop() 

# ============================================================ 
# SHOW LANDING PAGE 
# ============================================================ 

if st.session_state.page == "landing": 
    landing_page() 
    st.stop() 
# ============================================================ 
# RECRUITER ROLE ACCESS 
# ============================================================ 

if st.session_state.page == "dashboard": 

    if st.session_state.role != "recruiter": 
        st.session_state.page = "choose_role" 
        st.rerun() 
# ---------------------------------------------------- 
# TITLE 
# ---------------------------------------------------- 

st.title("🤖 AI Recruitment & Talent Management Copilot") 

st.write( 
    "AI-powered recruitment system for resume parsing, " 
    "candidate matching, ranking and hiring decisions." 
) 



# ---------------------------------------------------- 
# Sidebar Navigation 
# ---------------------------------------------------- 

selected_feature = st.sidebar.selectbox(
    "Select Feature",
    [
        "Dashboard",
        "Upload Resume",
        "Upload Job Description",
        "Job Dashboard",
        "Candidates",
        "Resume-JD Matching",
        "Candidate Ranking",
        "AI Resume Summary",
        "Screening & Performance",
        "AI Hiring Recommendation",
        "AI Email Generator",
        "Recruiter Analytics",
    ],
    key="recruiter_feature_menu",
)
# ============================================================
# SELECTED FEATURE HEADER
# ============================================================

st.markdown(
    f"### 📌 {selected_feature}",
    unsafe_allow_html=True
)

# ============================================================
# LOGOUT
# ============================================================

st.sidebar.write("") 

if st.sidebar.button("🚪 Logout", use_container_width=True): 
    st.session_state.role = None 
    st.session_state.user_id = None 
    st.session_state.user_name = "" 
    st.session_state.user_email = "" 
    st.session_state.candidate_id = None 
    st.session_state.page = "landing" 
    st.rerun() 

# ============================================================ 
# DASHBOARD 
# ============================================================ 

if selected_feature == "Dashboard": 

    st.title("📊 Recruiter Dashboard") 

    st.write( 
        "Overview of recruitment activities and candidate statistics." 
    ) 

    # ======================================================== 
    # GET CANDIDATES FROM FASTAPI 
    # ======================================================== 

    try: 

        response = requests.get( 
            f"{API_URL}/candidates" 
        ) 

        if response.status_code == 200: 

            data = response.json() 

            # Handle API response 
            if isinstance(data, dict) and "candidates" in data: 
                candidates = data["candidates"] 
            else: 
                candidates = data 

            if not isinstance(candidates, list): 
                candidates = [] 

            # ================================================= 
            # VALID CANDIDATES 
            # ================================================= 

            valid_candidates = [ 
                c for c in candidates 
                if isinstance(c, dict) 
            ] 

            # ================================================= 
            # BASIC COUNTS 
            # ================================================= 

            total_candidates = len(valid_candidates) 

            shortlisted = sum( 
                1 
                for c in valid_candidates 
                if str(c.get("status", "")).lower() 
                == "shortlisted" 
            ) 

            rejected = sum( 
                1 
                for c in valid_candidates 
                if str(c.get("status", "")).lower() 
                == "rejected" 
            ) 

            under_review = sum( 
                1 
                for c in valid_candidates 
                if str(c.get("status", "")).lower() 
                in [ 
                    "review", 
                    "under review", 
                    "pending" 
                ] 
            ) 

            # ================================================= 
            # SELECTED CANDIDATES 
            # ================================================= 

            selected_candidates = sum( 
                1 
                for c in valid_candidates 
                if str(c.get("status", "")).lower() 
                in [ 
                    "selected", 
                    "hired" 
                ] 
            ) 

            # ================================================= 
            # INTERVIEWS SCHEDULED 
            # 
            # Currently calculated from candidate status. 
            # Candidates with Interview status are counted. 
            # ================================================= 

            interviews_scheduled = sum( 
                1 
                for c in valid_candidates 
                if str(c.get("status", "")).lower() 
                in [ 
                    "interview", 
                    "interview scheduled" 
                ] 
            ) 

            # ================================================= 
            # GET TOTAL JOB OPENINGS 
            # ================================================= 

            total_jobs = 0 

            try: 

                jobs_response = requests.get( 
                    f"{API_URL}/jobs" 
                ) 

                if jobs_response.status_code == 200: 

                    jobs_data = jobs_response.json() 

                    if isinstance(jobs_data, dict): 

                        total_jobs = jobs_data.get( 
                            "total_jobs", 
                            0 
                        ) 

            except Exception: 

                total_jobs = 0 

            # ================================================= 
            # DATAFRAME 
            # ================================================= 

            if valid_candidates: 

                df = pd.DataFrame( 
                    valid_candidates 
                ) 

            else: 

                df = pd.DataFrame() 

            # ================================================= 
            # AVERAGE HIRING SCORE 
            # ================================================= 

            average_hiring_score = 0 

            if ( 
                not df.empty 
                and "hiring_score" in df.columns 
            ): 

                hiring_scores = pd.to_numeric( 
                    df["hiring_score"], 
                    errors="coerce" 
                ).dropna() 

                if not hiring_scores.empty: 

                    average_hiring_score = ( 
                        hiring_scores.mean() 
                    ) 

            # ================================================= 
            # DASHBOARD KPI ROW 1 
            # ================================================= 

            col1, col2, col3, col4 = st.columns(4) 

            with col1: 

                st.metric( 
                    "👥 Total Candidates", 
                    total_candidates 
                ) 

            with col2: 

                st.metric( 
                    "💼 Total Job Openings", 
                    total_jobs 
                ) 

            with col3: 

                st.metric( 
                    "✅ Shortlisted", 
                    shortlisted 
                ) 

            with col4: 

                st.metric( 
                    "❌ Rejected", 
                    rejected 
                ) 

            # ================================================= 
            # DASHBOARD KPI ROW 2 
            # ================================================= 

            col5, col6, col7, col8 = st.columns(4) 

            with col5: 

                st.metric( 
                    "⏳ Under Review", 
                    under_review 
                ) 

            with col6: 

                st.metric( 
                    "🎤 Interviews Scheduled", 
                    interviews_scheduled 
                ) 

            with col7: 

                st.metric( 
                    "🏆 Selected Candidates", 
                    selected_candidates 
                ) 

            with col8: 

                if average_hiring_score > 0: 

                    st.metric( 
                        "📈 Average Hiring Score", 
                        f"{average_hiring_score:.1f}%" 
                    ) 

                else: 

                    st.metric( 
                        "📈 Average Hiring Score", 
                        "N/A" 
                    ) 

            st.divider() 

            # ================================================= 
            # CANDIDATE PIPELINE 
            # ================================================= 

            st.subheader( 
                "🔄 Candidate Pipeline" 
            ) 

            pipeline_data = pd.DataFrame( 
                { 
                    "Stage": [ 
                        "Under Review", 
                        "Shortlisted", 
                        "Interview", 
                        "Selected / Hired", 
                        "Rejected" 
                    ], 
                    "Candidates": [ 
                        under_review, 
                        shortlisted, 
                        interviews_scheduled, 
                        selected_candidates, 
                        rejected 
                    ] 
                } 
            ) 

            st.bar_chart( 
                pipeline_data, 
                x="Stage", 
                y="Candidates" 
            ) 

            st.divider() 

            # ================================================= 
            # CANDIDATE OVERVIEW 
            # ================================================= 

            st.subheader( 
                "👥 Candidate Overview" 
            ) 

            if not df.empty: 

                st.dataframe( 
                    df, 
                    use_container_width=True, 
                    hide_index=True 
                ) 

                # ================================================= 
                # RECRUITMENT ANALYTICS 
                # ================================================= 

                st.divider() 

                st.subheader( 
                    "📊 Recruitment Analytics" 
                ) 

                # ================================================= 
                # 1. CANDIDATE STATUS DISTRIBUTION 
                # ================================================= 

                st.write( 
                    "### 👥 Candidate Status Distribution" 
                ) 

                if "status" in df.columns: 

                    status_counts = ( 
                        df["status"] 
                        .fillna("Unknown") 
                        .astype(str) 
                        .str.title() 
                        .value_counts() 
                        .reset_index() 
                    ) 

                    status_counts.columns = [ 
                        "Status", 
                        "Candidates" 
                    ] 

                    st.bar_chart( 
                        status_counts, 
                        x="Status", 
                        y="Candidates" 
                    ) 

                else: 

                    st.info( 
                        "Status information is not available." 
                    ) 

                # ================================================= 
                # 2. MATCH SCORE ANALYTICS 
                # ================================================= 

                st.write( 
                    "### 🎯 Match Score Analytics" 
                ) 

                if "match_score" in df.columns: 

                    df["match_score"] = pd.to_numeric( 
                        df["match_score"], 
                        errors="coerce" 
                    ) 

                    average_match = ( 
                        df["match_score"].mean() 
                    ) 

                    if pd.notna(average_match): 

                        st.metric( 
                            "Average Match Score", 
                            f"{average_match:.1f}%" 
                        ) 

                        match_data = ( 
                            df[ 
                                [ 
                                    "name", 
                                    "match_score" 
                                ] 
                            ] 
                            .dropna() 
                            .copy() 
                        ) 

                        if not match_data.empty: 

                            match_data["Candidate"] = ( 
                                match_data["name"] 
                                .astype(str) 
                            ) 

                            st.bar_chart( 
                                match_data, 
                                x="Candidate", 
                                y="match_score" 
                            ) 

                    else: 

                        st.info( 
                            "No match score data available." 
                        ) 

                else: 

                    st.info( 
                        "Match score information is not available." 
                    ) 

                # ================================================= 
                # 3. ATS SCORE ANALYTICS 
                # ================================================= 

                st.write( 
                    "### 📈 ATS Score Analytics" 
                ) 

                if "ats_score" in df.columns: 

                    df["ats_score"] = pd.to_numeric( 
                        df["ats_score"], 
                        errors="coerce" 
                    ) 

                    average_ats = ( 
                        df["ats_score"].mean() 
                    ) 

                    if pd.notna(average_ats): 

                        st.metric( 
                            "Average ATS Score", 
                            f"{average_ats:.1f}%" 
                        ) 

                        ats_data = ( 
                            df[ 
                                [ 
                                    "name", 
                                    "ats_score" 
                                ] 
                            ] 
                            .dropna() 
                            .copy() 
                        ) 

                        if not ats_data.empty: 

                            ats_data["Candidate"] = ( 
                                ats_data["name"] 
                                .astype(str) 
                            ) 

                            st.bar_chart( 
                                ats_data, 
                                x="Candidate", 
                                y="ats_score" 
                            ) 

                    else: 

                        st.info( 
                            "No ATS score data available." 
                        ) 

                else: 

                    st.info( 
                        "ATS score information is not available." 
                    ) 

                # ================================================= 
                # 4. HIRING SCORE ANALYTICS 
                # ================================================= 

                st.write( 
                    "### 🏆 Hiring Score Analytics" 
                ) 

                if "hiring_score" in df.columns: 

                    hiring_data = pd.to_numeric( 
                        df["hiring_score"], 
                        errors="coerce" 
                    ) 

                    valid_hiring = hiring_data.dropna() 

                    if not valid_hiring.empty: 

                        hiring_chart = pd.DataFrame( 
                            { 
                                "Candidate": df.loc[ 
                                    valid_hiring.index, 
                                    "name" 
                                ].astype(str), 
                                "Hiring Score": valid_hiring 
                            } 
                        ) 

                        st.bar_chart( 
                            hiring_chart, 
                            x="Candidate", 
                            y="Hiring Score" 
                        ) 

                    else: 

                        st.info( 
                            "No hiring score data available." 
                        ) 

                else: 

                    st.info( 
                        "Hiring score information is not available." 
                    ) 

                # ================================================= 
                # 5. RECRUITMENT SUMMARY 
                # ================================================= 

                st.write( 
                    "### 📋 Recruitment Summary" 
                ) 

                summary_col1, summary_col2, summary_col3 = ( 
                    st.columns(3) 
                ) 

                with summary_col1: 

                    st.metric( 
                        "Total Candidates", 
                        total_candidates 
                    ) 

                with summary_col2: 

                    st.metric( 
                        "Shortlisted", 
                        shortlisted 
                    ) 

                with summary_col3: 

                    st.metric( 
                        "Rejected", 
                        rejected 
                    ) 

            else: 

                st.info( 
                    "No candidates available." 
                ) 

        else: 

            st.error( 
                f"Unable to retrieve candidates. " 
                f"Status code: {response.status_code}" 
            ) 

    except Exception as e: 

        st.error( 
            f"Backend connection error: {e}" 
        ) 
# ============================================================ 
# CANDIDATE MANAGEMENT 
# ============================================================ 

if selected_feature == "Candidates": 

    st.title("👥 Candidate Management") 

    st.write( 
        "Search, view and manage candidate profiles." 
    ) 

    # -------------------------------------------------------- 
    # GET CANDIDATES FROM FASTAPI 
    # -------------------------------------------------------- 

    try: 

        response = requests.get( 
            f"{API_URL}/candidates" 
        ) 

        if response.status_code == 200: 

            data = response.json() 

            # Handle API response 
            if isinstance(data, dict) and "candidates" in data: 
                candidates = data["candidates"] 
            else: 
                candidates = data 

            # Make sure candidates is a list 
            if not isinstance(candidates, list): 
                candidates = [] 

            # ------------------------------------------------ 
            # VALID CANDIDATES 
            # ------------------------------------------------ 

            valid_candidates = [ 
                c for c in candidates 
                if isinstance(c, dict) 
            ] 

            if valid_candidates: 

                # Convert to DataFrame 
                df = pd.DataFrame(valid_candidates) 

                # ------------------------------------------------ 
                # SEARCH CANDIDATE 
                # ------------------------------------------------ 

                st.subheader("🔍 Search Candidate") 

                search_text = st.text_input( 
                    "Search by candidate name or email", 
                    placeholder="Enter candidate name or email..." 
                ) 

                filtered_df = df.copy() 

                if search_text: 

                    search_text = search_text.lower() 

                    # Make sure required columns exist 
                    if "name" not in filtered_df.columns: 
                        filtered_df["name"] = "" 

                    if "email" not in filtered_df.columns: 
                        filtered_df["email"] = "" 

                    filtered_df = filtered_df[ 
                        filtered_df["name"] 
                        .astype(str) 
                        .str.lower() 
                        .str.contains( 
                            search_text, 
                            na=False 
                        ) 
                        | 
                        filtered_df["email"] 
                        .astype(str) 
                        .str.lower() 
                        .str.contains( 
                            search_text, 
                            na=False 
                        ) 
                    ] 

                # ------------------------------------------------ 
                # CANDIDATE COUNT 
                # ------------------------------------------------ 

                st.write( 
                    f"**Candidates Found: {len(filtered_df)}**" 
                ) 

                # ------------------------------------------------ 
                # DISPLAY CANDIDATE TABLE 
                # ------------------------------------------------ 

                if not filtered_df.empty: 

                    display_columns = [] 

                    for column in [ 
                        "id", 
                        "name", 
                        "email", 
                        "phone", 
                        "status", 
                        "match_score", 
                        "ats_score" 
                    ]: 

                        if column in filtered_df.columns: 
                            display_columns.append(column) 

                    if display_columns: 

                        st.dataframe( 
                            filtered_df[display_columns], 
                            use_container_width=True, 
                            hide_index=True 
                        ) 

                else: 

                    st.info( 
                        "No candidates match your search." 
                    ) 

                # ------------------------------------------------ 
                # SELECT CANDIDATE 
                # ------------------------------------------------ 

                st.divider() 

                st.subheader("👤 Candidate Profile") 

                candidate_names = ( 
                    filtered_df["name"] 
                    .astype(str) 
                    .tolist() 
                    if ( 
                        not filtered_df.empty 
                        and "name" in filtered_df.columns 
                    ) 
                    else [] 
                ) 

                if candidate_names: 

                    selected_candidate = st.selectbox( 
                        "Select Candidate", 
                        candidate_names 
                    ) 

                    # Get selected candidate 
                    candidate_rows = filtered_df[ 
                        filtered_df["name"] 
                        .astype(str) 
                        == selected_candidate 
                    ] 

                    if not candidate_rows.empty: 

                        candidate_row = candidate_rows.iloc[0] 

                        # ------------------------------------------------ 
                        # BASIC INFORMATION 
                        # ------------------------------------------------ 

                        st.write("### 📄 Candidate Information") 

                        col1, col2 = st.columns(2) 

                        with col1: 

                            st.write( 
                                f"**Name:** " 
                                f"{candidate_row.get('name', 'N/A')}" 
                            ) 

                            st.write( 
                                f"**Email:** " 
                                f"{candidate_row.get('email', 'N/A')}" 
                            ) 

                            st.write( 
                                f"**Phone:** " 
                                f"{candidate_row.get('phone', 'N/A')}" 
                            ) 

                        with col2: 

                            st.write( 
                                f"**Match Score:** " 
                                f"{candidate_row.get('match_score', 'N/A')}" 
                            ) 

                            st.write( 
                                f"**ATS Score:** " 
                                f"{candidate_row.get('ats_score', 'N/A')}" 
                            ) 

                            st.write( 
                                f"**Status:** " 
                                f"{candidate_row.get('status', 'N/A')}" 
                            ) 

                        # ------------------------------------------------ 
                        # SKILLS 
                        # ------------------------------------------------ 

                        st.divider() 

                        st.write("### 🛠️ Skills") 

                        skills = candidate_row.get( 
                            "skills", 
                            "Not available" 
                        ) 

                        # Display list properly 
                        if isinstance(skills, list): 

                            if skills: 

                                for skill in skills: 
                                    st.write(f"• {skill}") 

                            else: 

                                st.write("Not available") 

                        else: 

                            st.write(str(skills)) 

                        # ------------------------------------------------ 
                        # EDUCATION 
                        # ------------------------------------------------ 

                        st.write("### 🎓 Education") 

                        education = candidate_row.get( 
                            "education", 
                            "Not available" 
                        ) 

                        if isinstance(education, list): 

                            if education: 

                                for edu in education: 
                                    st.write(f"• {edu}") 

                            else: 

                                st.write("Not available") 

                        else: 

                            st.write(str(education)) 

                        # ------------------------------------------------ 
                        # EXPERIENCE 
                        # ------------------------------------------------ 

                        st.write("### 💼 Experience") 

                        experience = candidate_row.get( 
                            "experience", 
                            "Not available" 
                        ) 

                        if isinstance(experience, list): 

                            if experience: 

                                for exp in experience: 
                                    st.write(f"• {exp}") 

                            else: 

                                st.write("Not available") 

                        else: 

                            st.write(str(experience)) 

                        # ------------------------------------------------ 
                        # UPDATE STATUS 
                        # ------------------------------------------------ 

                        st.divider() 

                        st.write("### 🔄 Update Candidate Status") 

                        current_status = str( 
                            candidate_row.get( 
                                "status", 
                                "Under Review" 
                            ) 
                        ) 

                        status_options = [ 
                            "Under Review", 
                            "Shortlisted", 
                            "Interview", 
                            "Hired", 
                            "Selected", 
                            "Rejected" 
                        ] 

                        # Find current status 
                        current_index = 0 

                        for i, status in enumerate( 
                            status_options 
                        ): 

                            if ( 
                                status.lower() 
                                == current_status.lower() 
                            ): 

                                current_index = i 
                                break 

                        new_status = st.selectbox( 
                            "Select New Status", 
                            status_options, 
                            index=current_index 
                        ) 

                        # ------------------------------------------------ 
                        # UPDATE BUTTON 
                        # ------------------------------------------------ 

                        if st.button( 
                            "💾 Update Status" 
                        ): 

                            candidate_id = candidate_row.get( 
                                "id" 
                            ) 

                            if candidate_id is not None: 

                                update_response = requests.put( 
                                    f"{API_URL}/candidate/{candidate_id}/status", 
                                    params={ 
                                        "status": new_status 
                                    } 
                                ) 

                                if update_response.status_code == 200: 

                                    st.success( 
                                        "Candidate status updated successfully!" 
                                    ) 

                                    st.rerun() 

                                else: 

                                    st.error( 
                                        "Failed to update candidate status." 
                                    ) 

                            else: 

                                st.error( 
                                    "Candidate ID not found." 
                                ) 

                else: 

                    st.info( 
                        "No candidate profiles available." 
                    ) 

            else: 

                st.info( 
                    "No candidates available." 
                ) 

        else: 

            st.error( 
                f"Unable to retrieve candidates. " 
                f"Status code: {response.status_code}" 
            ) 

    except Exception as e: 

        st.error( 
            f"Backend connection error: {e}" 
        ) 

# ============================================================ 
# RECRUITMENT ANALYTICS 
# ============================================================ 

if selected_feature == "Recruitment Analytics": 

    st.title("📊 Recruitment Analytics") 

    st.write( 
        "Analyze candidate recruitment data and hiring performance." 
    ) 

    # -------------------------------------------------------- 
    # GET CANDIDATES 
    # -------------------------------------------------------- 

    try: 

        response = requests.get( 
            f"{API_URL}/candidates" 
        ) 

        if response.status_code == 200: 

            data = response.json() 

            if isinstance(data, dict) and "candidates" in data: 
                candidates = data["candidates"] 
            else: 
                candidates = data 

            if not isinstance(candidates, list): 
                candidates = [] 

            valid_candidates = [ 
                c for c in candidates 
                if isinstance(c, dict) 
            ] 

            if valid_candidates: 

                df = pd.DataFrame(valid_candidates) 

                # ------------------------------------------------ 
                # TOTAL CANDIDATES 
                # ------------------------------------------------ 

                st.subheader("📈 Overview") 

                st.metric( 
                    "Total Candidates", 
                    len(df) 
                ) 

                # ------------------------------------------------ 
                # CANDIDATE DISTRIBUTION BY STATUS 
                # ------------------------------------------------ 

                st.subheader("👥 Candidate Distribution by Status") 

                if "status" in df.columns: 

                    status_counts = ( 
                        df["status"] 
                        .fillna("Unknown") 
                        .astype(str) 
                        .value_counts() 
                    ) 

                    st.bar_chart(status_counts) 

                else: 

                    st.info("Status data is not available.") 

                # ------------------------------------------------ 
                # HIRING SCORE DISTRIBUTION 
                # ------------------------------------------------ 

                st.subheader("🎯 Hiring Score Distribution") 

                if "hiring_score" in df.columns: 

                    hiring_scores = pd.to_numeric( 
                        df["hiring_score"], 
                        errors="coerce" 
                    ).dropna() 

                    if not hiring_scores.empty: 
                        st.bar_chart( 
                            hiring_scores.value_counts() 
                            .sort_index() 
                        ) 
                    else: 
                        st.info( 
                            "Hiring score data is not available." 
                        ) 

                else: 

                    st.info( 
                        "Hiring score column is not available." 
                    ) 

                # ------------------------------------------------ 
                # SKILL MATCH DISTRIBUTION 
                # ------------------------------------------------ 

                st.subheader("🛠️ Skill Match Distribution") 

                if "match_score" in df.columns: 

                    match_scores = pd.to_numeric( 
                        df["match_score"], 
                        errors="coerce" 
                    ).dropna() 

                    if not match_scores.empty: 

                        st.bar_chart( 
                            match_scores 
                            .value_counts() 
                            .sort_index() 
                        ) 

                    else: 

                        st.info( 
                            "Match score data is not available." 
                        ) 

                else: 

                    st.info( 
                        "Match score column is not available." 
                    ) 

                # ------------------------------------------------ 
                # CANDIDATES BY JOB ROLE 
                # ------------------------------------------------ 

                st.subheader("💼 Candidates by Job Role") 

                if "job_title" in df.columns: 

                    job_counts = ( 
                        df["job_title"] 
                        .fillna("Unknown") 
                        .astype(str) 
                        .value_counts() 
                    ) 

                    st.bar_chart(job_counts) 

                else: 

                    st.info( 
                        "Job role data is not available." 
                    ) 

                # ------------------------------------------------ 
                # INTERVIEW PERFORMANCE 
                # ------------------------------------------------ 

                st.subheader("🎤 Interview Performance") 

                if "interview_score" in df.columns: 

                    interview_scores = pd.to_numeric( 
                        df["interview_score"], 
                        errors="coerce" 
                    ).dropna() 

                    if not interview_scores.empty: 

                        st.bar_chart( 
                            interview_scores 
                            .value_counts() 
                            .sort_index() 
                        ) 

                    else: 

                        st.info( 
                            "Interview score data is not available." 
                        ) 

                else: 

                    st.info( 
                        "Interview performance data is not available yet." 
                    ) 

                # ------------------------------------------------ 
                # SELECTED VS REJECTED 
                # ------------------------------------------------ 

                st.subheader("✅ Selected vs. Rejected Candidates") 

                if "status" in df.columns: 

                    selected_count = ( 
                        df["status"] 
                        .astype(str) 
                        .str.lower() 
                        .isin(["selected", "hired"]) 
                        .sum() 
                    ) 

                    rejected_count = ( 
                        df["status"] 
                        .astype(str) 
                        .str.lower() 
                        .eq("rejected") 
                        .sum() 
                    ) 

                    comparison_df = pd.DataFrame( 
                        { 
                            "Status": [ 
                                "Selected / Hired", 
                                "Rejected" 
                            ], 
                            "Candidates": [ 
                                selected_count, 
                                rejected_count 
                            ] 
                        } 
                    ) 

                    st.bar_chart( 
                        comparison_df.set_index("Status") 
                    ) 

                else: 

                    st.info( 
                        "Candidate status data is not available." 
                    ) 

            else: 

                st.info( 
                    "No candidate data available for analytics." 
                ) 

        else: 

            st.error( 
                f"Unable to retrieve candidates. " 
                f"Status code: {response.status_code}" 
            ) 

    except Exception as e: 

        st.error( 
            f"Backend connection error: {e}" 
        ) 
# ============================================================ 
# UPLOAD RESUME 
# ============================================================ 
# ============================================================ 
# UPLOAD RESUME 
# ============================================================ 

if selected_feature == "Upload Resume": 

    st.title("📄 Upload Resume") 

    st.write( 
        "Upload a candidate resume in PDF or DOCX format." 
    ) 

    uploaded_file = st.file_uploader( 
        "Choose a Resume", 
        type=["pdf", "docx"] 
    ) 

    if uploaded_file is not None: 

        st.success( 
            f"Selected file: {uploaded_file.name}" 
        ) 

        if st.button("Upload Resume"): 

            try: 

                files = { 
                    "file": ( 
                        uploaded_file.name, 
                        uploaded_file.getvalue(), 
                        uploaded_file.type 
                    ) 
                } 

                response = requests.post( 
                    f"{API_URL}/upload-resume", 
                    files=files 
                ) 

                if response.status_code == 200: 

                    st.success( 
                        "✅ Resume uploaded successfully!" 
                    ) 

                    st.json( 
                        response.json() 
                    ) 

                else: 

                    st.error( 
                        f"❌ Resume upload failed. " 
                        f"Status code: {response.status_code}" 
                    ) 

                    st.write( 
                        response.text 
                    ) 

            except Exception as e: 

                st.error( 
                    f"Backend connection error: {e}" 
                ) 

# ==================================================== 
# Upload Job Description 
# ==================================================== 

elif selected_feature == "Upload Job Description": 



    st.header( 
        "📌 Upload Job Description" 
    ) 



    jd = st.file_uploader( 
        "Upload JD", 
        type=["pdf", "docx"] 
    ) 



    if st.button( 
        "Upload Job Description" 
    ): 



        if jd is None: 

            st.warning( 
                "Please upload a Job Description." 
            ) 



        else: 



            files = { 

                "file": 
                ( 
                    jd.name, 
                    jd, 
                    jd.type 
                ) 

            } 



            response = requests.post( 
                f"{API_URL}/upload-jd", 
                files=files 
            ) 



            if response.status_code == 200: 



                data = response.json() 

                job = data["job_description"] 



                st.success( 
                    data["message"] 
                ) 



                st.subheader( 
                    "📋 Job Details" 
                ) 



                st.write( 
                    "### Job Title" 
                ) 
                st.write( 
                    job.get("job_title") 
                ) 



                st.write( 
                    "### Company" 
                ) 
                st.write( 
                    job.get("company_name") 
                ) 



                st.write( 
                    "### Location" 
                ) 
                st.write( 
                    job.get("location") 
                ) 



                st.write( 
                    "### Salary" 
                ) 
                st.write( 
                    job.get("salary") 
                ) 



                st.write( 
                    "### Employment Type" 
                ) 
                st.write( 
                    job.get("employment_type") 
                ) 



                st.write( 
                    "### Experience" 
                ) 
                st.write( 
                    job.get("experience") 
                ) 



                st.write( 
                    "### Education" 
                ) 
                st.write( 
                    job.get("education") 
                ) 



                st.write( 
                    "### Skills" 
                ) 

                for skill in job.get("skills", []): 

                    st.write( 
                        "•", 
                        skill 
                    ) 



                st.write( 
                    "### Responsibilities" 
                ) 

                for item in job.get("responsibilities", []): 

                    st.write( 
                        "•", 
                        item 
                    ) 



            else: 

                st.error( 
                    "JD upload failed." 
                ) 
# ==================================================== 
# Job Description Dashboard 
# ==================================================== 

elif selected_feature == "Job Dashboard": 

    st.header("📂 Job Description Dashboard") 



    # ----------------------------- 
    # View All Jobs 
    # ----------------------------- 

    st.subheader("📋 All Job Descriptions") 



    response = requests.get( 
        f"{API_URL}/jobs" 
    ) 



    if response.status_code == 200: 

        data = response.json() 

        jobs = data.get("jobs", []) 



        if len(jobs) == 0: 

            st.info( 
                "No job descriptions found." 
            ) 

        else: 

            table = [] 



            for job in jobs: 

                table.append( 
                    { 
                        "ID": job["id"], 
                        "Job Title": job["job_title"], 
                        "Company": job["company_name"], 
                        "Location": job["location"], 
                        "Experience": job["experience"] 
                    } 
                ) 



            st.dataframe( 
                pd.DataFrame(table), 
                use_container_width=True 
            ) 



    st.markdown("---") 



    # ----------------------------- 
    # Search Job 
    # ----------------------------- 

    st.subheader("🔍 Search Job") 



    job_id = st.number_input( 
        "Enter Job ID", 
        min_value=1, 
        step=1, 
        key="search_job" 
    ) 



    if st.button( 
        "Get Job Details" 
    ): 



        response = requests.get( 
            f"{API_URL}/jobs/{job_id}" 
        ) 



        if response.status_code == 200: 

            st.json( 
                response.json() 
            ) 

        else: 

            st.error( 
                "Job not found." 
            ) 



    st.markdown("---") 



    # ----------------------------- 
    # Update Job 
    # ----------------------------- 

    st.subheader("✏ Update Job") 



    update_id = st.number_input( 
        "Job ID", 
        min_value=1, 
        step=1, 
        key="update_id" 
    ) 



    job_title = st.text_input( 
        "Job Title" 
    ) 



    company = st.text_input( 
        "Company" 
    ) 



    location = st.text_input( 
        "Location" 
    ) 



    salary = st.text_input( 
        "Salary" 
    ) 



    experience = st.text_input( 
        "Experience" 
    ) 



    description = st.text_area( 
        "Job Description" 
    ) 



    if st.button( 
        "Update Job" 
    ): 



        updated_job = { 

            "job_title": job_title, 
            "company_name": company, 
            "location": location, 
            "salary": salary, 
            "experience": experience, 
            "job_description": description 

        } 



        response = requests.put( 
            f"{API_URL}/jobs/{update_id}", 
            json=updated_job 
        ) 



        if response.status_code == 200: 

            st.success( 
                "Job updated successfully." 
            ) 

        else: 

            st.error( 
                "Update failed." 
            ) 



    st.markdown("---") 



    # ----------------------------- 
    # Delete Job 
    # ----------------------------- 

    st.subheader("🗑 Delete Job") 



    delete_id = st.number_input( 
        "Delete Job ID", 
        min_value=1, 
        step=1, 
        key="delete_id" 
    ) 



    if st.button( 
        "Delete Job" 
    ): 



        response = requests.delete( 
            f"{API_URL}/jobs/{delete_id}" 
        ) 



        if response.status_code == 200: 

            st.success( 
                response.json()["message"] 
            ) 

        else: 

            st.error( 
                "Delete failed." 
            ) 





# ==================================================== 
# Candidate Dashboard 
# ==================================================== 

elif selected_feature == "__legacy_candidates_block__": 



    st.header( 
        "👥 Recruiter Candidate Dashboard" 
    ) 



    response = requests.get( 
        f"{API_URL}/candidates" 
    ) 



    if response.status_code == 200: 



        data = response.json() 



        candidates = data["candidates"] 



        st.metric( 
            "Total Candidates", 
            data["total_candidates"] 
        ) 



        if len(candidates)==0: 

            st.info( 
                "No candidates available." 
            ) 



        else: 



            search = st.text_input( 
                "Search Candidate" 
            ) 



            if search: 

                candidates = [ 

                    c for c in candidates 

                    if search.lower() 
                    in c["name"].lower() 

                ] 





            table=[] 



            for c in candidates: 



                table.append( 
                    { 
                        "ID":c["id"], 
                        "Name":c["name"], 
                        "Email":c["email"] 
                    } 
                ) 



            st.dataframe( 
                pd.DataFrame(table), 
                use_container_width=True 
            ) 





            selected = st.selectbox( 
                "Select Candidate", 
                candidates, 
                format_func=lambda x:x["name"], 
                key="candidate_management_select" 
            ) 





            st.subheader( 
                "Candidate Details" 
            ) 



            st.write( 
                "Name:", 
                selected["name"] 
            ) 



            st.write( 
                "Email:", 
                selected["email"] 
            ) 



            st.write( 
                "Skills:", 
                selected.get("skills", "N/A") 
            ) 



            st.write( 
                "Education:", 
                selected.get("education", "N/A") 
            ) 



            st.write( 
                "Experience:", 
                selected.get("experience", "N/A") 
            ) 



    else: 

        st.error( 
            "Unable to fetch candidates." 
        ) 
# ============================================================
# RESUME - JOB DESCRIPTION MATCHING
# ============================================================

elif selected_feature == "Resume-JD Matching":

    st.header("🎯 Resume - Job Description Matching")

    st.write(
        "Compare a candidate's resume with a selected job description "
        "to identify matched skills, missing skills, extra skills, "
        "ATS score, compatibility score and hiring recommendation."
    )

    st.divider()

    # ============================================================
    # UPLOAD RESUME
    # ============================================================

    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Upload Candidate Resume",
        type=["pdf", "docx"],
        key="resume_jd_matching_resume"
    )

    # ============================================================
    # ENTER JOB ID
    # ============================================================

    st.subheader("💼 Job Information")

    job_id = st.number_input(
        "Enter Job ID",
        min_value=1,
        step=1,
        value=1,
        key="resume_jd_matching_job_id"
    )

    st.caption(
        "Enter the Job ID of the job description against which "
        "the resume should be matched."
    )

    st.divider()

    # ============================================================
    # MATCH BUTTON
    # ============================================================

    if st.button(
        "🔍 Match Resume with Job Description",
        type="primary",
        use_container_width=True,
        key="resume_jd_match_button"
    ):

        # --------------------------------------------------------
        # VALIDATE RESUME
        # --------------------------------------------------------

        if resume_file is None:

            st.warning(
                "⚠️ Please upload a resume before starting the matching."
            )

        else:

            # ----------------------------------------------------
            # PREPARE FILE
            # ----------------------------------------------------

            try:

                file_bytes = resume_file.getvalue()

                files = {
                    "resume": (
                        resume_file.name,
                        file_bytes,
                        resume_file.type
                    )
                }

                # ------------------------------------------------
                # CALL MATCH API
                # ------------------------------------------------

                with st.spinner(
                    "🤖 AI is analyzing the resume against the "
                    "job description..."
                ):

                    response = requests.post(
                        f"{API_URL}/match",
                        files=files,
                        data={
                            "job_id": int(job_id)
                        },
                        timeout=60
                    )

                # =================================================
                # SUCCESS
                # =================================================

                if response.status_code == 200:

                    # ------------------------------------------------
                    # GET RESULT
                    # ------------------------------------------------

                    result = response.json()

                    st.success(
                        "✅ Resume and Job Description matching completed!"
                    )

                    # =================================================
                    # BASIC INFORMATION
                    # =================================================

                    st.subheader(
                        "👤 Candidate & Job Information"
                    )

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:

                        st.info(
                            f"👤 **Candidate Name:** "
                            f"{result.get('candidate_name', 'N/A')}"
                        )

                    with info_col2:

                        st.info(
                            f"💼 **Job Title:** "
                            f"{result.get('job_title', 'N/A')}"
                        )

                    # =================================================
                    # GET SKILLS
                    # =================================================

                    matched_skills = result.get(
                        "matched_skills",
                        []
                    )

                    missing_skills = result.get(
                        "missing_skills",
                        []
                    )

                    extra_skills = result.get(
                        "extra_skills",
                        []
                    )

                    # ------------------------------------------------
                    # SAFETY: MAKE SURE LISTS ARE ACTUALLY LISTS
                    # ------------------------------------------------

                    if not isinstance(
                        matched_skills,
                        list
                    ):
                        matched_skills = []

                    if not isinstance(
                        missing_skills,
                        list
                    ):
                        missing_skills = []

                    if not isinstance(
                        extra_skills,
                        list
                    ):
                        extra_skills = []

                    # =================================================
                    # SKILL COUNTS
                    # =================================================

                    matched_count = len(
                        matched_skills
                    )

                    missing_count = len(
                        missing_skills
                    )

                    extra_count = len(
                        extra_skills
                    )

                    # Required JD skills are:
                    # matched + missing
                    total_jd_skills = (
                        matched_count +
                        missing_count
                    )

                    # =================================================
                    # SKILLS MATCHING SUMMARY
                    # =================================================

                    st.divider()

                    st.subheader(
                        "📊 Skills Matching Summary"
                    )

                    summary_col1, summary_col2, summary_col3, summary_col4 = (
                        st.columns(4)
                    )

                    with summary_col1:

                        st.metric(
                            "✅ Matched Skills",
                            matched_count
                        )

                    with summary_col2:

                        st.metric(
                            "❌ Missing Skills",
                            missing_count
                        )

                    with summary_col3:

                        st.metric(
                            "➕ Extra Skills",
                            extra_count
                        )

                    with summary_col4:

                        st.metric(
                            "📋 Total JD Skills",
                            total_jd_skills
                        )

                    # =================================================
                    # MATCHED SKILLS TABLE
                    # =================================================

                    st.divider()

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    if matched_skills:

                        matched_data = []

                        for index, skill in enumerate(
                            matched_skills,
                            start=1
                        ):

                            matched_data.append(
                                {
                                    "S.No": index,
                                    "Skill": str(skill).title(),
                                    "Status": "Matched"
                                }
                            )

                        st.dataframe(
                            matched_data,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.warning(
                            "⚠️ No matched skills found."
                        )

                    # =================================================
                    # MISSING SKILLS TABLE
                    # =================================================

                    st.subheader(
                        "❌ Missing Skills"
                    )

                    if missing_skills:

                        missing_data = []

                        for index, skill in enumerate(
                            missing_skills,
                            start=1
                        ):

                            missing_data.append(
                                {
                                    "S.No": index,
                                    "Required Skill": str(skill).title(),
                                    "Status": "Missing"
                                }
                            )

                        st.dataframe(
                            missing_data,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.success(
                            "🎉 No required skills are missing!"
                        )

                    # =================================================
                    # EXTRA SKILLS TABLE
                    # =================================================

                    st.subheader(
                        "➕ Extra Skills Found in Resume"
                    )

                    if extra_skills:

                        extra_data = []

                        for index, skill in enumerate(
                            extra_skills,
                            start=1
                        ):

                            extra_data.append(
                                {
                                    "S.No": index,
                                    "Extra Skill": str(skill).title(),
                                    "Status": "Additional Skill"
                                }
                            )

                        st.dataframe(
                            extra_data,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.info(
                            "ℹ️ No additional skills found."
                        )

                    # =================================================
                    # SCORE ANALYSIS
                    # =================================================

                    st.divider()

                    st.subheader(
                        "📈 Overall Score Analysis"
                    )

                    # ------------------------------------------------
                    # GET SCORES SAFELY
                    # ------------------------------------------------

                    try:

                        match_percentage = float(
                            result.get(
                                "match_percentage",
                                0
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        match_percentage = 0.0

                    try:

                        compatibility_score = float(
                            result.get(
                                "compatibility_score",
                                0
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        compatibility_score = 0.0

                    try:

                        ats_score = float(
                            result.get(
                                "ats_score",
                                0
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        ats_score = 0.0

                    try:

                        hiring_score = float(
                            result.get(
                                "hiring_score",
                                0
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        hiring_score = 0.0

                    # =================================================
                    # SCORE CARDS
                    # =================================================

                    score_col1, score_col2 = st.columns(2)

                    with score_col1:

                        st.metric(
                            "🎯 Skill Match Percentage",
                            f"{match_percentage:.2f}%"
                        )

                        st.progress(
                            min(
                                max(
                                    match_percentage / 100,
                                    0.0
                                ),
                                1.0
                            )
                        )

                    with score_col2:

                        st.metric(
                            "🔗 Compatibility Score",
                            f"{compatibility_score:.2f}%"
                        )

                        st.progress(
                            min(
                                max(
                                    compatibility_score / 100,
                                    0.0
                                ),
                                1.0
                            )
                        )

                    score_col3, score_col4 = st.columns(2)

                    with score_col3:

                        st.metric(
                            "📄 ATS Score",
                            f"{ats_score:.2f}%"
                        )

                        st.progress(
                            min(
                                max(
                                    ats_score / 100,
                                    0.0
                                ),
                                1.0
                            )
                        )

                    with score_col4:

                        st.metric(
                            "🤖 Hiring Score",
                            f"{hiring_score:.2f}%"
                        )

                        st.progress(
                            min(
                                max(
                                    hiring_score / 100,
                                    0.0
                                ),
                                1.0
                            )
                        )

                    # =================================================
                    # MATCHING CALCULATION
                    # =================================================

                    st.divider()

                    st.subheader(
                        "🔢 Matching Calculation"
                    )

                    if total_jd_skills > 0:

                        matched_ratio = (
                            matched_count /
                            total_jd_skills
                        ) * 100

                        not_matched_ratio = (
                            missing_count /
                            total_jd_skills
                        ) * 100

                    else:

                        matched_ratio = 0.0
                        not_matched_ratio = 0.0

                    # ------------------------------------------------
                    # CALCULATION CARDS
                    # ------------------------------------------------

                    calc_col1, calc_col2 = st.columns(2)

                    with calc_col1:

                        st.metric(
                            "✅ Skills Matched",
                            f"{matched_count} / "
                            f"{total_jd_skills}",
                            f"{matched_ratio:.2f}%"
                        )

                    with calc_col2:

                        st.metric(
                            "❌ Skills Not Matched",
                            f"{missing_count} / "
                            f"{total_jd_skills}",
                            f"{not_matched_ratio:.2f}%"
                        )

                    # ------------------------------------------------
                    # TEXT SUMMARY
                    # ------------------------------------------------

                    st.info(
                        f"""
                        **Total Required Skills in JD:** {total_jd_skills}

                        **Successfully Matched:** {matched_count}

                        **Missing / Not Matched:** {missing_count}

                        **Additional Skills in Resume:** {extra_count}

                        **Overall Skill Match:** {match_percentage:.2f}%
                        """
                    )

                    # =================================================
                    # FINAL AI RECOMMENDATION
                    # =================================================

                    st.divider()

                    st.subheader(
                        "🤖 AI Matching Recommendation"
                    )

                    # ------------------------------------------------
                    # STRONG RECOMMENDATION
                    # ------------------------------------------------

                    if (
                        hiring_score >= 80
                        and match_percentage >= 70
                    ):

                        st.success(
                            "### 🟢 STRONG RECOMMENDATION — "
                            "Highly Suitable"
                        )

                        st.write(
                            f"""
                            The candidate matches
                            **{matched_count} out of "
                            f"{total_jd_skills}** required skills.

                            **Skill Match:** {match_percentage:.2f}%

                            **ATS Score:** {ats_score:.2f}%

                            **Compatibility Score:**
                            {compatibility_score:.2f}%

                            **Hiring Score:** {hiring_score:.2f}%

                            **Recommendation:**
                            Proceed to the next stage of the
                            recruitment process.
                            """
                        )

                    # ------------------------------------------------
                    # MODERATE RECOMMENDATION
                    # ------------------------------------------------

                    elif (
                        hiring_score >= 50
                        or match_percentage >= 40
                    ):

                        st.warning(
                            "### 🟡 MODERATE RECOMMENDATION — "
                            "Further Evaluation Required"
                        )

                        st.write(
                            f"""
                            The candidate matches
                            **{matched_count} out of "
                            f"{total_jd_skills}** required skills.

                            **Missing Skills:** {missing_count}

                            **Skill Match:** {match_percentage:.2f}%

                            **ATS Score:** {ats_score:.2f}%

                            **Compatibility Score:**
                            {compatibility_score:.2f}%

                            **Hiring Score:** {hiring_score:.2f}%

                            **Recommendation:**
                            Consider the candidate for a technical
                            interview or further evaluation.
                            """
                        )

                    # ------------------------------------------------
                    # LOW MATCH
                    # ------------------------------------------------

                    else:

                        st.error(
                            "### 🔴 NOT RECOMMENDED — "
                            "Low Match for Current Role"
                        )

                        st.write(
                            f"""
                            The candidate matches only
                            **{matched_count} out of "
                            f"{total_jd_skills}** required skills.

                            **Missing Skills:** {missing_count}

                            **Skill Match:** {match_percentage:.2f}%

                            **ATS Score:** {ats_score:.2f}%

                            **Compatibility Score:**
                            {compatibility_score:.2f}%

                            **Hiring Score:** {hiring_score:.2f}%

                            **Recommendation:**
                            The candidate is not a strong fit for
                            the current job description.
                            Consider the candidate for another role
                            with a better skill match.
                            """
                        )

                # =====================================================
                # API ERROR
                # =====================================================

                else:

                    st.error(
                        f"❌ Resume-JD matching failed.\n\n"
                        f"Status Code: {response.status_code}"
                    )

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                str(error_data)
                            )
                        )

                    except Exception:

                        st.code(
                            response.text
                        )

            # ========================================================
            # REQUEST ERROR
            # ========================================================

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The matching request timed out. "
                    "Please make sure the FastAPI backend is running "
                    "and try again."
                )
            except requests.exceptions.ConnectionError:
                st.error( "🔌 Could not connect to the backend API. " 
                         "Please start your FastAPI server and try again." 
                        )
            except Exception as e:

                st.error(
                    f"❌ An unexpected error occurred: {str(e)}"
                )


# ============================================================
# AI RESUME SUMMARY
# ============================================================

elif selected_feature == "AI Resume Summary":

    st.header("🤖 AI Resume Summary")

    st.write(
        "Upload a candidate resume to generate an AI-powered "
        "resume summary. Job Description is not required."
    )

    st.divider()

    st.subheader("📄 Upload Candidate Resume")

    resume = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx"],
        key="ai_resume_summary_upload"
    )

    if resume is not None:

        st.success(
            f"✅ Resume selected: {resume.name}"
        )

        if st.button(
            "🤖 Generate AI Resume Summary",
            type="primary",
            use_container_width=True,
            key="generate_ai_resume_summary"
        ):

            try:

                with st.spinner(
                    "🤖 Analyzing resume and generating AI summary..."
                ):

                    files = {
                        "file": (
                            resume.name,
                            resume.getvalue(),
                            resume.type
                        )
                    }

                    summary_response = requests.post(
                        f"{API_URL}/resume-summary",
                        files=files,
                        timeout=60
                    )

                if summary_response.status_code == 200:

                    summary = summary_response.json()

                    st.success(
                        "✅ AI Resume Summary generated successfully!"
                    )

                    st.divider()

                    st.subheader("📝 AI Generated Summary")

                    ai_summary = (
                        summary.get("summary")
                        or summary.get("resume_summary")
                        or summary.get("ai_summary")
                    )

                    if ai_summary:
                        st.info(ai_summary)
                    else:
                        st.warning(
                            "⚠️ The backend did not return a summary."
                        )

                    skills = summary.get("skills", [])

                    if skills:

                        st.subheader("🛠️ Skills")

                        if isinstance(skills, str):
                            skills = [
                                item.strip()
                                for item in skills.split(",")
                                if item.strip()
                            ]

                        for skill in skills:
                            st.write(f"• {skill}")

                    education = summary.get("education")

                    if education:
                        st.subheader("🎓 Education")
                        st.write(education)

                    experience = summary.get("experience")

                    if experience:
                        st.subheader("💼 Experience")
                        st.write(experience)

                    ats_score = summary.get("ats_score")

                    if ats_score is not None:

                        st.subheader("📊 ATS Score")

                        try:
                            st.metric(
                                "ATS Score",
                                f"{float(ats_score):.2f}%"
                            )
                        except (TypeError, ValueError):
                            st.write(ats_score)

                    with st.expander(
                        "🔍 View Complete Backend Response"
                    ):
                        st.json(summary)

                else:

                    st.error(
                        f"❌ Unable to generate AI Resume Summary. "
                        f"Status Code: {summary_response.status_code}"
                    )

                    try:
                        st.code(summary_response.json())
                    except Exception:
                        st.code(summary_response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "🔌 Could not connect to the FastAPI backend. "
                    "Please make sure the backend is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ Resume analysis timed out. Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Error generating AI Resume Summary: {str(e)}"
                )

    else:

        st.info(
            "📌 Upload a PDF or DOCX resume to generate the AI summary."
        )


# ====================================================
# Candidate Ranking
# ====================================================

 
# ==================================================== 

elif selected_feature == "Candidate Ranking": 



    st.header( 
        "🏆 AI Candidate Ranking" 
    ) 



    job_id = st.number_input( 
        "Enter Job ID", 
        min_value=1, 
        step=1, 
        key="ranking_job" 
    ) 



    if st.button( 
        "Rank Candidates" 
    ): 



        response=requests.post( 

            f"{API_URL}/rank-candidates/{job_id}" 

        ) 



        if response.status_code==200: 



            data=response.json() 



            st.success( 
                data["message"] 
            ) 



            ranking=data["ranking"] 



            table = [] 
            for c in ranking: 
                table.append( 
                    { 
                        "Rank": c["rank"], 
                        "Candidate": c["candidate_name"], 
                        "Match %": c["match_percentage"], 
                        "Match Score": c["match_score"], 
                        "ATS Score": c["ats_score"], 
                        "Compatibility Score": c["compatibility_score"], 
                        "Hiring Score": c["hiring_score"] 
                    } 
                ) 
            df = pd.DataFrame(table) 
            st.dataframe( 
                df, 
                use_container_width=True 
            ) 



        else: 

            st.error( 
                "Ranking failed." 
            ) 
# ==================================================== 
# AI Resume Summary 
# ==================================================== 

elif selected_feature == "Screening & Performance":

    st.header("🎤 Screening & Performance")
    st.write(
        "Review completed AI voice-screening results and candidate performance."
    )

    st.divider()

    try:
        # ========================================================
        # LOAD ALL CANDIDATES
        # ========================================================
        candidates_response = requests.get(
            f"{API_URL}/candidates",
            timeout=10
        )

        if candidates_response.status_code != 200:
            st.error(
                f"❌ Unable to load candidates. Backend returned "
                f"{candidates_response.status_code}."
            )
        else:
            candidates_data = candidates_response.json()

            # Support both {"candidates": [...]} and [...] responses.
            if isinstance(candidates_data, dict):
                candidates = candidates_data.get("candidates", [])
            elif isinstance(candidates_data, list):
                candidates = candidates_data
            else:
                candidates = []

            candidates = [
                c for c in candidates if isinstance(c, dict)
            ]

            st.subheader("📋 Candidate Screening Results")

            if not candidates:
                st.info("📭 No candidates are available in the database yet.")
            else:
                # ========================================================
                # FIND COMPLETED SCREENINGS
                # ========================================================
                completed_screenings = []

                for candidate in candidates:
                    candidate_id = candidate.get(
                        "id", candidate.get("candidate_id")
                    )
                    candidate_name = candidate.get(
                        "name", "Unknown Candidate"
                    )

                    if candidate_id is None:
                        continue

                    try:
                        summary_response = requests.get(
                            f"{API_URL}/screening-summary/{candidate_id}",
                            timeout=10
                        )

                        if summary_response.status_code == 200:
                            summary_data = summary_response.json()
                            summary = summary_data.get("summary")

                            if summary:
                                completed_screenings.append({
                                    "candidate_id": candidate_id,
                                    "candidate_name": candidate_name,
                                    "candidate": candidate,
                                    "summary": summary
                                })
                    except requests.RequestException:
                        continue

                # ========================================================
                # SCREENING COUNTS
                # ========================================================
                total_candidates = len(candidates)
                completed_count = len(completed_screenings)
                pending_count = total_candidates - completed_count

                count_col1, count_col2, count_col3 = st.columns(3)

                with count_col1:
                    st.metric("👥 Total Candidates", total_candidates)

                with count_col2:
                    st.metric("🎤 Completed Screening", completed_count)

                with count_col3:
                    st.metric("⏳ Pending Screening", pending_count)

                st.divider()

                if not completed_screenings:
                    st.warning(
                        "⚠️ Candidates are available, but no completed "
                        "voice-screening result has been saved yet."
                    )
                    st.info(
                        "Complete Candidate Dashboard → Interview for a candidate. "
                        "After the five questions are answered, the screening "
                        "summary will appear here."
                    )
                else:
                    # ====================================================
                    # DISPLAY ALL COMPLETED SCREENINGS
                    # ====================================================
                    screening_rows = []

                    for item in completed_screenings:
                        summary = item["summary"]
                        candidate = item["candidate"]

                        overall_score = summary.get(
                            "overall_score",
                            summary.get("final_score", 0)
                        )

                        try:
                            score_display = f"{float(overall_score):.1f}%"
                        except (TypeError, ValueError):
                            score_display = str(overall_score)

                        recommendation = summary.get(
                            "recommendation",
                            summary.get("hiring_recommendation", "N/A")
                        ) or "N/A"

                        screening_rows.append({
                            "Candidate ID": item["candidate_id"],
                            "Candidate": item["candidate_name"],
                            "Screening Score": score_display,
                            "AI Recommendation": recommendation,
                            "Recruiter Status": candidate.get(
                                "status", "Under Review"
                            )
                        })

                    st.subheader("📊 Completed Screening Results")
                    st.dataframe(
                        pd.DataFrame(screening_rows),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.divider()

                    # ====================================================
                    # SELECT CANDIDATE
                    # ====================================================
                    candidate_options = {}

                    for item in completed_screenings:
                        label = (
                            f"{item['candidate_name']} "
                            f"(ID: {item['candidate_id']})"
                        )
                        candidate_options[label] = item

                    selected_label = st.selectbox(
                        "👤 Select Candidate to View Full Performance",
                        list(candidate_options.keys()),
                        key="screening_performance_candidate"
                    )

                    selected_data = candidate_options[selected_label]
                    selected_candidate_id = selected_data["candidate_id"]
                    selected_candidate_name = selected_data["candidate_name"]
                    selected_candidate = selected_data["candidate"]
                    summary = selected_data["summary"]

                    # ====================================================
                    # QUESTION-WISE RESULTS
                    # ====================================================
                    interview_results = []

                    try:
                        interview_response = requests.get(
                            f"{API_URL}/interview-results/{selected_candidate_id}",
                            timeout=10
                        )

                        if interview_response.status_code == 200:
                            interview_data = interview_response.json()

                            if isinstance(interview_data, dict):
                                interview_results = interview_data.get(
                                    "results", []
                                )
                            elif isinstance(interview_data, list):
                                interview_results = interview_data
                    except requests.RequestException:
                        interview_results = []

                    if not isinstance(interview_results, list):
                        interview_results = []

                    interview_results = [
                        result for result in interview_results
                        if isinstance(result, dict)
                    ]

                    # ====================================================
                    # SUMMARY VALUES
                    # ====================================================
                    overall_score = summary.get(
                        "overall_score",
                        summary.get("final_score", 0)
                    )

                    recommendation = summary.get(
                        "recommendation",
                        summary.get("hiring_recommendation", "N/A")
                    ) or "N/A"

                    strengths = summary.get(
                        "strengths",
                        summary.get("strength", "")
                    )

                    improvement = summary.get(
                        "improvement",
                        summary.get(
                            "improvement_areas",
                            summary.get("improvements", "")
                        )
                    )

                    # ====================================================
                    # CANDIDATE INFORMATION
                    # ====================================================
                    st.divider()
                    st.subheader("👤 Candidate Information")

                    info_col1, info_col2, info_col3 = st.columns(3)

                    with info_col1:
                        st.write("**Candidate:**")
                        st.write(selected_candidate_name)

                    with info_col2:
                        st.write("**Candidate ID:**")
                        st.write(selected_candidate_id)

                    with info_col3:
                        st.write("**Current Status:**")
                        st.write(
                            selected_candidate.get(
                                "status", "Under Review"
                            )
                        )

                    # ====================================================
                    # SCORE CARDS
                    # ====================================================
                    st.divider()
                    st.subheader("🎯 Screening Performance")

                    score_col1, score_col2, score_col3 = st.columns(3)

                    try:
                        score_value = float(overall_score)
                        score_display = f"{score_value:.1f}%"
                    except (TypeError, ValueError):
                        score_value = 0.0
                        score_display = str(overall_score)

                    with score_col1:
                        st.metric(
                            "🎤 Voice Screening Score",
                            score_display
                        )

                    with score_col2:
                        st.metric(
                            "📋 Questions",
                            len(interview_results) if interview_results else 5
                        )

                    with score_col3:
                        st.metric(
                            "🏆 Recommendation",
                            str(recommendation)
                        )

                    # ====================================================
                    # AI RECOMMENDATION
                    # ====================================================
                    st.divider()
                    st.subheader("🤖 AI Hiring Recommendation")

                    recommendation_lower = str(
                        recommendation
                    ).lower()

                    if (
                        "hire" in recommendation_lower
                        or "strong" in recommendation_lower
                        or "suitable" in recommendation_lower
                        or "selected" in recommendation_lower
                    ):
                        st.success(f"✅ {recommendation}")
                    elif (
                        "reject" in recommendation_lower
                        or "weak" in recommendation_lower
                    ):
                        st.error(f"❌ {recommendation}")
                    else:
                        st.warning(f"⚠️ {recommendation}")

                    # ====================================================
                    # STRENGTHS / IMPROVEMENT
                    # ====================================================
                    strength_col, improvement_col = st.columns(2)

                    with strength_col:
                        st.subheader("💪 Strengths")

                        if isinstance(strengths, list):
                            for item in strengths:
                                st.write(f"• {item}")
                        elif strengths:
                            st.success(str(strengths))
                        else:
                            st.info("No strengths recorded.")

                    with improvement_col:
                        st.subheader("📈 Areas for Improvement")

                        if isinstance(improvement, list):
                            for item in improvement:
                                st.write(f"• {item}")
                        elif improvement:
                            st.warning(str(improvement))
                        else:
                            st.info("No improvement areas recorded.")

                    # ====================================================
                    # QUESTION-WISE RESULTS
                    # ====================================================
                    st.divider()
                    st.subheader("📝 Question-wise Interview Results")

                    if interview_results:
                        question_rows = []

                        for index, result in enumerate(
                            interview_results, start=1
                        ):
                            question = result.get(
                                "question", f"Question {index}"
                            )

                            score = result.get(
                                "score",
                                result.get(
                                    "question_score",
                                    result.get("final_score", "N/A")
                                )
                            )

                            feedback = result.get(
                                "feedback",
                                result.get(
                                    "evaluation",
                                    result.get(
                                        "answer_evaluation", ""
                                    )
                                )
                            )

                            transcript = result.get(
                                "transcript",
                                result.get("answer", "")
                            )

                            question_rows.append({
                                "Question": question,
                                "Score": score,
                                "Feedback": feedback,
                                "Candidate Answer": transcript
                            })

                        st.dataframe(
                            pd.DataFrame(question_rows),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info(
                            "Question-wise records are not available from "
                            "the interview-results API, but the overall "
                            "screening summary was successfully saved."
                        )

                    # ====================================================
                    # RECRUITER FINAL DECISION
                    # ====================================================
                    st.divider()
                    st.subheader("👨‍💼 Recruiter Final Decision")

                    decision_col1, decision_col2, decision_col3 = st.columns(3)

                    def update_recruiter_decision(new_status):
                        try:
                            update_response = requests.put(
                                f"{API_URL}/candidate/"
                                f"{selected_candidate_id}/status",
                                params={"status": new_status},
                                timeout=10
                            )

                            if update_response.status_code == 200:
                                st.success(
                                    f"✅ Candidate status updated to {new_status}."
                                )
                                st.rerun()
                            else:
                                st.error(
                                    "❌ Failed to update candidate status. "
                                    f"Backend returned "
                                    f"{update_response.status_code}."
                                )
                        except requests.RequestException as exc:
                            st.error(
                                f"❌ Unable to update candidate status: {exc}"
                            )

                    with decision_col1:
                        if st.button(
                            "✅ Hire",
                            use_container_width=True,
                            key=f"screen_hire_{selected_candidate_id}"
                        ):
                            update_recruiter_decision("Hired")

                    with decision_col2:
                        if st.button(
                            "🟢 Shortlist",
                            use_container_width=True,
                            key=f"screen_shortlist_{selected_candidate_id}"
                        ):
                            update_recruiter_decision("Shortlisted")

                    with decision_col3:
                        if st.button(
                            "❌ Reject",
                            use_container_width=True,
                            key=f"screen_reject_{selected_candidate_id}"
                        ):
                            update_recruiter_decision("Rejected")

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Backend is not running. Please start FastAPI first."
        )
    except requests.exceptions.Timeout:
        st.error(
            "❌ Backend request timed out. Please make sure FastAPI is running correctly."
        )
    except Exception as e:
        st.error(
            f"❌ Error while loading Screening & Performance: {e}"
        )


# ==================================================== 
# AI Resume JD Analysis 
# ==================================================== 

elif selected_feature == "Resume-JD AI Analysis": 



    st.header( 
        "🔍 AI Resume vs Job Description Analysis" 
    ) 



    resume = st.file_uploader( 

        "Upload Resume", 

        type=["pdf","docx"], 

        key="analysis_resume" 

    ) 



    job_id = st.number_input( 

        "Enter Job ID", 

        min_value=1, 

        step=1, 

        key="analysis_job" 

    ) 



    if st.button( 
        "Analyze Resume" 
    ): 



        if resume is None: 

            st.warning( 
                "Upload resume." 
            ) 



        else: 



            files={ 

                "resume": 
                ( 
                    resume.name, 
                    resume, 
                    resume.type 
                ) 

            } 



            data={ 

                "job_id":job_id 

            } 



            response=requests.post( 

                f"{API_URL}/resume-jd-analysis", 

                files=files, 

                data=data 

            ) 



            if response.status_code==200: 



                result=response.json() 



                st.subheader( 
                    "🤖 AI Recruiter Analysis" 
                ) 



                st.write( 
                    result["analysis"] 
                ) 



            else: 



                st.error( 
                    "Analysis failed." 
                ) 







# ==================================================== 
# AI Interview Questions 
# ==================================================== 

elif selected_feature == "AI Interview Questions": 



    st.header( 
        "🎤 AI Interview Question Generator" 
    ) 



    resume = st.file_uploader( 

        "Upload Candidate Resume", 

        type=["pdf","docx"], 

        key="interview_resume" 

    ) 



    job_id = st.number_input( 

        "Enter Job ID", 

        min_value=1, 

        step=1, 

        key="interview_job" 

    ) 



    if st.button( 
        "Generate Interview Questions" 
    ): 



        if resume is None: 

            st.warning( 
                "Please upload resume." 
            ) 



        else: 



            files={ 

                "resume": 
                ( 
                    resume.name, 
                    resume, 
                    resume.type 
                ) 

            } 



            data={ 

                "job_id":job_id 

            } 



            response=requests.post( 

                f"{API_URL}/ai-interview-questions", 

                files=files, 

                data=data 

            ) 



            if response.status_code==200: 



                result=response.json() 



                st.subheader( 
                    "🤖 Generated Questions" 
                ) 



                st.write( 

                    result["interview_questions"] 

                ) 



            else: 

                st.error( 
                    "Unable to generate questions." 
                ) 









# ==================================================== 
# AI Hiring Recommendation 
# ==================================================== 

elif selected_feature == "AI Hiring Recommendation": 



    st.header( 
        "🤖 AI Hiring Decision" 
    ) 



    resume = st.file_uploader( 

        "Upload Candidate Resume", 

        type=["pdf","docx"], 

        key="hire_resume" 

    ) 



    job_id = st.number_input( 

        "Enter Job ID", 

        min_value=1, 

        step=1, 

        key="hire_job" 

    ) 



    if st.button( 
        "Generate Hiring Recommendation" 
    ): 



        if resume is None: 



            st.warning( 
                "Please upload resume." 
            ) 



        else: 



            files={ 

                "resume": 
                ( 
                    resume.name, 
                    resume, 
                    resume.type 
                ) 

            } 



            data={ 

                "job_id":job_id 

            } 



            response=requests.post( 

                f"{API_URL}/hiring-recommendation", 

                files=files, 

                data=data 

            ) 



            if response.status_code==200: 



                result=response.json() 



                st.subheader( 
                    "📋 AI Hiring Recommendation" 
                ) 



                st.write( 

                    result["hiring_recommendation"] 

                ) 



            else: 



                st.error( 
                    "Recommendation failed." 
                ) 







# ==================================================== 
# AI Email Generator 
# ==================================================== 

elif selected_feature == "AI Email Generator": 



    st.header( 
        "📧 AI Recruitment Email Generator" 
    ) 



    candidate_id = st.number_input( 

        "Candidate ID", 

        min_value=1, 

        step=1, 

        key="email_candidate" 

    ) 



    job_id = st.number_input( 

        "Job ID", 

        min_value=1, 

        step=1, 

        key="email_job" 

    ) 



    email_type = st.selectbox( 

        "Email Type", 

        [ 

            "Interview Invitation", 

            "Shortlisting", 

            "Offer Letter", 

            "Rejection" 

        ] 

    ) 



    if st.button( 
        "Generate Email" 
    ): 



        response=requests.get( 

            f"{API_URL}/generate-email/{candidate_id}/{job_id}/{email_type}" 

        ) 



        if response.status_code==200: 



            result=response.json() 



            st.subheader( 
                "📨 Generated Email" 
            ) 



            if "email" in result: 

                st.write( 
                    result["email"] 
                ) 

            else: 

                st.write( 
                    result 
                ) 



        else: 



            st.error( 
                "Email generation failed." 
            ) 
# ==================================================== 
# Recruiter Analytics 
# ==================================================== 

elif selected_feature == "Recruiter Analytics": 



    st.header("📊 Recruiter Analytics Dashboard") 



    response = requests.get( 
        f"{API_URL}/analytics" 
    ) 



    if response.status_code == 200: 



        data = response.json() 





        col1,col2,col3,col4,col5 = st.columns(5) 





        with col1: 

            st.metric( 
                "👥 Candidates", 
                data["total_candidates"] 
            ) 



        with col2: 

            st.metric( 
                "💼 Jobs", 
                data["total_jobs"] 
            ) 



        with col3: 

            st.metric( 
                "🎯 Avg Match", 
                f'{data["average_match_score"]}%' 
            ) 



        with col4: 

            st.metric( 
                "✅ Selected", 
                data["shortlisted_candidates"] 
            ) 



        with col5: 

            st.metric( 
                "❌ Rejected", 
                data["rejected_candidates"] 
            ) 



    else: 

        st.error( 
            "Unable to load analytics" 
        ) 
elif selected_feature == "AI Interview Evaluation": 

    st.header("🧠 AI Interview Evaluation") 

    candidate_id = st.number_input( 
        "Candidate ID", 
        min_value=1 
    ) 

    job_id = st.number_input( 
        "Job ID", 
        min_value=1 
    ) 

    answers = st.text_area( 
        "Enter Candidate Answers" 
    ) 

    if st.button("Evaluate Interview"): 

        response = requests.post( 
            f"{API_URL}/evaluate-interview", 
            json={ 
                "candidate_id": candidate_id, 
                "job_id": job_id, 
                "answers": answers 
            } 
        ) 

        if response.status_code == 200: 
            st.success("Interview evaluated successfully!") 
            st.write(response.json()["evaluation"]) 
        else: 
            st.error("Evaluation failed.") 
# ============================================================ 
# VOICE-BASED SCREENING 
# ============================================================ 

if selected_feature == "Voice-Based Screening": 

    st.title("🎤 Voice-Based Screening") 

    st.write( 
        "Conduct an AI-powered voice interview with the candidate." 
    ) 

    st.info( 
        "Questions → 🎤 Microphone → Speech-to-Text → " 
        "🤖 AI Evaluation → Next Question → 🏆 Final Score" 
    ) 

    st.divider() 

    # ======================================================== 
    # CHECK GROQ 
    # ======================================================== 

    if groq_client is None: 

        st.error("GROQ_API_KEY is not configured.") 

        st.info( 
            "Please add GROQ_API_KEY to your .env file " 
            "and restart Streamlit." 
        ) 

        st.stop() 

    # ======================================================== 
    # HELPER FUNCTION - PARSE AI EVALUATION 
    # ======================================================== 

    def parse_voice_evaluation(evaluation_text): 

        feedback = "" 
        strengths = [] 
        improvement = "" 

        lines = evaluation_text.splitlines() 

        current_section = None 

        for raw_line in lines: 

            line = raw_line.strip() 

            if not line: 
                continue 

            upper_line = line.upper() 

            # ----------------------------------------------- 
            # FEEDBACK 
            # ----------------------------------------------- 

            if upper_line.startswith("FEEDBACK:"): 

                current_section = "feedback" 

                feedback = line.split( 
                    ":", 
                    1 
                )[1].strip() 

                continue 

            # ----------------------------------------------- 
            # STRENGTHS 
            # ----------------------------------------------- 

            if upper_line.startswith("STRENGTHS:"): 

                current_section = "strengths" 

                continue 

            # ----------------------------------------------- 
            # IMPROVEMENT 
            # ----------------------------------------------- 

            if upper_line.startswith("IMPROVEMENT:"): 

                current_section = "improvement" 

                improvement = line.split( 
                    ":", 
                    1 
                )[1].strip() 

                continue 

            # ----------------------------------------------- 
            # COLLECT FEEDBACK 
            # ----------------------------------------------- 

            if current_section == "feedback": 

                feedback += ( 
                    " " + line 
                    if feedback 
                    else line 
                ) 

            # ----------------------------------------------- 
            # COLLECT STRENGTHS 
            # ----------------------------------------------- 

            elif current_section == "strengths": 

                if line.startswith("-"): 

                    strengths.append( 
                        line.lstrip("- ").strip() 
                    ) 

                elif not upper_line.startswith( 
                    "IMPROVEMENT:" 
                ): 

                    strengths.append(line) 

            # ----------------------------------------------- 
            # COLLECT IMPROVEMENT 
            # ----------------------------------------------- 

            elif current_section == "improvement": 

                improvement += ( 
                    " " + line 
                    if improvement 
                    else line 
                ) 

        return { 
            "feedback": feedback.strip(), 
            "strengths": strengths, 
            "improvement": improvement.strip() 
        } 

    # ======================================================== 
    # INITIALIZE SESSION STATE 
    # ======================================================== 

    if "voice_questions" not in st.session_state: 
        st.session_state.voice_questions = [] 

    if "voice_question_index" not in st.session_state: 
        st.session_state.voice_question_index = 0 

    if "voice_answers" not in st.session_state: 
        st.session_state.voice_answers = [] 

    if "voice_scores" not in st.session_state: 
        st.session_state.voice_scores = [] 

    if "voice_evaluations" not in st.session_state: 
        st.session_state.voice_evaluations = [] 

    if "voice_candidate_name" not in st.session_state: 
        st.session_state.voice_candidate_name = "" 

    if "voice_job_id" not in st.session_state: 
        st.session_state.voice_job_id = None 

    if "voice_interview_started" not in st.session_state: 
        st.session_state.voice_interview_started = False 

    if "voice_interview_finished" not in st.session_state: 
        st.session_state.voice_interview_finished = False 

    if "voice_overall_analysis" not in st.session_state: 
        st.session_state.voice_overall_analysis = None 
    if "voice_summary_saved" not in st.session_state: 
        st.session_state.voice_summary_saved = False 

    # ======================================================== 
    # STAGE 1 - INTERVIEW RESULT SESSION STATE 
    # ======================================================== 

    if "voice_final_score" not in st.session_state: 
        st.session_state.voice_final_score = 0.0 

    if "voice_recommendation" not in st.session_state: 
        st.session_state.voice_recommendation = "" 

    if "voice_overall_feedback" not in st.session_state: 
        st.session_state.voice_overall_feedback = "" 

    if "voice_overall_strengths" not in st.session_state: 
        st.session_state.voice_overall_strengths = [] 

    if "voice_overall_improvement" not in st.session_state: 
        st.session_state.voice_overall_improvement = "" 

    # ======================================================== 
    # SELECT CANDIDATE 
    # ======================================================== 

    st.subheader("👤 Select Candidate") 

    try: 

        candidate_response = requests.get( 
            f"{API_URL}/candidates", 
            timeout=10 
        ) 

        if candidate_response.status_code != 200: 

            st.error( 
                "Unable to retrieve candidates." 
            ) 

            st.stop() 

        candidate_data = candidate_response.json() 

        if ( 
            isinstance(candidate_data, dict) 
            and "candidates" in candidate_data 
        ): 

            candidates = candidate_data["candidates"] 

        else: 

            candidates = candidate_data 

        if not isinstance(candidates, list): 

            candidates = [] 

        valid_candidates = [ 
            candidate 
            for candidate in candidates 
            if isinstance(candidate, dict) 
        ] 

        if not valid_candidates: 

            st.warning( 
                "No candidates available." 
            ) 

            st.stop() 

        # ==================================================== 
        # CANDIDATE DROPDOWN 
        # ==================================================== 

        candidate_names = [ 
            candidate.get( 
                "name", 
                "Unknown Candidate" 
            ) 
            for candidate in valid_candidates 
        ] 

        selected_candidate_name = st.selectbox( 
            "Choose Candidate", 
            candidate_names, 
            key="voice_candidate_select" 
        ) 

        # ==================================================== 
        # GET SELECTED CANDIDATE 
        # ==================================================== 

        selected_candidate = next( 
            ( 
                candidate 
                for candidate in valid_candidates 
                if candidate.get("name") 
                == selected_candidate_name 
            ), 
            None 
        ) 

        if selected_candidate is None: 

            st.warning( 
                "Unable to find selected candidate." 
            ) 

            st.stop() 

        st.success( 
            f"Selected Candidate: " 
            f"{selected_candidate_name}" 
        ) 

        # ==================================================== 
        # CANDIDATE INFORMATION 
        # ==================================================== 

        st.subheader( 
            "📋 Candidate Information" 
        ) 

        col1, col2 = st.columns(2) 

        with col1: 

            st.write( 
                "**Name:**", 
                selected_candidate.get( 
                    "name", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Email:**", 
                selected_candidate.get( 
                    "email", 
                    "N/A" 
                ) 
            ) 

        with col2: 

            st.write( 
                "**Phone:**", 
                selected_candidate.get( 
                    "phone", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Status:**", 
                selected_candidate.get( 
                    "status", 
                    "N/A" 
                ) 
            ) 

        # ==================================================== 
        # SELECT JOB 
        # ==================================================== 

        st.divider() 

        st.subheader( 
            "💼 Select Job" 
        ) 

        job_response = requests.get( 
            f"{API_URL}/jobs", 
            timeout=10 
        ) 

        if job_response.status_code != 200: 

            st.error( 
                "Unable to retrieve job openings." 
            ) 

            st.stop() 

        job_data = job_response.json() 

        if ( 
            isinstance(job_data, dict) 
            and "jobs" in job_data 
        ): 

            jobs = job_data["jobs"] 

        else: 

            jobs = job_data 

        if not isinstance(jobs, list): 

            jobs = [] 

        if not jobs: 

            st.warning( 
                "No job openings available." 
            ) 

            st.stop() 

        # ==================================================== 
        # JOB OPTIONS 
        # ==================================================== 

        job_options = [] 

        job_lookup = {} 

        for job in jobs: 

            if not isinstance(job, dict): 
                continue 

            job_id = job.get("id") 

            job_title = job.get( 
                "job_title", 
                "Unknown Job" 
            ) 

            if job_id: 

                display_name = ( 
                    f"{job_title} " 
                    f"(ID: {job_id})" 
                ) 

                job_options.append( 
                    display_name 
                ) 

                job_lookup[ 
                    display_name 
                ] = job 

        if not job_options: 

            st.warning( 
                "No valid job records found." 
            ) 

            st.stop() 

        # ==================================================== 
        # JOB DROPDOWN 
        # ==================================================== 

        selected_job_display = st.selectbox( 
            "Choose Job", 
            job_options, 
            key="voice_job_select" 
        ) 

        selected_job = job_lookup.get( 
            selected_job_display 
        ) 

        if selected_job is None: 

            st.warning( 
                "Unable to find selected job." 
            ) 

            st.stop() 

        st.success( 
            f"Selected Job: " 
            f"{selected_job.get('job_title', 'N/A')}" 
        ) 

        # ==================================================== 
        # JOB DETAILS 
        # ==================================================== 

        with st.expander( 
            "📄 View Job Details" 
        ): 

            st.write( 
                "**Job Title:**", 
                selected_job.get( 
                    "job_title", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Company:**", 
                selected_job.get( 
                    "company_name", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Location:**", 
                selected_job.get( 
                    "location", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Experience:**", 
                selected_job.get( 
                    "experience", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Education:**", 
                selected_job.get( 
                    "education", 
                    "N/A" 
                ) 
            ) 

            st.write( 
                "**Skills:**", 
                selected_job.get( 
                    "skills", 
                    "N/A" 
                ) 
            ) 

        # ==================================================== 
        # BUILD CANDIDATE PROFILE 
        # ==================================================== 

        candidate_profile = [] 

        candidate_profile.append( 
            f"Name: " 
            f"{selected_candidate.get('name', 'N/A')}" 
        ) 

        candidate_profile.append( 
            f"Email: " 
            f"{selected_candidate.get('email', 'N/A')}" 
        ) 

        candidate_profile.append( 
            f"Phone: " 
            f"{selected_candidate.get('phone', 'N/A')}" 
        ) 

        candidate_profile.append( 
            f"Status: " 
            f"{selected_candidate.get('status', 'N/A')}" 
        ) 

        # ==================================================== 
        # SKILLS 
        # ==================================================== 

        skills = selected_candidate.get( 
            "skills", 
            [] 
        ) 

        if isinstance(skills, list): 

            candidate_profile.append( 
                "Skills: " 
                + ", ".join( 
                    str(skill) 
                    for skill in skills 
                ) 
            ) 

        else: 

            candidate_profile.append( 
                f"Skills: {skills}" 
            ) 

        # ==================================================== 
        # EDUCATION 
        # ==================================================== 

        education = selected_candidate.get( 
            "education", 
            [] 
        ) 

        if isinstance(education, list): 

            candidate_profile.append( 
                "Education:\n" 
                + "\n".join( 
                    str(item) 
                    for item in education 
                ) 
            ) 

        else: 

            candidate_profile.append( 
                f"Education: {education}" 
            ) 

        # ==================================================== 
        # EXPERIENCE 
        # ==================================================== 

        experience = selected_candidate.get( 
            "experience", 
            [] 
        ) 

        if isinstance(experience, list): 

            candidate_profile.append( 
                "Experience:\n" 
                + "\n".join( 
                    str(item) 
                    for item in experience 
                ) 
            ) 

        else: 

            candidate_profile.append( 
                f"Experience: {experience}" 
            ) 

        # ==================================================== 
        # PROJECTS 
        # ==================================================== 

        projects = selected_candidate.get( 
            "projects", 
            [] 
        ) 

        if projects: 

            if isinstance(projects, list): 

                candidate_profile.append( 
                    "Projects:\n" 
                    + "\n".join( 
                        str(project) 
                        for project in projects 
                    ) 
                ) 

            else: 

                candidate_profile.append( 
                    f"Projects: {projects}" 
                ) 

        # ==================================================== 
        # CERTIFICATIONS 
        # ==================================================== 

        certifications = selected_candidate.get( 
            "certifications", 
            [] 
        ) 

        if certifications: 

            if isinstance( 
                certifications, 
                list 
            ): 

                candidate_profile.append( 
                    "Certifications:\n" 
                    + "\n".join( 
                        str(item) 
                        for item in certifications 
                    ) 
                ) 

            else: 

                candidate_profile.append( 
                    f"Certifications: " 
                    f"{certifications}" 
                ) 

        # ==================================================== 
        # LANGUAGES 
        # ==================================================== 

        languages = selected_candidate.get( 
            "languages", 
            [] 
        ) 

        if languages: 

            if isinstance( 
                languages, 
                list 
            ): 

                candidate_profile.append( 
                    "Languages: " 
                    + ", ".join( 
                        str(item) 
                        for item in languages 
                    ) 
                ) 

            else: 

                candidate_profile.append( 
                    f"Languages: {languages}" 
                ) 

        # ==================================================== 
        # ORIGINAL RESUME 
        # ==================================================== 

        original_resume = selected_candidate.get( 
            "resume_text", 
            "" 
        ) 

        if original_resume: 

            candidate_profile.append( 
                "Original Resume Text:\n" 
                + str(original_resume) 
            ) 

        resume_text = "\n\n".join( 
            candidate_profile 
        ) 

        # ==================================================== 
        # JOB INFORMATION FOR AI 
        # ==================================================== 

        job_title = selected_job.get( 
            "job_title", 
            "N/A" 
        ) 

        job_skills = selected_job.get( 
            "skills", 
            [] 
        ) 

        job_information = ( 
            f"Job Title: {job_title}\n" 
            f"Company: " 
            f"{selected_job.get('company_name', 'N/A')}\n" 
            f"Location: " 
            f"{selected_job.get('location', 'N/A')}\n" 
            f"Experience: " 
            f"{selected_job.get('experience', 'N/A')}\n" 
            f"Education: " 
            f"{selected_job.get('education', 'N/A')}\n" 
            f"Skills: {job_skills}\n" 
        ) 

        # ==================================================== 
        # GENERATE INTERVIEW QUESTIONS 
        # ==================================================== 

        st.divider() 

        st.subheader( 
            "🤖 AI Interview Questions" 
        ) 

        st.write( 
            "Generate questions based on the " 
            "candidate profile and selected job." 
        ) 

        if not st.session_state.voice_interview_started: 

            if st.button( 
                "🤖 Generate Interview Questions", 
                use_container_width=True, 
                key="generate_voice_questions" 
            ): 

                with st.spinner( 
                    "Generating interview questions..." 
                ): 

                    try: 

                        prompt = f""" 
You are an expert technical interviewer. 

Generate exactly 5 interview questions for this candidate 
and job. 

CANDIDATE: 
{resume_text} 

JOB: 
{job_information} 

Requirements: 

1. Questions must be relevant to the candidate. 
2. Questions must be relevant to the job. 
3. Include technical questions. 
4. Include project/experience questions. 
5. Include one behavioral question. 
6. Do not provide answers. 
7. Number the questions from 1 to 5. 

Return ONLY the numbered questions. 
""" 

                        completion = ( 
                            groq_client 
                            .chat 
                            .completions 
                            .create( 
                                model=( 
                                    "openai/gpt-oss-20b" 
                                ), 
                                messages=[ 
                                    { 
                                        "role": "system", 
                                        "content": ( 
                                            "You are an " 
                                            "expert interviewer." 
                                        ) 
                                    }, 
                                    { 
                                        "role": "user", 
                                        "content": prompt 
                                    } 
                                ], 
                                temperature=0.3 
                            ) 
                        ) 

                        generated_text = ( 
                            completion 
                            .choices[0] 
                            .message 
                            .content 
                        ) 

                        # ==================================== 
                        # PARSE QUESTIONS 
                        # ==================================== 

                        raw_lines = ( 
                            generated_text 
                            .splitlines() 
                        ) 

                        questions = [] 

                        for line in raw_lines: 

                            line = line.strip() 

                            if not line: 
                                continue 

                            cleaned = line 

                            if ( 
                                len(cleaned) > 2 
                                and cleaned[0].isdigit() 
                            ): 

                                cleaned = ( 
                                    cleaned 
                                    .lstrip( 
                                        "0123456789" 
                                    ) 
                                    .lstrip( 
                                        ".):- " 
                                    ) 
                                ) 

                            if cleaned: 

                                questions.append( 
                                    cleaned 
                                ) 

                        questions = questions[:5] 

                        if not questions: 

                            st.error( 
                                "No interview questions " 
                                "were generated." 
                            ) 

                        else: 

                            # ================================ 
                            # RESET INTERVIEW 
                            # ================================ 

                            st.session_state.voice_questions = ( 
                                questions 
                            ) 

                            st.session_state.voice_question_index = 0 

                            st.session_state.voice_answers = [] 

                            st.session_state.voice_scores = [] 

                            st.session_state.voice_evaluations = [] 

                            st.session_state.voice_candidate_name = ( 
                                selected_candidate_name 
                            ) 

                            st.session_state.voice_job_id = ( 
                                selected_job.get("id") 
                            ) 

                            st.session_state.voice_interview_started = ( 
                                True 
                            ) 

                            st.session_state.voice_interview_finished = ( 
                                False 
                            ) 

                            st.session_state.voice_overall_analysis = None 

                            # Stage 1 result reset 
                            st.session_state.voice_final_score = 0.0 
                            st.session_state.voice_recommendation = "" 
                            st.session_state.voice_overall_feedback = "" 
                            st.session_state.voice_overall_strengths = [] 
                            st.session_state.voice_overall_improvement = "" 

                            st.session_state[ 
                                "current_transcript" 
                            ] = "" 

                            st.rerun() 

                    except Exception as e: 

                        st.error( 
                            f"Question generation error: {e}" 
                        ) 

        # ==================================================== 
        # ACTIVE VOICE INTERVIEW 
        # ==================================================== 

        if ( 
            st.session_state.voice_interview_started 
            and not st.session_state.voice_interview_finished 
        ): 

            questions = ( 
                st.session_state.voice_questions 
            ) 

            current_index = ( 
                st.session_state.voice_question_index 
            ) 

            total_questions = len( 
                questions 
            ) 

            # ================================================= 
            # SAFETY CHECK 
            # ================================================= 

            if current_index >= total_questions: 

                st.session_state.voice_interview_finished = True 

                st.rerun() 

            else: 

                current_question = questions[ 
                    current_index 
                ] 

                # ============================================= 
                # PROGRESS 
                # ============================================= 

                st.progress( 
                    current_index / total_questions 
                ) 

                st.write( 
                    f"Question " 
                    f"{current_index + 1} " 
                    f"of " 
                    f"{total_questions}" 
                ) 

                # ============================================= 
                # QUESTION 
                # ============================================= 

                st.markdown( 
                    f"### 🎤 Question " 
                    f"{current_index + 1}" 
                ) 

                st.info( 
                    current_question 
                ) 

                st.write( 
                    "Click the microphone button below " 
                    "and speak your answer." 
                ) 

                # ============================================= 
                # MICROPHONE 
                # ============================================= 

                audio_value = st.audio_input( 
                    "🎙️ Record your answer", 
                    key=( 
                        f"voice_audio_" 
                        f"{current_index}" 
                    ) 
                ) 

                # ============================================= 
                # PROCESS AUDIO 
                # ============================================= 

                if audio_value is not None: 

                    st.audio( 
                        audio_value 
                    ) 

                    st.success( 
                        "Audio recorded successfully." 
                    ) 

                    if st.button( 
                        "📝 Convert Speech to Text", 
                        use_container_width=True, 
                        key=( 
                            f"transcribe_" 
                            f"{current_index}" 
                        ) 
                    ): 

                        with st.spinner( 
                            "Converting your speech to text..." 
                        ): 

                            try: 

                                audio_bytes = ( 
                                    audio_value 
                                    .getvalue() 
                                ) 

                                transcription = ( 
                                    groq_client 
                                    .audio 
                                    .transcriptions 
                                    .create( 
                                        file=( 
                                            "answer.wav", 
                                            audio_bytes 
                                        ), 
                                        model=( 
                                            "whisper-large-v3-turbo" 
                                        ), 
                                        language="en", 
                                        temperature=0 
                                    ) 
                                ) 

                                transcript = ( 
                                    transcription.text 
                                ) 

                                if not transcript.strip(): 

                                    st.warning( 
                                        "No speech was detected. " 
                                        "Please record your answer again." 
                                    ) 

                                else: 

                                    st.session_state[ 
                                        "current_transcript" 
                                    ] = transcript 

                                    st.success( 
                                        "Speech converted " 
                                        "successfully!" 
                                    ) 

                            except Exception as e: 

                                st.error( 
                                    "Speech-to-text error: " 
                                    f"{e}" 
                                ) 

                # ============================================= 
                # SHOW TRANSCRIPT 
                # ============================================= 

                current_transcript = ( 
                    st.session_state.get( 
                        "current_transcript", 
                        "" 
                    ) 
                ) 

                if current_transcript: 

                    st.subheader( 
                        "📝 Your Answer" 
                    ) 

                    st.text_area( 
                        "Speech-to-Text Result", 
                        current_transcript, 
                        height=180, 
                        key=( 
                            f"transcript_display_" 
                            f"{current_index}" 
                        ) 
                    ) 

                    st.info( 
                        "Review your answer above before " 
                        "submitting it for AI evaluation." 
                    ) 

                    # ========================================= 
                    # EVALUATE ANSWER 
                    # ========================================= 

                    if st.button( 
                        "🤖 Evaluate My Answer", 
                        use_container_width=True, 
                        key=( 
                            f"evaluate_" 
                            f"{current_index}" 
                        ) 
                    ): 

                        with st.spinner( 
                            "AI is evaluating your answer..." 
                        ): 

                            try: 

                                evaluation_prompt = f""" 
You are an expert recruitment interviewer. 

Evaluate the candidate's answer to the interview question. 

JOB: 
{job_information} 

QUESTION: 
{current_question} 

CANDIDATE ANSWER: 
{current_transcript} 

Evaluate ONLY the candidate's actual answer. 

Consider: 

1. Technical correctness 
2. Relevance 
3. Completeness 
4. Clarity 
5. Practical knowledge 

Be objective and do not give a high score unless the answer 
actually demonstrates the required knowledge. 

Return EXACTLY this format: 

SCORE: <number from 0 to 100> 

TECHNICAL SCORE: <number from 0 to 100> 

RELEVANCE SCORE: <number from 0 to 100> 

CLARITY SCORE: <number from 0 to 100> 

FEEDBACK: 
<2-3 sentences specifically about this answer> 

STRENGTHS: 
- <specific strength from the answer> 
- <specific strength from the answer> 

IMPROVEMENT: 
<one specific improvement for this answer> 
""" 

                                evaluation_completion = ( 
                                    groq_client 
                                    .chat 
                                    .completions 
                                    .create( 
                                        model=( 
                                            "openai/gpt-oss-20b" 
                                        ), 
                                        messages=[ 
                                            { 
                                                "role": "system", 
                                                "content": ( 
                                                    "You are an " 
                                                    "objective " 
                                                    "technical " 
                                                    "interviewer." 
                                                ) 
                                            }, 
                                            { 
                                                "role": "user", 
                                                "content": ( 
                                                    evaluation_prompt 
                                                ) 
                                            } 
                                        ], 
                                        temperature=0.2 
                                    ) 
                                ) 

                                evaluation_text = ( 
                                    evaluation_completion 
                                    .choices[0] 
                                    .message 
                                    .content 
                                ) 

                                # ================================= 
                                # EXTRACT SCORE 
                                # ================================= 

                                score = 0 

                                for line in ( 
                                    evaluation_text 
                                    .splitlines() 
                                ): 

                                    if ( 
                                        line 
                                        .strip() 
                                        .upper() 
                                        .startswith( 
                                            "SCORE:" 
                                        ) 
                                    ): 

                                        score_text = ( 
                                            line 
                                            .split( 
                                                ":", 
                                                1 
                                            )[1] 
                                            .strip() 
                                        ) 

                                        try: 

                                            score = float( 
                                                score_text 
                                                .replace( 
                                                    "%", 
                                                    "" 
                                                ) 
                                            ) 

                                        except: 

                                            score = 0 

                                        break 

                                score = max( 
                                    0, 
                                    min( 
                                        100, 
                                        score 
                                    ) 
                                ) 

                                # ================================= 
                                # STORE ANSWER 
                                # ================================= 

                                st.session_state.voice_answers.append( 
                                    { 
                                        "question": current_question, 
                                        "answer": current_transcript 
                                    } 
                                ) 

                                st.session_state.voice_scores.append( 
                                    score 
                                ) 

                                st.session_state.voice_evaluations.append( 
                                    evaluation_text 
                                ) 
                                # ================================= 
                                # SAVE INTERVIEW RESULT TO DATABASE 
                                # ================================= 

                                try: 
                                    save_response = requests.post( 
                                        f"{API_URL}/save-interview-result", 
                                        json={ 
                                            "candidate_id": st.session_state.get( 
                                            "candidate_id" 
                                            ), 
                                            "job_id": st.session_state.get( 
                                            "voice_job_id" 
                                            ), 
                                            "question": current_question, 
                                            "answer": current_transcript, 
                                            "score": score, 
                                            "feedback": evaluation_text 
                                        }, 
                                        timeout=10 
                                    ) 

                                    if save_response.status_code != 200: 
                                        st.warning( 
                                            f"Interview result save failed: " 
                                            f"{save_response.text}" 
                                        ) 

                                except Exception as e: 
                                    st.warning( 
                                        f"Could not save interview result: {e}" 
                                    ) 

                                # ================================= 
                                # CLEAR TRANSCRIPT 
                                # ================================= 

                                st.session_state[ 
                                    "current_transcript" 
                                ] = "" 

                                # ================================= 
                                # NEXT QUESTION 
                                # ================================= 

                                st.session_state.voice_question_index += 1 

                                # ================================= 
                                # FINISH INTERVIEW 
                                # ================================= 

                                if ( 
                                    st.session_state.voice_question_index 
                                    >= total_questions 
                                ): 

                                    st.session_state.voice_interview_finished = ( 
                                        True 
                                    ) 

                                st.rerun() 

                            except Exception as e: 

                                st.error( 
                                    "AI evaluation error: " 
                                    f"{e}" 
                                ) 

        # ==================================================== 
        # FINAL SCREENING RESULT 
        # ==================================================== 

        if st.session_state.voice_interview_finished: 

            st.divider() 

            st.title( 
                "🏆 Voice Screening Result" 
            ) 

            scores = ( 
                st.session_state.voice_scores 
            ) 

            answers = ( 
                st.session_state.voice_answers 
            ) 

            evaluations = ( 
                st.session_state.voice_evaluations 
            ) 

            # ================================================= 
            # CALCULATE FINAL SCORE 
            # ================================================= 

            if scores: 

                final_score = ( 
                    sum(scores) 
                    / len(scores) 
                ) 

            else: 

                final_score = 0 
            st.session_state.voice_final_score = final_score 

            # ================================================= 
            # STAGE 1 - STORE FINAL SCORE 
            # ================================================= 

            st.session_state.voice_final_score = final_score 

            # ================================================= 
            # GENERATE OVERALL AI ANALYSIS 
            # ================================================= 

            if ( 
                st.session_state.voice_overall_analysis 
                is None 
                and evaluations 
            ): 

                try: 

                    evaluation_summary = "" 

                    for i, evaluation in enumerate( 
                        evaluations 
                    ): 

                        parsed = parse_voice_evaluation( 
                            evaluation 
                        ) 

                        evaluation_summary += f""" 
Question {i + 1} 
Score: {scores[i]:.0f}% 

Feedback: 
{parsed["feedback"]} 

Strengths: 
{", ".join(parsed["strengths"])} 

Improvement: 
{parsed["improvement"]} 

""" 

                    overall_prompt = f""" 
You are a senior recruitment evaluator. 

Analyze the candidate's complete voice interview. 

JOB: 
{job_information} 

FINAL SCORE: 
{final_score:.1f}% 

QUESTION-WISE EVALUATION: 
{evaluation_summary} 

Provide an overall assessment. 

Use EXACTLY this format: 

RECOMMENDATION: 
<one of: Strong Candidate, Suitable Candidate, Needs Further Review, Weak Candidate> 

FEEDBACK: 
<2-3 sentences summarizing the candidate's overall performance> 

STRENGTHS: 
- <strength 1> 
- <strength 2> 
- <strength 3> 

IMPROVEMENT: 
<one or two specific areas the candidate should improve> 
""" 

                    overall_completion = ( 
                        groq_client 
                        .chat 
                        .completions 
                        .create( 
                            model=( 
                                "openai/gpt-oss-20b" 
                            ), 
                            messages=[ 
                                { 
                                    "role": "system", 
                                    "content": ( 
                                        "You are a senior " 
                                        "recruitment evaluator." 
                                    ) 
                                }, 
                                { 
                                    "role": "user", 
                                    "content": overall_prompt 
                                } 
                            ], 
                            temperature=0.2 
                        ) 
                    ) 

                    overall_text = ( 
                        overall_completion 
                        .choices[0] 
                        .message 
                        .content 
                    ) 

                    st.session_state.voice_overall_analysis = ( 
                        overall_text 
                    ) 

                except Exception as e: 

                    st.warning( 
                        "Unable to generate overall AI analysis. " 
                        "Using score-based recommendation." 
                    ) 

                    st.session_state.voice_overall_analysis = ( 
                        "" 
                    ) 

            # ================================================= 
            # FINAL RESULT 
            # ================================================= 

            st.metric( 
                "🎯 Final Voice Screening Score", 
                f"{final_score:.1f}%" 
            ) 

            # ================================================= 
            # PARSE OVERALL ANALYSIS 
            # ================================================= 

            overall_text = ( 
                st.session_state.voice_overall_analysis 
                or "" 
            ) 

            overall_recommendation = "" 

            overall_feedback = "" 

            overall_strengths = [] 

            overall_improvement = "" 

            if overall_text: 

                lines = overall_text.splitlines() 

                current_section = None 

                for raw_line in lines: 

                    line = raw_line.strip() 

                    if not line: 
                        continue 

                    upper_line = line.upper() 

                    # ----------------------------------------- 
                    # RECOMMENDATION 
                    # ----------------------------------------- 

                    if upper_line.startswith( 
                        "RECOMMENDATION:" 
                    ): 

                        current_section = "recommendation" 

                        overall_recommendation = ( 
                            line 
                            .split( 
                                ":", 
                                1 
                            )[1] 
                            .strip() 
                        ) 

                        continue 

                    # ----------------------------------------- 
                    # FEEDBACK 
                    # ----------------------------------------- 

                    if upper_line.startswith( 
                        "FEEDBACK:" 
                    ): 

                        current_section = "feedback" 

                        overall_feedback = ( 
                            line 
                            .split( 
                                ":", 
                                1 
                            )[1] 
                            .strip() 
                        ) 

                        continue 

                    # ----------------------------------------- 
                    # STRENGTHS 
                    # ----------------------------------------- 

                    if upper_line.startswith( 
                        "STRENGTHS:" 
                    ): 

                        current_section = "strengths" 

                        continue 

                    # ----------------------------------------- 
                    # IMPROVEMENT 
                    # ----------------------------------------- 

                    if upper_line.startswith( 
                        "IMPROVEMENT:" 
                    ): 

                        current_section = "improvement" 

                        overall_improvement = ( 
                            line 
                            .split( 
                                ":", 
                                1 
                            )[1] 
                            .strip() 
                        ) 

                        continue 

                    # ----------------------------------------- 
                    # CONTINUE FEEDBACK 
                    # ----------------------------------------- 

                    if current_section == "feedback": 

                        overall_feedback += ( 
                            " " + line 
                        ) 

                    # ----------------------------------------- 
                    # CONTINUE STRENGTHS 
                    # ----------------------------------------- 

                    elif current_section == "strengths": 

                        if line.startswith("-"): 

                            overall_strengths.append( 
                                line.lstrip("- ").strip() 
                            ) 

                    # ----------------------------------------- 
                    # CONTINUE IMPROVEMENT 
                    # ----------------------------------------- 

                    elif current_section == "improvement": 

                        overall_improvement += ( 
                            " " + line 
                        ) 

            # ================================================= 
            # FALLBACK RECOMMENDATION 
            # ================================================= 

            if not overall_recommendation: 

                if final_score >= 80: 

                    overall_recommendation = ( 
                        "Strong Candidate" 
                    ) 

                elif final_score >= 65: 

                    overall_recommendation = ( 
                        "Suitable Candidate" 
                    ) 

                elif final_score >= 50: 

                    overall_recommendation = ( 
                        "Needs Further Review" 
                    ) 

                else: 

                    overall_recommendation = ( 
                        "Weak Candidate" 
                    ) 

            # ================================================= 
            # STAGE 1 - STORE OVERALL RESULT 
            # ================================================= 

            st.session_state.voice_recommendation = ( 
                overall_recommendation 
            ) 

            st.session_state.voice_overall_feedback = ( 
                overall_feedback 
            ) 

            st.session_state.voice_overall_strengths = ( 
                overall_strengths 
            ) 

            st.session_state.voice_overall_improvement = ( 
                overall_improvement 
            ) 
            #=================================================  
            # SAVE SCREENING SUMMARY TO DATABASE  
            # =================================================  

            if (  
                "voice_summary_saved" not in st.session_state  
                or not st.session_state.voice_summary_saved  
            ):  

                try:  

                    candidate_id = selected_candidate.get("id")  

                    if candidate_id is None:  

                        st.warning(  
                            "Candidate ID not found. "  
                            "Screening result could not be saved."  
                        )  

                    else:  

                        summary_payload = {  

                            "candidate_id": int(candidate_id),  

                            "overall_score": float(  
                                final_score  
                            ),  

                            "recommendation": (  
                                overall_recommendation  
                            ),  

                            "strengths": "\n".join(  
                                overall_strengths  
                            )  
                            if overall_strengths  
                            else "",  

                            "improvement": (  
                                overall_improvement  
                            )  
                        }  

                        save_response = requests.post(  
                            f"{API_URL}/save-screening-summary",  
                            json=summary_payload,  
                            timeout=10  
                        )  

                        if save_response.status_code in [200, 201]:  

                            st.session_state.voice_summary_saved = True  

                            st.success(  
                                "✅ Interview performance saved successfully."  
                            )  

                        else:  

                            st.error(  
                                "Unable to save interview performance."  
                            )  

                            st.write(  
                                save_response.text  
                            )  

                except Exception as e:  

                    st.error(  
                        f"Error saving interview performance: {e}"  
                    )  



            # ================================================= 
            # AI RECOMMENDATION 
            # ================================================= 

            st.subheader( 
                "🤖 AI Recommendation" 
            ) 

            if "Strong" in overall_recommendation: 

                st.success( 
                    f"🌟 {overall_recommendation}" 
                ) 

            elif "Suitable" in overall_recommendation: 

                st.success( 
                    f"✅ {overall_recommendation}" 
                ) 

            elif "Review" in overall_recommendation: 

                st.warning( 
                    f"⚠️ {overall_recommendation}" 
                ) 

            else: 

                st.error( 
                    f"❌ {overall_recommendation}" 
                ) 

            # ================================================= 
            # SUMMARY 
            # ================================================= 

            result_col1, result_col2, result_col3 = ( 
                st.columns(3) 
            ) 

            with result_col1: 

                st.metric( 
                    "Questions", 
                    len( 
                        st.session_state.voice_questions 
                    ) 
                ) 

            with result_col2: 

                st.metric( 
                    "Answered", 
                    len(answers) 
                ) 

            with result_col3: 

                st.metric( 
                    "Average Score", 
                    f"{final_score:.1f}%" 
                ) 

            # ================================================= 
            # OVERALL FEEDBACK 
            # ================================================= 

            if overall_feedback: 

                st.divider() 

                st.subheader( 
                    "💬 Overall Feedback" 
                ) 

                st.info( 
                    overall_feedback 
                ) 

            # ================================================= 
            # OVERALL STRENGTHS 
            # ================================================= 

            if overall_strengths: 
                st.subheader("💪 Overall Strengths") 
                st.success(overall_strengths) 

            # ================================================= 
            # OVERALL IMPROVEMENT 
            # ================================================= 

            if overall_improvement: 

                st.subheader( 
                    "📈 Overall Improvement" 
                ) 

                st.warning( 
                    overall_improvement 
                ) 

            # ================================================= 
            # QUESTION-WISE RESULTS 
            # ================================================= 

            st.divider() 

            st.subheader( 
                "📋 Question-wise Evaluation" 
            ) 

            for index, answer_data in enumerate( 
                answers 
            ): 

                question_score = ( 
                    scores[index] 
                    if index < len(scores) 
                    else 0 
                ) 

                with st.expander( 
                    f"Question {index + 1} " 
                    f"— Score: " 
                    f"{question_score:.0f}%" 
                ): 

                    # ========================================= 
                    # QUESTION 
                    # ========================================= 

                    st.markdown( 
                        "**Question:**" 
                    ) 

                    st.write( 
                        answer_data[ 
                            "question" 
                        ] 
                    ) 

                    # ========================================= 
                    # ANSWER 
                    # ========================================= 

                    st.markdown( 
                        "**Candidate's Answer:**" 
                    ) 

                    st.write( 
                        answer_data[ 
                            "answer" 
                        ] 
                    ) 

                    # ========================================= 
                    # AI EVALUATION 
                    # ========================================= 

                    if index < len(evaluations): 

                        evaluation_text = ( 
                            evaluations[index] 
                        ) 

                        parsed_evaluation = ( 
                            parse_voice_evaluation( 
                                evaluation_text 
                            ) 
                        ) 

                        feedback = ( 
                            parsed_evaluation[ 
                                "feedback" 
                            ] 
                        ) 

                        strengths = ( 
                            parsed_evaluation[ 
                                "strengths" 
                            ] 
                        ) 

                        improvement = ( 
                            parsed_evaluation[ 
                                "improvement" 
                            ] 
                        ) 

                        st.markdown( 
                            "### 🤖 AI Evaluation" 
                        ) 

                        # ------------------------------------- 
                        # FEEDBACK 
                        # ------------------------------------- 

                        st.markdown( 
                            "#### 💬 Feedback" 
                        ) 

                        if feedback: 

                            st.info( 
                                feedback 
                            ) 

                        else: 

                            st.write( 
                                "No feedback available." 
                            ) 

                        # ------------------------------------- 
                        # STRENGTHS 
                        # ------------------------------------- 

                        st.markdown( 
                            "#### 💪 Strengths" 
                        ) 

                        if strengths: 

                            for strength in strengths: 

                                st.success( 
                                    f"✓ {strength}" 
                                ) 

                        else: 

                            st.write( 
                                "No strengths identified." 
                            ) 

                        # ------------------------------------- 
                        # IMPROVEMENT 
                        # ------------------------------------- 

                        st.markdown( 
                            "#### 📈 Improvement" 
                        ) 

                        if improvement: 

                            st.warning( 
                                improvement 
                            ) 

                        else: 

                            st.write( 
                                "No improvement suggestions " 
                                "available." 
                            ) 

            # ================================================= 
            # STAGE 1 - STRUCTURED RESULT PREVIEW 
            # ================================================= 
            # This section confirms that all interview result 
            # information is available for Stage 2. 
            # ================================================= 

            st.divider() 

            with st.expander( 
                "📊 Interview Performance Data" 
            ): 

                st.write( 
                    "**Candidate:**", 
                    st.session_state.voice_candidate_name 
                ) 

                st.write( 
                    "**Job ID:**", 
                    st.session_state.voice_job_id 
                ) 

                st.write( 
                    "**Final Score:**", 
                    f"{st.session_state.voice_final_score:.1f}%" 
                ) 

                st.write( 
                    "**Recommendation:**", 
                    st.session_state.voice_recommendation 
                ) 

                st.write( 
                    "**Questions Answered:**", 
                    len( 
                        st.session_state.voice_answers 
                    ) 
                ) 

                st.write( 
                    "**Question Scores:**", 
                    st.session_state.voice_scores 
                ) 

                st.write( 
                    "**Overall Feedback:**", 
                    st.session_state.voice_overall_feedback 
                ) 

                if st.session_state.voice_overall_strengths: 

                    st.write( 
                        "**Overall Strengths:**" 
                    ) 

                    for strength in ( 
                        st.session_state.voice_overall_strengths 
                    ): 

                        st.write( 
                            f"✓ {strength}" 
                        ) 

                st.write( 
                    "**Overall Improvement:**", 
                    st.session_state.voice_overall_improvement 
                ) 

            # ================================================= 
            # RESTART INTERVIEW 
            # ================================================= 

            st.divider() 

            if st.button( 
                "🔄 Start New Voice Interview", 
                use_container_width=True, 
                key="restart_voice_interview" 
            ): 

                st.session_state.voice_questions = [] 

                st.session_state.voice_question_index = 0 

                st.session_state.voice_answers = [] 

                st.session_state.voice_scores = [] 

                st.session_state.voice_evaluations = [] 

                st.session_state.voice_interview_started = False 

                st.session_state.voice_interview_finished = False 

                st.session_state.voice_candidate_name = "" 

                st.session_state.voice_job_id = None 

                st.session_state.voice_overall_analysis = None 

                # Stage 1 result reset 

                st.session_state.voice_final_score = 0.0 

                st.session_state.voice_recommendation = "" 

                st.session_state.voice_overall_feedback = "" 

                st.session_state.voice_overall_strengths = [] 

                st.session_state.voice_overall_improvement = "" 

                st.session_state[ 
                    "current_transcript" 
                ] = "" 

                st.rerun() 

    except Exception as e: 

        st.error( 
            f"Voice-Based Screening error: {e}" 
        ) 
# ============================================================ 
# FOOTER 
# ============================================================ 



st.markdown("---") 





st.caption( 

    "AI Recruitment & Talent Management Copilot | Infosys Springboard Project" 
)