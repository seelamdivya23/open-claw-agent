import os
from services.llm_service import ask_llm

# ---------------- TEXT EXTRACTION ----------------
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


# ---------------- ROLE EXTRACTION (FIXED LLM) ----------------
def extract_job_role_llm(text):
    try:
        prompt = f"""
        Extract ONLY the job title from this resume.

        RULES:
        - Only 2 or 3 words
        - No explanation
        - No sentence

        Examples:
        Python Developer
        Data Scientist
        Backend Engineer

        Resume:
        {text}
        """

        response = ask_llm(prompt)

        if not response:
            return ""

        # ✅ CLEAN OUTPUT
        role = response.strip().split("\n")[0]

        for word in ["based", "resume", "candidate", "job", "role", "is"]:
            role = role.lower().replace(word, "")

        role = role.replace(".", "").replace(":", "").strip()

        role = " ".join(role.split()[:3])

        return role

    except Exception as e:
        print("LLM role extraction error:", e)
        return ""
# ---------------- SKILLS EXTRACTION (FOR RECRUITER MODE) ----------------
def extract_skills_llm(text):
    try:
        prompt = f"""
        Extract key technical skills from this resume.

        Resume:
        {text}

        Return ONLY skills separated by commas.
        Example:
        Python, SQL, Machine Learning, Flask
        """

        response = ask_llm(prompt)

        if not response:
            return []

        skills = response.split(",")

        return [s.strip() for s in skills if s.strip()]

    except Exception as e:
        print("Skill extraction error:", e)
        return []
