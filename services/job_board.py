# services/job_board.py
import json
import time

FILE = "data/job_board.json"

def post_job(job_desc):

    job = {
        "id": str(time.time()),
        "description": job_desc
    }

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(job)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return job
