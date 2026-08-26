import sqlite3
import os

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = os.path.join(BASE_DIR, "recruitment.db")

print("Database Path:", DATABASE_NAME)

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Candidates Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT,
        resume_text TEXT,
        match_score REAL,
        ats_score REAL,
        compatibility_score REAL,
        hiring_score REAL,
        status TEXT
    )
    """)

    # -----------------------------
    # Job Descriptions Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        company_name TEXT,
        location TEXT,
        salary TEXT,
        employment_type TEXT,
        experience TEXT,
        education TEXT,
        skills TEXT,
        responsibilities TEXT,
        job_description TEXT
    )
    """)

    conn.commit()
    conn.close()
# -----------------------------
# Get Job by ID
# -----------------------------
def get_job_by_id(job_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM job_descriptions WHERE id = ?",
        (job_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None
# =====================================================
# Add candidate_id to existing users table
# =====================================================

def add_candidate_id_to_users():

    conn = get_connection()
    cursor = conn.cursor()

    # Check existing columns in users table
    cursor.execute("""
        PRAGMA table_info(users)
    """)

    columns = cursor.fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    # Add candidate_id only if it does not already exist
    if "candidate_id" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN candidate_id INTEGER
        """)

        conn.commit()

    conn.close()