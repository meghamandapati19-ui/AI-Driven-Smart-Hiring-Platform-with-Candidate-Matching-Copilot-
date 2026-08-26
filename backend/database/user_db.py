import hashlib

from database.database import get_connection


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Convert password into a SHA-256 password hash.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE USERS TABLE
# ============================================================

def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            candidate_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE LOWER(email) = LOWER(?)
    """, (
        email.strip(),
    ))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    name,
    email,
    password,
    role
):

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # ----------------------------------------------------
        # Clean input
        # ----------------------------------------------------

        name = name.strip()
        email = email.strip().lower()
        role = role.strip().lower()

        # ----------------------------------------------------
        # Validate role
        # ----------------------------------------------------

        if role not in [
            "candidate",
            "recruiter"
        ]:

            conn.close()

            return {
                "success": False,
                "error": "Invalid role."
            }

        # ----------------------------------------------------
        # Check existing email
        # ----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM users
            WHERE LOWER(email) = LOWER(?)
        """, (
            email,
        ))

        existing_user = cursor.fetchone()

        if existing_user:

            conn.close()

            return {
                "success": False,
                "error": "Email already registered."
            }

        # ----------------------------------------------------
        # Hash password
        # ----------------------------------------------------

        password_hash = hash_password(
            password
        )

        # ====================================================
        # CANDIDATE REGISTRATION
        # ====================================================

        if role == "candidate":

            # ------------------------------------------------
            # Create candidate profile
            # ------------------------------------------------

            cursor.execute("""
                INSERT INTO candidates (
                    name,
                    email,
                    phone,
                    skills,
                    education,
                    experience,
                    resume_text,
                    match_score,
                    ats_score,
                    compatibility_score,
                    hiring_score,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                email,
                "",
                "[]",
                "[]",
                "[]",
                "",
                0,
                0,
                0,
                0,
                "Pending"
            ))

            # Get newly created candidate ID

            candidate_id = cursor.lastrowid

            # ------------------------------------------------
            # Create user account linked to candidate
            # ------------------------------------------------

            cursor.execute("""
                INSERT INTO users (
                    name,
                    email,
                    password,
                    role,
                    candidate_id
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                email,
                password_hash,
                role,
                candidate_id
            ))

        # ====================================================
        # RECRUITER REGISTRATION
        # ====================================================

        else:

            # Recruiters do not need a candidate profile

            candidate_id = None

            cursor.execute("""
                INSERT INTO users (
                    name,
                    email,
                    password,
                    role,
                    candidate_id
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                email,
                password_hash,
                role,
                candidate_id
            ))

        # ----------------------------------------------------
        # Get newly created user ID
        # ----------------------------------------------------

        user_id = cursor.lastrowid

        # ----------------------------------------------------
        # Save changes
        # ----------------------------------------------------

        conn.commit()
        conn.close()

        return {
            "success": True,
            "user_id": user_id,
            "candidate_id": candidate_id
        }

    except Exception as e:

        if conn:

            conn.rollback()
            conn.close()

        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(
    email,
    password
):

    user = get_user_by_email(
        email
    )

    # --------------------------------------------------------
    # User does not exist
    # --------------------------------------------------------

    if not user:

        return {
            "success": False,
            "error": "Email not registered."
        }

    # --------------------------------------------------------
    # Hash entered password
    # --------------------------------------------------------

    entered_password_hash = hash_password(
        password
    )

    stored_password = user["password"]

    # --------------------------------------------------------
    # Compare hashed password
    # --------------------------------------------------------

    if stored_password == entered_password_hash:

        return {
            "success": True,
            "user": user
        }

    # --------------------------------------------------------
    # Support old accounts that may have plain-text password
    # --------------------------------------------------------

    if stored_password == password:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            entered_password_hash,
            user["id"]
        ))

        conn.commit()
        conn.close()

        user["password"] = entered_password_hash

        return {
            "success": True,
            "user": user
        }

    # --------------------------------------------------------
    # Wrong password
    # --------------------------------------------------------

    return {
        "success": False,
        "error": "Incorrect password."
    }


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (
        user_id,
    ))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role,
            candidate_id,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    users = []

    for row in rows:

        users.append(
            dict(row)
        )

    return users


# ============================================================
# UPDATE CANDIDATE ID
# ============================================================

def update_user_candidate_id(
    user_id,
    candidate_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET candidate_id = ?
        WHERE id = ?
    """, (
        candidate_id,
        user_id
    ))

    conn.commit()
    conn.close()


# ============================================================
# DELETE USER
# ============================================================

def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (
        user_id,
    ))

    conn.commit()
    conn.close()