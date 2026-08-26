import json

from database.database import get_connection

# -----------------------------------------
# Save Job Description
# -----------------------------------------
def save_job_description(job):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO job_descriptions(
        job_title,
        company_name,
        location,
        salary,
        employment_type,
        experience,
        education,
        skills,
        responsibilities,
        job_description
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        job.get("job_title"),
        job.get("company_name"),
        job.get("location"),
        job.get("salary"),
        job.get("employment_type"),
        job.get("experience"),
        job.get("education"),
        json.dumps(job.get("skills", [])),
        json.dumps(job.get("responsibilities", [])),
        job.get("job_description")

    ))

    conn.commit()
    conn.close()


# -----------------------------------------
# Get All Job Descriptions
# -----------------------------------------
def get_all_job_descriptions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_descriptions")

    rows = cursor.fetchall()

    conn.close()

    jobs = []

    for row in rows:
        job = dict(row)
        job["skills"] = json.loads(job["skills"]) if job["skills"] else []
        job["responsibilities"] = json.loads(job["responsibilities"]) if job["responsibilities"] else []

        jobs.append(job)

    return jobs


# -----------------------------------------
# Get One Job Description
# -----------------------------------------
def get_job_by_id(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM job_descriptions WHERE id = ?",
        (job_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        job = dict(row)

        job["skills"] = json.loads(job["skills"]) if job["skills"] else []
        job["responsibilities"] = json.loads(job["responsibilities"]) if job["responsibilities"] else []

        return job

    return None
# -----------------------------------------
# Update Job Description
# -----------------------------------------
def update_job_description(job_id, job):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE job_descriptions
    SET
        job_title = ?,
        company_name = ?,
        location = ?,
        salary = ?,
        employment_type = ?,
        experience = ?,
        education = ?,
        skills = ?,
        responsibilities = ?,
        job_description = ?
    WHERE id = ?
    """, (

        job.get("job_title"),
        job.get("company_name"),
        job.get("location"),
        job.get("salary"),
        job.get("employment_type"),
        job.get("experience"),
        job.get("education"),
        json.dumps(job.get("skills", [])),
        json.dumps(job.get("responsibilities", [])),
        job.get("job_description"),
        job_id

    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


# -----------------------------------------
# Delete Job Description
# -----------------------------------------
def delete_job_description(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM job_descriptions WHERE id = ?",
        (job_id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted > 0
# =====================================================
# GET ALL JOBS
# =====================================================

def get_all_jobs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM job_descriptions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    jobs = []

    for row in rows:
        jobs.append(dict(row))

    return jobs