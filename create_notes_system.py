"""
Create Lesson Notes System

Database schema for user notes with rich content support:
- Text notes
- URL attachments
- Image uploads
- Video embeds
- Code snippets
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def create_notes_system(db_path: str = "cyberlearn.db"):
    """Create lesson_notes table and related structures"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("CREATING LESSON NOTES SYSTEM")
    print("=" * 60)

    # Create lesson_notes table
    print("\n[1/2] Creating lesson_notes table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_notes (
            note_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            content_block_index INTEGER,
            note_text TEXT,
            note_type TEXT DEFAULT 'text',
            attachments TEXT,
            is_pinned BOOLEAN DEFAULT 0,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
        )
    """)
    print("   [OK] lesson_notes table created")

    # Create indexes for performance
    print("\n[2/2] Creating indexes...")

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_user
        ON lesson_notes(user_id)
    """)
    print("   [OK] Index on user_id created")

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_lesson
        ON lesson_notes(lesson_id)
    """)
    print("   [OK] Index on lesson_id created")

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_user_lesson
        ON lesson_notes(user_id, lesson_id)
    """)
    print("   [OK] Index on user_id + lesson_id created")

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_pinned
        ON lesson_notes(user_id, is_pinned)
    """)
    print("   [OK] Index on user_id + is_pinned created")

    conn.commit()

    # Verify table structure
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    cursor.execute("PRAGMA table_info(lesson_notes)")
    columns = cursor.fetchall()

    print("\nlesson_notes table columns:")
    for col in columns:
        print(f"   - {col[1]:20} {col[2]:10} {'NOT NULL' if col[3] else ''}")

    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM lesson_notes")
    count = cursor.fetchone()[0]
    print(f"\nCurrent notes count: {count}")

    conn.close()

    print("\n" + "=" * 60)
    print("[SUCCESS] LESSON NOTES SYSTEM CREATED!")
    print("=" * 60)
    print("\nDatabase structure:")
    print("  - lesson_notes table: [OK]")
    print("  - 4 indexes for performance: [OK]")
    print("\nNote types supported:")
    print("  - text: Plain text notes")
    print("  - url: URL attachments with previews")
    print("  - image: Image uploads")
    print("  - video: Video embeds (YouTube, Vimeo)")
    print("  - code: Code snippets with syntax highlighting")
    print("\nReady to implement UI!")
    print()

if __name__ == "__main__":
    create_notes_system()
