from services.llm_service import ask_llm

def detect_job_role_llm(resume_text):
    prompt = f"""
    Analyze this resume and give ONLY ONE job role.

    Resume:
    {resume_text}

    Rules:
    - Only job title
    - Max 3 words
    - No explanation
    """

    role = ask_llm(prompt)

    # ✅ extra safety
    return role.split("\n")[0][:50]