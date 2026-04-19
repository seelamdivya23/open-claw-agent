def analyze_resume_prompt(resume_text, job_desc):
    return f"""
    Compare the resume with job description.

    Resume:
    {resume_text}

    Job Description:
    {job_desc}

    Give:
    - Matching score (0-100)
    - Skills matched
    - Missing skills
    """
