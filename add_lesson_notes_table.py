#!/usr/bin/env python3
"""
Add lesson_notes table to existing database.

This migration script adds the lesson_notes table for block-level note-taking.
"""

import sqlite3
from pathlib import Path


def add_lesson_notes_table():
    """Add lesson_notes table to existing database"""
    db_path = Path("cyberlearn.db")

    if not db_path.exists():
        print("ERROR Database not found at cyberlearn.db")
        print("Please run the app first to create the database.")
        return False

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("=" * 60)
    print("ADDING LESSON_NOTES TABLE")
    print("=" * 60)

    # Check if lesson_notes table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lesson_notes'")
    has_table = cursor.fetchone() is not None

    if has_table:
        print("\nOK lesson_notes table already exists.")
        print("\nNo migration needed.")
        conn.close()
        return True

    # Create lesson_notes table
    print("\nCreating lesson_notes table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_notes (
            note_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            content_block_index INTEGER,
            note_text TEXT,
            note_type TEXT DEFAULT 'text',
            attachments TEXT DEFAULT '[]',
            is_pinned INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE
        )
    """)

    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_lesson_notes_user
        ON lesson_notes(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_lesson_notes_lesson
        ON lesson_notes(lesson_id)
    """)

    print("  OK lesson_notes table created")
    print("  OK Indexes created")

    conn.commit()

    print("\n" + "=" * 60)
    print("SUCCESS LESSON_NOTES TABLE ADDED!")
    print("=" * 60)
    print("\nUsers can now create notes at the content block level.")

    conn.close()
    return True


if __name__ == "__main__":
    import sys
    success = add_lesson_notes_table()
    sys.exit(0 if success else 1)
