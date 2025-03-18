import sqlite3
import os

# ---------------------- 📂 DATABASE CONFIGURATION ----------------------
DB_PATH = "/home/ubuntu/AI-Presentation-Generator/database/feedback.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure DB directory exists

# ---------------------- 🏗️ DATABASE INITIALIZATION ----------------------
def initialize_db():
    """
    Creates necessary tables for storing AI feedback if they do not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table to store AI-generated feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            slide_number INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table to store user-provided feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            feedback TEXT NOT NULL,
            weightage INTEGER DEFAULT 1,  -- Higher weight for frequently repeated feedback
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---------------------- 🔄 STORE AI FEEDBACK ----------------------
def store_ai_feedback(topic, slide_number, feedback):
    """
    Stores AI-generated feedback for specific slides.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ai_feedback (topic, slide_number, feedback) VALUES (?, ?, ?)
    """, (topic, slide_number, feedback))

    conn.commit()
    conn.close()


# ---------------------- 🔄 STORE USER FEEDBACK ----------------------
def store_user_feedback(topic, feedback):
    """
    Stores user feedback and increases weightage if repeated feedback exists.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if feedback already exists
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


# ---------------------- 📊 RETRIEVE MOST RELEVANT FEEDBACK ----------------------
def retrieve_common_feedback(topic):
    """
    Retrieves the most frequently given user feedback for a topic.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT feedback FROM user_feedback WHERE topic = ? ORDER BY weightage DESC LIMIT 5
    """, (topic,))
    feedback_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return feedback_list


# ---------------------- 🔥 INITIALIZE DATABASE ON IMPORT ----------------------
initialize_db()