import os
import re
from services.llm_service import ask_llm


# ---------------- TEXT EXTRACTION (UNCHANGED) ----------------
def extract_text(file_path):
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif file_path.endswith(".pdf"):
            import PyPDF2
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text

        elif file_path.endswith(".docx"):
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])

        else:
            return ""

    except Exception as e:
        print("Error reading file:", e)
        return ""


# ---------------- ROLE EXTRACTION (UNCHANGED AS YOU REQUESTED) ----------------
def extract_job_role_llm(text):
    try:
        prompt = f"""
Extract ONLY the job role from this resume.

RULES:
- Only job title
- Max 3 words
- No explanation
- No extra text

Resume:
{text}
"""

        response = ask_llm(prompt)

        if not response:
            return "Python Developer"

        role = response.strip().split("\n")[0]

        # remove garbage words
        bad_words = [
            "extract", "resume", "job", "role", "title",
            "candidate", "based", "analysis", "the"
        ]

        role = role.lower()

        for w in bad_words:
            role = role.replace(w, "")

        role = role.replace(".", "").replace(":", "").replace("-", "")
        role = " ".join(role.split())

        role = " ".join(role.split()[:3])

        if len(role.strip()) < 3:
            return "Python Developer"

        return role.title()

    except Exception as e:
        print("Role extraction error:", e)
        return "Python Developer"


# ---------------- SKILLS EXTRACTION (🔥 FIXED VERSION) ----------------
def extract_skills_llm(text):
    try:
        prompt = f"""
Extract technical skills from resume.

RULES:
- Return ONLY comma separated skills
- No explanation
- No sentences

Example:
Python, SQL, Flask, Machine Learning

Resume:
{text}
"""

        response = ask_llm(prompt)

        if not response:
            return []

        # 🔥 CLEAN TEXT FIRST
        response = response.replace("\n", " ").lower()

        # 🔥 EXTRACT WORDS MORE INTELLIGENTLY
        raw_skills = re.split(r",|\|", response)

        clean_skills = []

        for skill in raw_skills:
            skill = skill.strip()

            # remove garbage words
            if (
                len(skill) > 1
                and not any(x in skill for x in ["resume", "skills", "experience", "based"])
            ):
                clean_skills.append(skill)

        # remove duplicates while preserving order
        final_skills = list(dict.fromkeys(clean_skills))

        return final_skills[:10]

    except Exception as e:
        print("Skill extraction error:", e)
        return []
