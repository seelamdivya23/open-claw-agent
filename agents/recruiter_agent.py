from services.job_service import search_jobs
from services.resume_parser import extract_text
from services.email_service import generate_recruiter_followup_email
from services.llm_service import ask_llm

import os
import re




# ---------------- YOUR EXISTING FUNCTION (UNCHANGED) ----------------
def analyze_with_llm(resume_text, job_desc):

    prompt = f"""
You are an AI recruiter.

Compare resume with job description.

Return exactly:
Score: 0-100
Skills: comma separated

Resume:
{resume_text}

Job:
{job_desc}
"""

    response = ask_llm(prompt)

    score = 50
    skills = []

    if response:

        score_match = re.search(r"score\s*[:\-]?\s*(\d+)", response, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))

        skills_match = re.search(r"skills\s*[:\-]?\s*(.*)", response, re.IGNORECASE)
        if skills_match:
            skills = [s.strip() for s in skills_match.group(1).split(",")]

    return score, skills


# ---------------- STAGE 1: FIND + SCORE ----------------
def find_candidates(job_desc, resumes_folder="data/resumes"):

    results = []

    for file in os.listdir(resumes_folder):

        if not file.endswith((".txt", ".pdf", ".docx")):
            continue

        path = os.path.join(resumes_folder, file)
        text = extract_text(path)

        score, skills = analyze_with_llm(text, job_desc)

        results.append({
            "name": file,
            "score": score,
            "skills": skills,
            "resume_text": text
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# ---------------- STAGE 2: EMAIL FOLLOW-UP ----------------
def send_followup_emails(candidates, job_desc):

    messages = []

    for c in candidates[:5]:  # top 5 only

        prompt = f"""
You are a recruiter.

Ask 2 technical interview questions based on:

Job:
{job_desc}

Candidate Skills:
{c['skills']}

Return only questions.
"""

        questions = ask_llm(prompt)

        email = generate_recruiter_followup_email(
            c["name"],
            job_desc,
            c["skills"]
        )

        messages.append({
            "candidate": c["name"],
            "email": email,
            "questions": questions
        })

    return messages


# ---------------- STAGE 3: DAILY SUMMARY ----------------
def generate_daily_summary(candidates):

    summary = "📊 DAILY AI RECRUITER REPORT\n\n"

    for c in candidates:

        summary += f"""
👤 {c['name']}
⭐ Score: {c['score']}
🛠 Skills: {', '.join(c['skills'])}
------------------------
"""

    return summary


# ---------------- FULL PIPELINE (MAIN AGENT) ----------------
def run_recruiter_agent(job_desc):

    print("🚀 Starting AI Recruiter Agent...")

    # Step 1: Find candidates
    candidates = find_candidates(job_desc)

    # Step 2: Send emails
    emails = send_followup_emails(candidates, job_desc)

    # Step 3: Generate job post HERE (correct place)
    from services.job_post_service import generate_recruiter_job_post
    job_post = generate_recruiter_job_post(job_desc)

    # Step 4: Daily report
    report = generate_daily_summary(candidates)

    return {
        "candidates": candidates,
        "emails": emails,
        "report": report,
        "job_post": job_post
    }