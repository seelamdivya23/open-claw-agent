import requests
from config import OPENAI_API_KEY

def ask_llm(prompt):
    try:
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # DEBUG (optional)
        # print(result)

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("LLM Error:", e)
        return fallback_response(prompt)


# ✅ FALLBACK (if API fails)
def fallback_response(prompt):
    prompt = prompt.lower()

    if "job role" in prompt:
        return "Python Developer"

    if "skills" in prompt:
        return "python, sql, machine learning"

    if "email" in prompt:
        return "Dear Hiring Manager, I am interested in this role."

    return "Python Developer"
