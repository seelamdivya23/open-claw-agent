from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import TELEGRAM_TOKEN

from agents.recruiter_agent import (
    find_candidates,
    generate_daily_summary
)

from agents.candidate_agent import (
    find_jobs_for_candidate,
    apply_to_jobs,
    get_daily_candidate_summary
)

from services.resume_parser import extract_text

from services.email_service import (
    generate_candidate_application_email,
    generate_recruiter_followup_email,
    send_email
)

from services.job_post_service import generate_recruiter_job_post


import os
import time


# ---------------- SPLIT MESSAGE ----------------
async def send_long_message(update, text):
    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i+4000])


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Recruiter Bot Ready!\n\n"
        "/recruit <job desc> - Recruiter pipeline\n"
        "/jobs - Candidate job search + email draft\n"
        "/summary - Candidate daily summary\n"
    )


# ---------------- RECRUITER FLOW ----------------
async def recruit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        job_desc = " ".join(context.args)

        if not job_desc:
            return await update.message.reply_text("❗ Provide job description")

        await update.message.reply_text("🤖 Running Full AI Recruiter Pipeline...")

        # STEP 1: Find candidates
        results = find_candidates(job_desc)

        # STEP 2: Post job (internal board)
        job_post = generate_recruiter_job_post(job_desc)

        # STEP 3: Prepare response
        response = f"""
📌 FULL AI RECRUITER PIPELINE REPORT
----------------------------------------

🧾 JOB DESCRIPTION:
{job_desc}

📢 JOB POSTED (FREE INTERNAL BOARD):
{job_post}

----------------------------------------
👥 CANDIDATE SCREENING RESULTS:
"""

        # STEP 4: Process candidates
        for r in results:

            skills = ", ".join(r["skills"]) if r["skills"] else "Not detected"

            email = generate_recruiter_followup_email(
                r["name"],
                job_desc,
                skills
            )

            # send email
            send_email(
                to_email="divyaseelam83@gmail.com",
                subject="Interview Opportunity",
                body=email
            )

            response += f"""
👤 Candidate: {r['name']}
⭐ Score: {r['score']}
🛠 Skills: {skills}

📧 Follow-up Email Sent:
{email}

----------------------------------------
"""

        # STEP 5: Sort + Daily Summary
        results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)

        summary = "📊 DAILY SUMMARY (BEST → WORST):\n"

        for r in results_sorted:
            summary += f"\n{r['name']} - Score: {r['score']}"

        response += "\n" + summary

        await send_long_message(update, response)

    except Exception as e:
        print("Recruit error:", e)
        await update.message.reply_text("❌ Error in recruit")


# ---------------- JOBS (CANDIDATE FLOW) ----------------
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resume_text = extract_text("data/resumes/resume1.txt")

        jobs_list = find_jobs_for_candidate(resume_text)

        if not jobs_list:
            return await update.message.reply_text("❌ No jobs found")

        response = "💼 JOB MATCHES:\n\n"

        # apply jobs (simulation)
        applied_jobs = apply_to_jobs(jobs_list[:3])

        for job in applied_jobs:

            email_text = generate_candidate_application_email(
                "Candidate",
                job["title"],
                job["company"]
            )

            response += f"""
🏢 {job['title']} - {job['company']}
⭐ Match Score: {job['score']}%
🔗 {job['url']}

📧 Email Draft:
{email_text}

---------------------
"""

        await send_long_message(update, response)

    except Exception as e:
        print("Jobs error:", e)
        await update.message.reply_text("❌ Error in jobs")






# ---------------- RESUME UPLOAD ----------------
async def upload_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        doc = update.message.document

        if not doc:
            return await update.message.reply_text("❌ Upload file")

        file = await doc.get_file()

        os.makedirs("data/resumes", exist_ok=True)

        path = f"data/resumes/{doc.file_name}"
        await file.download_to_drive(path)

        await update.message.reply_text("✅ Resume uploaded")

        resume_text = extract_text(path)

        jobs_list = find_jobs_for_candidate(resume_text)

        response = "💼 JOB MATCHES:\n\n"

        for job in jobs_list[:3]:
            response += f"""
🏢 {job['title']} - {job['company']}
⭐ Match Score: {job['score']}%
🔗 {job.get('url', 'No link available')}
---------------------
"""

        await send_long_message(update, response)

    except Exception as e:
        print("Upload error:", e)
        await update.message.reply_text("❌ Error")


# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("recruit", recruit))
    app.add_handler(CommandHandler("jobs", jobs))
    app.add_handler(MessageHandler(filters.Document.ALL, upload_resume))

    print("🚀 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()