import requests
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY


def search_jobs(query):
    try:
        print("🔍 Searching jobs for:", query)

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

        print("📡 API FULL RESPONSE:", data)

        jobs = []

        # ✅ If API returns empty → try fallback
        if not data.get("results"):
            print("⚠️ No results, trying fallback...")

            fallback_query = "software developer"

            params["what"] = fallback_query
            response = requests.get(url, params=params)
            data = response.json()

            print("📡 FALLBACK RESPONSE:", data)

        # ✅ Extract jobs
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "description": job.get("description", ""),
                "url": job.get("redirect_url") or job.get("url", "")
            })

        return jobs

    except Exception as e:
        print("❌ Job API Error:", e)
        return []
