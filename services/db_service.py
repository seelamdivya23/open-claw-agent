import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


# ---------------- CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ---------------- INIT TABLES ----------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Candidates table (existing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        score INT
    )
    """)

    # ✅ NEW: Jobs tracking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs_applied (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        company VARCHAR(255),
        url TEXT,
        status VARCHAR(50),
        applied_date DATE
    )
    """)

    conn.commit()
    conn.close()


# ---------------- SAVE CANDIDATE ----------------
def save_candidate(name, score):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO candidates (name, score) VALUES (%s, %s)"
    values = (name, score)

    cursor.execute(query, values)

    conn.commit()
    conn.close()


# ---------------- SAVE JOB ----------------
def save_job(title, company, url):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO jobs_applied (title, company, url, status, applied_date)
    VALUES (%s, %s, %s, %s, CURDATE())
    """

    values = (title, company, url, "applied")

    cursor.execute(query, values)

    conn.commit()
    conn.close()


# ---------------- GET TODAY SUMMARY ----------------
def get_today_jobs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT title, company 
    FROM jobs_applied
    WHERE applied_date = CURDATE()
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results
