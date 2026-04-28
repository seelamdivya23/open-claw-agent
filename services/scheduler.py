import schedule
import time
from agents.candidate_agent import find_jobs_for_candidate
from services.resume_parser import extract_text

def send_daily_jobs():
    print("Running daily job update...")

    resume_text = extract_text("data/resumes/resume1.txt")
    jobs = find_jobs_for_candidate(resume_text)

    for job in jobs[:3]:
        print(job["title"], "-", job["company"])

def start_scheduler():
    schedule.every().day.at("10:00").do(send_daily_jobs)

    while True:
        schedule.run_pending()
        time.sleep(60)