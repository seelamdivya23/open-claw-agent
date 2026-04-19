import smtplib
from services.llm_service import ask_llm

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"


# ✅ UPDATED: Candidate sends email to recruiter
def generate_email(candidate_name, job_title, company):
    prompt = f"""
    Write a professional job application email.

    Candidate Name: {candidate_name}
    Job Title: {job_title}
    Company: {company}

    The email should:
    - Be short and professional
    - Candidate is applying for the job
    - Mention skills briefly
    - End politely

    Return only email content.
    """

    return ask_llm(prompt)


# (Keep this same if you want to send real emails later)
def send_email(to_email, subject, body):
    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, message)
    server.quit()
