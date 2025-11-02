import sqlite3
from pathlib import Path

# ---------------------- 📂 DATABASE CONFIGURATION ----------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "feedback.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure DB directory exists

# ---------------------- 🏗️ DATABASE INITIALIZATION ----------------------
def initialize_db():
    """
    Creates necessary tables for storing AI feedback if they do not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ Stores AI-generated content for each slide (for reuse & improvements)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            slide_number INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Stores **user preferences & past requests**
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            num_slides INTEGER NOT NULL,
            font_choice TEXT DEFAULT 'Arial',
            color_scheme TEXT DEFAULT '#000000',
            bullet_style TEXT DEFAULT 'Dots',
            header_color TEXT DEFAULT '#00008B',
            body_font_size INTEGER DEFAULT 22,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Stores **user feedback to improve AI**
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            feedback TEXT NOT NULL,
            weightage INTEGER DEFAULT 1,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---------------------- 🔄 STORE AI FEEDBACK ----------------------
def store_ai_feedback(topic, slide_number, feedback):
    """
    Stores AI-generated slide content for future optimization.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ai_feedback (topic, slide_number, feedback) VALUES (?, ?, ?)
    """, (topic, slide_number, feedback))

    conn.commit()
    conn.close()


# ---------------------- 🔄 STORE USER PREFERENCES ----------------------
def store_user_preferences(topic, num_slides, font_choice, color_scheme, bullet_style, header_color, body_font_size):
    """
    Saves user-selected preferences (fonts, colors, styles) for future PPT generations.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_preferences (topic, num_slides, font_choice, color_scheme, bullet_style, header_color, body_font_size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (topic, num_slides, font_choice, color_scheme, bullet_style, header_color, body_font_size))
    
    conn.commit()
    conn.close()


# ---------------------- 🔄 STORE USER FEEDBACK ----------------------
def store_user_feedback(topic, feedback):
    """
    Stores user feedback and increases weightage if repeated feedback exists.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, weightage FROM user_feedback WHERE topic = ? AND feedback = ?
    """, (topic, feedback))
    result = cursor.fetchone()

    if result:
        feedback_id, weightage = result
        cursor.execute("""
            UPDATE user_feedback SET weightage = ? WHERE id = ?
        """, (weightage + 1, feedback_id))
    else:
        cursor.execute("""
            INSERT INTO user_feedback (topic, feedback, weightage) VALUES (?, ?, 1)
        """, (topic, feedback))

    conn.commit()
    conn.close()


# ---------------------- 📊 RETRIEVE AI FEEDBACK ----------------------
def retrieve_common_feedback(topic):
    """
    Retrieves most frequently given AI feedback for a topic.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT feedback FROM ai_feedback WHERE topic = ? ORDER BY timestamp DESC LIMIT 5
    """, (topic,))
    feedback_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return feedback_list


# ---------------------- 📊 RETRIEVE USER PREFERENCES ----------------------
def retrieve_user_preferences(topic):
    """
    Fetches stored user preferences for a given topic.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT num_slides, font_choice, color_scheme, bullet_style, header_color, body_font_size
        FROM user_preferences WHERE topic = ? ORDER BY timestamp DESC LIMIT 1
    """, (topic,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "num_slides": result[0],
            "font_choice": result[1],
            "color_scheme": result[2],
            "bullet_style": result[3],
            "header_color": result[4],
            "body_font_size": result[5]
        }
    return None


# ---------------------- 🔄 RETRIEVE USER FEEDBACK ----------------------
def retrieve_past_feedback(topic):
    """
    Retrieves user-submitted feedback to improve slide generation.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT feedback FROM user_feedback WHERE topic = ? ORDER BY weightage DESC LIMIT 5
    """, (topic,))
    feedback_list = cursor.fetchall()
    conn.close()
    return [fb[0] for fb in feedback_list]


# ---------------------- 🔥 INITIALIZE DATABASE ON IMPORT ----------------------
initialize_db()
