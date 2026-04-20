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


# ---------------- ROLE EXTRACTION (STRONG FIX) ----------------
def extract_job_role_llm(text):
    try:
        prompt = f"""
        Extract the BEST job role from this resume.

        STRICT RULES:
        - Only return job title
        - Max 3 words
        - No explanation
        - No punctuation
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
            return "Python Developer"

        # ✅ CLEAN OUTPUT HARD FILTER
        role = response.strip().split("\n")[0]

        # remove unwanted words
        unwanted = [
            "based", "resume", "candidate", "job",
            "role", "is", "the", "best", "from",
            "this", "only", "title"
        ]

        role = role.lower()

        for word in unwanted:
            role = role.replace(word, "")

        # remove symbols
        for ch in [".", ":", "-", "_", "|"]:
            role = role.replace(ch, "")

        role = " ".join(role.split())

        # keep only first 3 words
        role = " ".join(role.split()[:3])

        # ✅ fallback safety
        if len(role) < 3:
            return "Python Developer"

        return role.title()

    except Exception as e:
        print("LLM role extraction error:", e)
        return "Python Developer"


# ---------------- SKILLS EXTRACTION (IMPROVED) ----------------
def extract_skills_llm(text):
    try:
        prompt = f"""
        Extract important technical skills from this resume.

        RULES:
        - Only skills
        - Comma separated
        - No explanation

        Example:
        Python, SQL, Machine Learning, Flask

        Resume:
        {text}
        """

        response = ask_llm(prompt)

        if not response:
            return []

        # ✅ CLEAN OUTPUT
        skills = response.replace("\n", "").split(",")

        clean_skills = []
        for s in skills:
            s = s.strip().lower()

            # remove noise words
            if len(s) > 1 and not any(x in s for x in ["resume", "skills", "based"]):
                clean_skills.append(s)

        return clean_skills[:10]  # limit

    except Exception as e:
        print("Skill extraction error:", e)
        return []
