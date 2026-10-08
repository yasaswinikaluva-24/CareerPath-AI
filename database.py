import sqlite3
import hashlib
import json
import os

DB_FILE = "career_data.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        name TEXT,
        skills TEXT,
        logic INTEGER DEFAULT 5,
        creativity INTEGER DEFAULT 5,
        communication INTEGER DEFAULT 5,
        preferences TEXT
    )
    """)
    
    # Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    
    # Career results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        career_name TEXT,
        match_percentage REAL,
        skills_gap TEXT,
        roadmap TEXT,
        courses TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    
    # Mock interviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        career_name TEXT,
        feedback TEXT,
        score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    
    # Dynamic column migrations for SaaS features
    try:
        cursor.execute("ALTER TABLE career_results ADD COLUMN roadmap_progress TEXT DEFAULT '[]'")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN xp INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN badges TEXT DEFAULT '[]'")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_pro INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    """Generates a PBKDF2 hash of a password using a unique salt."""
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return f"{salt.hex()}${dk.hex()}"

def register_user(username, password, name):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        pw_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, name) VALUES (?, ?, ?)",
            (username, pw_hash, name)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT name, password_hash FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    name, stored_hash = row
    
    # Check if stored_hash matches new salted format
    if "$" in stored_hash:
        try:
            salt_hex, hash_hex = stored_hash.split("$")
            salt = bytes.fromhex(salt_hex)
            dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            if dk.hex() == hash_hex:
                return name
        except Exception:
            pass
    else:
        # Legacy fallback
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()
        if legacy_hash == stored_hash:
            # Upgrade legacy hash to PBKDF2
            try:
                new_hash = hash_password(password)
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE username = ?",
                    (new_hash, username)
                )
                conn.commit()
                conn.close()
            except Exception:
                pass
            return name
            
    return None

def get_user_profile(username):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT name, skills, logic, creativity, communication, preferences FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "name": row[0],
            "skills": row[1] if row[1] else "",
            "logic": row[2],
            "creativity": row[3],
            "communication": row[4],
            "preferences": json.loads(row[5]) if row[5] else {}
        }
    return None

def update_user_profile(username, name, skills, logic, creativity, communication, preferences):
    conn = get_connection()
    cursor = conn.cursor()
    
    pref_str = json.dumps(preferences)
    cursor.execute("""
        UPDATE users 
        SET name = ?, skills = ?, logic = ?, creativity = ?, communication = ?, preferences = ?
        WHERE username = ?
    """, (name, skills, logic, creativity, communication, pref_str, username))
    
    conn.commit()
    conn.close()

def save_chat_message(username, role, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)",
        (username, role, content)
    )
    conn.commit()
    conn.close()

def get_chat_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_history WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def clear_chat_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def save_career_result(username, career_name, match_percentage, skills_gap, roadmap, courses):
    conn = get_connection()
    cursor = conn.cursor()
    
    gap_str = json.dumps(skills_gap)
    cursor.execute("""
        INSERT INTO career_results (username, career_name, match_percentage, skills_gap, roadmap, courses)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, career_name, match_percentage, gap_str, roadmap, courses))
    
    conn.commit()
    conn.close()

def get_career_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT career_name, match_percentage, skills_gap, roadmap, courses, timestamp 
        FROM career_results WHERE username = ? ORDER BY timestamp DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "career_name": r[0],
            "match_percentage": r[1],
            "skills_gap": json.loads(r[2]) if r[2] else {},
            "roadmap": r[3],
            "courses": r[4],
            "timestamp": r[5]
        })
    return results

def save_mock_interview(username, career_name, feedback, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mock_interviews (username, career_name, feedback, score)
        VALUES (?, ?, ?, ?)
    """, (username, career_name, feedback, score))
    conn.commit()
    conn.close()

def get_mock_interview_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT career_name, feedback, score, timestamp 
        FROM mock_interviews WHERE username = ? ORDER BY timestamp DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        "career_name": r[0],
        "feedback": r[1],
        "score": r[2],
        "timestamp": r[3]
    } for r in rows]

def add_user_xp(username, xp_to_add):
    """Adds XP points to user and returns the new XP, level, and whether a new level was unlocked."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT xp FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    old_xp = row[0] if (row and row[0] is not None) else 0
    new_xp = old_xp + xp_to_add
    
    cursor.execute("UPDATE users SET xp = ? WHERE username = ?", (new_xp, username))
    conn.commit()
    conn.close()
    
    old_level = old_xp // 100 + 1
    new_level = new_xp // 100 + 1
    leveled_up = new_level > old_level
    
    # Auto badge for reaching Level 2
    if leveled_up and new_level == 2:
        unlock_user_badge(username, "Level 2 Achiever")
        
    return new_xp, new_level, leveled_up

def unlock_user_badge(username, badge_name):
    """Unlocks a badge for the user if not already unlocked."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT badges FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    badges = []
    if row and row[0]:
        try:
            badges = json.loads(row[0])
        except Exception:
            badges = []
            
    if badge_name not in badges:
        badges.append(badge_name)
        badges_str = json.dumps(badges)
        cursor.execute("UPDATE users SET badges = ? WHERE username = ?", (badges_str, username))
        conn.commit()
        
    conn.close()

def update_roadmap_progress(username, career_name, completed_tasks_list):
    """Updates the task roadmap progress for the latest matching career result."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Find the latest career result ID for this user and career
    cursor.execute("""
        SELECT id FROM career_results 
        WHERE username = ? AND career_name = ? 
        ORDER BY timestamp DESC LIMIT 1
    """, (username, career_name))
    row = cursor.fetchone()
    
    if row:
        result_id = row[0]
        progress_str = json.dumps(completed_tasks_list)
        cursor.execute("""
            UPDATE career_results SET roadmap_progress = ? 
            WHERE id = ?
        """, (progress_str, result_id))
        conn.commit()
        
    conn.close()

def get_roadmap_progress(username, career_name):
    """Gets the roadmap task progress for the latest matching career result."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT roadmap_progress FROM career_results 
        WHERE username = ? AND career_name = ? 
        ORDER BY timestamp DESC LIMIT 1
    """, (username, career_name))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0]:
        try:
            return json.loads(row[0])
        except Exception:
            pass
    return []

def get_user_gamification(username):
    """Gets user's current XP and unlocked badges."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT xp, badges FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    xp = 0
    badges = []
    if row:
        xp = row[0] if row[0] is not None else 0
        if row[1]:
            try:
                badges = json.loads(row[1])
            except Exception:
                pass
    return {"xp": xp, "badges": badges}

def get_user_subscription(username):
    """Checks if the user has an active Pro membership."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT is_pro FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and row[0] == 1:
            return True
    except Exception:
        pass
    finally:
        conn.close()
    return False

def upgrade_to_pro(username):
    """Upgrades user to Pro membership in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET is_pro = 1 WHERE username = ?", (username,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def cancel_pro_subscription(username):
    """Reverts user subscription to Free tier."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET is_pro = 0 WHERE username = ?", (username,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

