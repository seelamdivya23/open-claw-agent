import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"


def ask_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60  # ✅ prevents hanging
        )

        data = response.json()

        # ✅ Debug if needed
        # print("LLM RAW:", data)

        if "response" in data:
            text = data["response"].strip()

            # ✅ CLEAN OUTPUT (VERY IMPORTANT)
            text = text.replace("\n\n", "\n")

            return text

        else:
            print("LLM ERROR:", data)
            return fallback_response(prompt)

    except Exception as e:
        print("LLM Exception:", e)
        return fallback_response(prompt)


# ✅ SMART FALLBACK
def fallback_response(prompt):
    if "job role" in prompt.lower():
        return "Software Engineer"

    if "job description" in prompt.lower():
        return "We are hiring a Software Engineer with relevant skills."

    if "email" in prompt.lower():
        return "Dear Candidate, we are interested in your profile."

    return "Unable to process request"
