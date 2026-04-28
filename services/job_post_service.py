from services.llm_service import ask_llm

# 🔹 Recruiter Job Post (formal, detailed)
def generate_recruiter_job_post(job_desc):
    prompt = f"""
    Create a professional job description for recruiters to post on job portals.

    Role: {job_desc}

    Include:
    - Job title
    - Responsibilities
    - Required skills
    - Experience
    """

    return ask_llm(prompt)


# 🔹 Candidate Job Post (simple, readable)
def generate_candidate_job_post(job_desc):
    prompt = f"""
    Create a simple and attractive job description for a candidate.

    Role: {job_desc}

    Keep it short and easy to understand.
    """

    return ask_llm(prompt)