"""
Migration: Add system and cloud domains to user skill levels
Run this once to update the database schema
"""

import sqlite3
import sys
import os

def migrate():
    """Add system and cloud skill columns to users table"""

    # Find database file
    db_path = 'cyberlearn.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("This is normal if you haven't created any users yet.")
        print("The new domains will be included automatically when you create users.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Migrating database to add system and cloud domains...")
        print()

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        changes_made = False

        # Add system skill if not exists
        if 'skill_system' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN skill_system INTEGER DEFAULT 0")
            print("[OK] Added skill_system column")
            changes_made = True
        else:
            print("[INFO] skill_system column already exists")

        # Add cloud skill if not exists
        if 'skill_cloud' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN skill_cloud INTEGER DEFAULT 0")
            print("[OK] Added skill_cloud column")
            changes_made = True
        else:
            print("[INFO] skill_cloud column already exists")

        if changes_made:
            conn.commit()
            print()
            print("[SUCCESS] Migration completed successfully!")
            print()
            print("The database now supports two new domains:")
            print("  - system: Operating systems security (Windows, Linux)")
            print("  - cloud: Cloud security (AWS, Azure, GCP)")
            print()
            print("Next steps:")
            print("  1. Create lessons for the new domains")
            print("  2. Run: python load_all_lessons.py")
            print("  3. Run: streamlit run app.py")
        else:
            print()
            print("[INFO] Database already up to date - no changes needed")

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
