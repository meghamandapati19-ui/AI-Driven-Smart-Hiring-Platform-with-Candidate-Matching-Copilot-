import sqlite3
from datetime import datetime

from database.database import get_connection


# =====================================================
# Create Applications Table
# =====================================================

def create_applications_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Applied',
            applied_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Apply for Job
# =====================================================

def apply_for_job(candidate_id, job_id):

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------------------------
    # Check whether candidate already applied
    # -------------------------------------------------

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE candidate_id = ?
        AND job_id = ?
    """, (
        candidate_id,
        job_id
    ))

    existing_application = cursor.fetchone()

    if existing_application:

        conn.close()

        return {
            "success": False,
            "message": "You have already applied for this job."
        }

    # -------------------------------------------------
    # Create application
    # -------------------------------------------------

    cursor.execute("""
        INSERT INTO applications (
            candidate_id,
            job_id,
            status,
            applied_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        job_id,
        "Applied",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    application_id = cursor.lastrowid

    conn.close()

    return {
        "success": True,
        "message": "Application submitted successfully.",
        "application_id": application_id
    }


# =====================================================
# Get Candidate Applications
# =====================================================

def get_candidate_applications(candidate_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            applications.id AS application_id,
            applications.candidate_id,
            applications.job_id,
            applications.status,
            applications.applied_at,

            job_descriptions.job_title,
            job_descriptions.company_name,
            job_descriptions.location,
            job_descriptions.salary,
            job_descriptions.employment_type,
            job_descriptions.experience,
            job_descriptions.education,
            job_descriptions.skills

        FROM applications

        INNER JOIN job_descriptions
        ON applications.job_id = job_descriptions.id

        WHERE applications.candidate_id = ?

        ORDER BY applications.id DESC
    """, (
        candidate_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    applications = []

    for row in rows:

        applications.append(dict(row))

    return applications


# =====================================================
# Check Application
# =====================================================

def has_applied(candidate_id, job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE candidate_id = ?
        AND job_id = ?
    """, (
        candidate_id,
        job_id
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None