#!/usr/bin/env python3
"""
Migration script to add last_username and preferred_tag_filters columns to users table.
These columns store UI preferences that persist across sessions.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "cyberlearn.db"


def migrate():
    """Add last_username and preferred_tag_filters columns to users table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    changes_made = False

    # Add last_username column if missing
    if "last_username" not in columns:
        print("Adding last_username column...")
        cursor.execute("ALTER TABLE users ADD COLUMN last_username TEXT")
        changes_made = True
        print("✓ Added last_username column")
    else:
        print("✓ last_username column already exists")

    # Add preferred_tag_filters column if missing
    if "preferred_tag_filters" not in columns:
        print("Adding preferred_tag_filters column...")
        cursor.execute("ALTER TABLE users ADD COLUMN preferred_tag_filters TEXT DEFAULT '[]'")
        changes_made = True
        print("✓ Added preferred_tag_filters column")
    else:
        print("✓ preferred_tag_filters column already exists")

    if changes_made:
        conn.commit()
        print("\n✅ Migration completed successfully!")
    else:
        print("\n✅ No migration needed - all columns present")

    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("USER PREFERENCES MIGRATION")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print()

    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    migrate()
