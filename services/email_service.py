import smtplib
from services.llm_service import ask_llm
from config import EMAIL, EMAIL_PASSWORD
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# ✅ UPDATED: Candidate sends email to recruiter
def generate_recruiter_followup_email(candidate_name, job_title, skills):

    prompt = f"""
You are a recruiter.

Write a professional follow-up email to a candidate.

Details:
Candidate Name: {candidate_name}
Job Role: {job_title}
Skills: {skills}

Include:
- Greeting
- Short intro
- Mention profile match
- Ask 2 technical interview questions
- Ask availability for interview
- Polite closing

Tone: professional, friendly

Return ONLY email content.
"""

    return ask_llm(prompt)


def generate_candidate_application_email(candidate_name, job_title, company):

    prompt = f"""
Write a job application email from candidate to recruiter.

Details:
Candidate Name: {candidate_name}
Job Title: {job_title}
Company: {company}

Include:
- Professional greeting
- Candidate is applying for job
- Mention interest in role
- Brief skills mention
- Request for interview consideration
- Polite closing

Tone: formal, professional

Return ONLY email content.
"""

    return ask_llm(prompt)


# (Keep this same if you want to send real emails later)
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)

        result = server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        if result == {}:
            print("✅ Email sent successfully")
        else:
            print("⚠️ Delivery issue:", result)

    except Exception as e:
        print("❌ Email error:", e)