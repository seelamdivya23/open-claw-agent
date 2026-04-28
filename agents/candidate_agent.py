from services.job_service import search_jobs
from services.resume_parser import extract_job_role_llm


def find_jobs_for_candidate(resume_text):

    role = extract_job_role_llm(resume_text)

    if not role or len(role) < 3:
        role = "python developer"

    query = role.lower().strip()

    print("FINAL QUERY:", query)

    jobs = search_jobs(query)

    print("Jobs from API:", jobs)

    matched_jobs = []

    for job in jobs:
        description = job.get("description", "").lower()

        score = 40
        if role in description:
            score = 80

        matched_jobs.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "score": score,
            "url": job.get("url")
        })

    matched_jobs.sort(key=lambda x: x["score"], reverse=True)

    return matched_jobs

# ---------------- APPLY TO JOBS ----------------
def apply_to_jobs(jobs):

    applied = []

    for job in jobs:

        applied.append({
            "title": job["title"],
            "company": job["company"],
            "url": job["url"],
            "score": job.get("score", 0)
        })

    return applied



# ---------------- DAILY SUMMARY ----------------
def get_daily_candidate_summary(jobs):

    summary = "📊 DAILY CANDIDATE REPORT\n\n"

    for job in jobs:

        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        score = job.get("score", 0)
    

        summary += f"""
🏢 {title} - {company}
⭐ Match Score: {score}%

------------------------
"""

    return summary