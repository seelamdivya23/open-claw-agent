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
