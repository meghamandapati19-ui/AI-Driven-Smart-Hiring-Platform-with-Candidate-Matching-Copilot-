from database.database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        phone TEXT,

        skills TEXT,

        education TEXT,

        experience TEXT,

        projects TEXT,

        certifications TEXT,

        languages TEXT,

        status TEXT DEFAULT 'Applied'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_title TEXT,

            skills TEXT,

            experience TEXT,

            education TEXT,

            responsibilities TEXT
        )
    """)

    conn.commit()

    conn.close()