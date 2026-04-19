import os
from services.resume_parser import extract_text, extract_skills_llm
from services.llm_service import ask_llm


# ---------------- LLM SCORING ----------------
def analyze_with_llm(resume_text, job_desc):
    try:
        prompt = f"""
        Compare the resume with job description.

        Resume:
        {resume_text}

        Job:
        {job_desc}

        Return in this format:
        Score: <number>
        Skills: <comma separated>
        """

        response = ask_llm(prompt)

        score = 50
        skills = []

        if response:
            lines = response.split("\n")

            for line in lines:
                if "score" in line.lower():
                    try:
                        score = int(''.join(filter(str.isdigit, line)))
                    except:
                        score = 50

                if "skills" in line.lower():
                    skills = line.split(":")[-1].split(",")

        return score, [s.strip() for s in skills if s.strip()]

    except Exception as e:
        print("LLM error:", e)
        return 50, []


# ---------------- FIND CANDIDATES ----------------
def find_candidates(job_desc, resumes_folder="data/resumes"):
    results = []

    for file in os.listdir(resumes_folder):
        if not file.endswith((".txt", ".pdf", ".docx")):
            continue

        path = f"{resumes_folder}/{file}"
        text = extract_text(path)

        # ✅ LLM scoring
        score, skills = analyze_with_llm(text, job_desc)

        results.append({
            "name": file,
            "score": score,
            "skills": skills
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
