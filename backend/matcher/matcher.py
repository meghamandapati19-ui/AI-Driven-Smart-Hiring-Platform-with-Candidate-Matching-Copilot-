import json

def match_resume_with_jd(candidate, job):

    candidate_skills = candidate.get("skills", [])
    job_skills = job.get("skills", [])

    # Convert JSON strings to Python lists
    if isinstance(candidate_skills, str):
        candidate_skills = json.loads(candidate_skills)

    if isinstance(job_skills, str):
        job_skills = json.loads(job_skills)

    candidate_skills = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    job_skills = {
        skill.lower().strip()
        for skill in job_skills
    }
    matched_skills = sorted(candidate_skills & job_skills)
    ats_score = 0
    if candidate.get("name"):
        ats_score += 10

    if candidate.get("email"):
        ats_score += 10

    if candidate.get("phone"):
        ats_score += 10

    if candidate.get("education"):
        ats_score += 20

    if candidate.get("experience"):
        ats_score += 20

    if candidate.get("skills"):
        ats_score += 30

    ats_score = min(ats_score, 100)

    missing_skills = sorted(job_skills - candidate_skills)

    extra_skills = sorted(candidate_skills - job_skills)
    if len(job_skills) > 0:
        match_percentage = round(
            (len(matched_skills) / len(job_skills)) * 100,
            2
        )
    else:
        match_percentage = 0

    compatibility_score = match_percentage
    hiring_score = round(
        (0.4 * ats_score) + (0.6 * compatibility_score),
        2
    )


    return {
        "candidate_name": candidate["name"],
        "job_title": job.get("job_title", "Not Available"),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "match_percentage": match_percentage,
        "compatibility_score": compatibility_score,
        "ats_score": ats_score,
        "hiring_score": hiring_score
}