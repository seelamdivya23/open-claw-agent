def score_candidate(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())

    match = resume_words.intersection(job_words)

    score = int((len(match) / len(job_words)) * 100) if job_words else 0

    return min(score, 100), list(match)