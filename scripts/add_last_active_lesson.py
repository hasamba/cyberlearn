"""
Database migration: Add last_active_lesson_id and last_active_at to users table

This migration adds two new fields to track the user's last active lesson:
- last_active_lesson_id: UUID of the last lesson the user was viewing
- last_active_at: Timestamp of when they were last viewing that lesson

This enables "Continue Learning" functionality across devices.
"""

import sqlite3
from pathlib import Path

def migrate_database(db_path: str = "cyberlearn.db"):
    """Add last_active_lesson fields to users table"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'last_active_lesson_id' not in columns:
        print("Adding last_active_lesson_id column...")
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN last_active_lesson_id TEXT
        """)
        print("[OK] Added last_active_lesson_id column")
    else:
        print("[OK] last_active_lesson_id column already exists")

    if 'last_active_at' not in columns:
        print("Adding last_active_at column...")
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN last_active_at TEXT
        """)
        print("[OK] Added last_active_at column")
    else:
        print("[OK] last_active_at column already exists")

    conn.commit()
    conn.close()

    print("\n[SUCCESS] Migration completed successfully!")
    print("\nNext steps:")
    print("1. Update cyberlearn_template.db with: python update_template_database.py")
    print("2. Commit changes to git")
    print("3. Deploy to VM with: bash update_vm.sh")

if __name__ == "__main__":
    # Migrate main database
    print("Migrating cyberlearn.db...")
    migrate_database("cyberlearn.db")

    # Migrate template database if it exists
    template_path = Path("cyberlearn_template.db")
    if template_path.exists():
        print("\nMigrating cyberlearn_template.db...")
        migrate_database("cyberlearn_template.db")
