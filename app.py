from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import TELEGRAM_TOKEN

from agents.recruiter_agent import find_candidates
from agents.candidate_agent import find_jobs_for_candidate

from services.resume_parser import extract_text
from services.email_service import generate_email
from services.job_post_service import generate_recruiter_job_post

import os
import time


# ---------------- SPLIT LONG MESSAGE ----------------
async def send_long_message(update, text):
    max_length = 4000
    for i in range(0, len(text), max_length):
        await update.message.reply_text(text[i:i+max_length])


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Recruiter Bot Ready!\n\n"
        "📌 Commands:\n"
        "/recruit <job description> - Find candidates\n"
        "/jobs - Get job matches\n\n"
        "📄 Or upload your resume (PDF/TXT/DOCX)"
    )


# ---------------- RECRUITER MODE ----------------
async def recruit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        job_desc = " ".join(context.args)

        if not job_desc:
            await update.message.reply_text("❗ Provide job description")
            return

        results = find_candidates(job_desc)

        response = "📊 Top Candidates:\n\n"

        for r in results[:5]:
            skills = ", ".join(r["skills"]) if r["skills"] else "Not detected"

            response += f"👤 {r['name']}\n"
            response += f"⭐ Score: {r['score']}%\n"
            response += f"🛠 Skills: {skills}\n\n"

        job_post = generate_recruiter_job_post(job_desc)

        response += "📢 Job Post:\n"
        response += job_post

        await send_long_message(update, response)

    except Exception as e:
        print("Error in recruit:", e)
        await update.message.reply_text("❌ Error in recruit")


# ---------------- JOBS COMMAND ----------------
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Jobs command received")

        resume_text = extract_text("data/resumes/resume1.txt")

        jobs_list = find_jobs_for_candidate(resume_text)

        if not jobs_list:
            await update.message.reply_text("❌ No jobs found")
            return

        response = "💼 Job Matches:\n\n"

        for job in jobs_list[:3]:
            response += f"🏢 {job['title']} - {job['company']}\n"
            response += f"🔗 {job['url']}\n"
            response += f"⭐ Match: {job['score']}%\n\n"

        await send_long_message(update, response)

        # ✅ Email Draft
        top_job = jobs_list[0]

        email_text = generate_email(
            "Divya Seelam",
            top_job["title"],
            top_job["company"]
        )

        await update.message.reply_text("✉️ Email Draft:")
        await send_long_message(update, email_text)

    except Exception as e:
        print("Error in jobs:", e)
        await update.message.reply_text("❌ Error in jobs")


# ---------------- RESUME UPLOAD ----------------
async def upload_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        document = update.message.document

        if document is None:
            await update.message.reply_text("❌ Please upload a file")
            return

        file_name = document.file_name

        if not file_name.endswith((".txt", ".pdf", ".docx")):
            await update.message.reply_text("❌ Only TXT, PDF, DOCX supported")
            return

        file = await document.get_file()

        os.makedirs("data/resumes", exist_ok=True)

        filename = f"{int(time.time())}_{file_name}"
        path = f"data/resumes/{filename}"

        await file.download_to_drive(path)

        await update.message.reply_text("✅ Resume uploaded successfully!")

        resume_text = extract_text(path)

        jobs_list = find_jobs_for_candidate(resume_text)

        if not jobs_list:
            await update.message.reply_text("❌ No jobs found")
            return

        response = "💼 Job Matches:\n\n"

        for job in jobs_list[:3]:
            response += f"🏢 {job['title']} - {job['company']}\n"
            response += f"🔗 {job['url']}\n"
            response += f"⭐ Match: {job['score']}%\n\n"

        await send_long_message(update, response)

        # ✅ Email Draft
        top_job = jobs_list[0]

        email_text = generate_email(
            "Divya Seelam",
            top_job["title"],
            top_job["company"]
        )

        await update.message.reply_text("✉️ Email Draft:")
        await send_long_message(update, email_text)

    except Exception as e:
        print("Error in upload:", e)
        await update.message.reply_text("❌ Error processing resume")


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
