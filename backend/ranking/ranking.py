from database.candidate_db import (
    get_all_candidates,
    update_candidate_scores,
    update_candidate_status
)

from matcher.matcher import match_resume_with_jd


def rank_candidates(job):
    """
    Compare all candidates with the Job Description
    and return ranked candidates.
    """

    candidates = get_all_candidates()

    ranked_candidates = []

    for candidate in candidates:

        result = match_resume_with_jd(
            candidate,
            job
        )

        match_score = result.get(
            "match_percentage",
            0
        )

        ats_score = min(
            match_score + 10,
            100
        )

        compatibility_score = (
            match_score * 0.7
            + ats_score * 0.3
        )

        hiring_score = (
            compatibility_score * 0.8
        )

        result["match_score"] = round(
            match_score,
            2
        )

        result["ats_score"] = round(
            ats_score,
            2
        )

        result["compatibility_score"] = round(
            compatibility_score,
            2
        )

        result["hiring_score"] = round(
            hiring_score,
            2
        )

        # Candidate Status
        if hiring_score >= 70:
            status = "Selected"

        elif hiring_score >= 50:
            status = "Shortlisted"

        else:
            status = "Rejected"

        result["status"] = status

        # Save scores
        update_candidate_scores(
            candidate["id"],
            result["match_score"],
            result["compatibility_score"],
            result["ats_score"],
            result["hiring_score"]
        )

        # Save status
        update_candidate_status(
            candidate["id"],
            status
        )

        ranked_candidates.append(result)

    ranked_candidates = sorted(
        ranked_candidates,
        key=lambda x: x["match_score"],
        reverse=True
    )

    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = index

    return ranked_candidates