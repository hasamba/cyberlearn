"""
Ensure hidden column exists in lessons table
Safe migration that checks before adding
"""

import sqlite3
from pathlib import Path

def ensure_hidden_column(db_path: str = "cyberlearn.db"):
    """Add hidden column if it doesn't exist"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if column exists
    cursor.execute("PRAGMA table_info(lessons)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'hidden' in columns:
        print(f"✅ 'hidden' column already exists in {db_path}")
    else:
        print(f"📝 Adding 'hidden' column to {db_path}...")
        cursor.execute("ALTER TABLE lessons ADD COLUMN hidden BOOLEAN DEFAULT 0")
        conn.commit()
        print(f"✅ 'hidden' column added successfully")

    # Verify all lessons are visible by default
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE hidden = 1")
    hidden_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM lessons")
    total_count = cursor.fetchone()[0]

    print(f"\n📊 Lesson visibility:")
    print(f"   Total lessons: {total_count}")
    print(f"   Visible: {total_count - hidden_count}")
    print(f"   Hidden: {hidden_count}")

    conn.close()

if __name__ == "__main__":
    ensure_hidden_column()
