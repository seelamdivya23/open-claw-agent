import requests
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY


def search_jobs(query):
    try:
        print("🔍 Searching jobs:", query)

        url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": 5,
            "what": query,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)
        data = response.json()

        jobs = data.get("results", [])

        if not jobs:
            print("⚠️ No results, fallback used")

            params["what"] = "software developer"
            response = requests.get(url, params=params)
            data = response.json()
            jobs = data.get("results", [])

        result = []

        for job in jobs:
            result.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "description": job.get("description", ""),
                "url": job.get("redirect_url", "")
            })

        return result

    except Exception as e:
        print("Job API Error:", e)
        return []
