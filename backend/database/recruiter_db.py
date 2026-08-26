import json

from database.database import get_connection


# ----------------------------------------------------
# Get All Candidates
# ----------------------------------------------------
def get_all_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")

    rows = cursor.fetchall()

    conn.close()

    candidates = []

    for row in rows:

        candidate = {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "skills": json.loads(row["skills"]),
            "education": json.loads(row["education"]),
            "experience": json.loads(row["experience"]),
            "ats_score": row["ats_score"],
            "compatibility_score": row["compatibility_score"],
            "hiring_score": row["hiring_score"]
        }

        candidates.append(candidate)

    return candidates


# ----------------------------------------------------
# Delete Candidate
# ----------------------------------------------------
def delete_candidate(candidate_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM candidates WHERE id = ?",
        (candidate_id,)
    )

    conn.commit()
    conn.close()