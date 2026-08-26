import json
from database.database import get_connection


# -----------------------------------------
# Save Candidate
# -----------------------------------------
def save_candidate(candidate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            name,
            email,
            phone,
            skills,
            education,
            experience,
            resume_text,
            match_score,
            ats_score,
            compatibility_score,
            hiring_score,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate["name"],
        candidate["email"],
        candidate["phone"],
        json.dumps(candidate["skills"]),
        json.dumps(candidate["education"]),
        json.dumps(candidate["experience"]),
        candidate.get("resume_text", ""),
        candidate.get("match_score", 0),
        candidate.get("ats_score", 0),
        candidate.get("compatibility_score", 0),
        candidate.get("hiring_score", 0),
        candidate.get("status", "Pending")
    ))

    conn.commit()
    conn.close()


# -----------------------------------------
# Get All Candidates
# -----------------------------------------
def get_all_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")

    rows = cursor.fetchall()

    conn.close()

    candidates = []

    for row in rows:
        candidates.append(dict(row))

    return candidates


# -----------------------------------------
# Update Candidate Status
# -----------------------------------------
def update_candidate_status(candidate_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE candidates
        SET status = ?
        WHERE id = ?
    """, (
        status,
        candidate_id
    ))

    conn.commit()
    conn.close()


# -----------------------------------------
# Update Candidate Scores
# -----------------------------------------
def update_candidate_scores(
    candidate_id,
    match_score,
    compatibility_score,
    ats_score,
    hiring_score
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE candidates
        SET
            match_score = ?,
            compatibility_score = ?,
            ats_score = ?,
            hiring_score = ?
        WHERE id = ?
    """, (
        match_score,
        compatibility_score,
        ats_score,
        hiring_score,
        candidate_id
    ))

    conn.commit()
    conn.close()
# -----------------------------------------
# Update Candidate Profile
# -----------------------------------------
def update_candidate_profile(
    candidate_id,
    name,
    email,
    phone,
    skills,
    education,
    experience
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE candidates
        SET
            name = ?,
            email = ?,
            phone = ?,
            skills = ?,
            education = ?,
            experience = ?
        WHERE id = ?
    """, (
        name,
        email,
        phone,
        json.dumps(skills),
        json.dumps(education),
        json.dumps(experience),
        candidate_id
    ))

    conn.commit()
    conn.close()