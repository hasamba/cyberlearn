#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration script to add user_id column to tags table.
This allows us to track which user created which tag.
System tags will have user_id = NULL.
"""

import sqlite3
import sys
from pathlib import Path

# Fix unicode output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = Path(__file__).parent / "cyberlearn.db"


def migrate():
    """Add user_id column to tags table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if column already exists
    cursor.execute("PRAGMA table_info(tags)")
    columns = [row[1] for row in cursor.fetchall()]

    if "user_id" not in columns:
        print("Adding user_id column to tags table...")
        cursor.execute("ALTER TABLE tags ADD COLUMN user_id TEXT")
        conn.commit()
        print("✓ Added user_id column")

        # All existing tags are system tags (user_id = NULL)
        print("\n✓ All existing tags marked as system tags (user_id = NULL)")
        print("✓ New tags created by users will have their user_id set")
    else:
        print("✓ user_id column already exists")

    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("TAG USER TRACKING MIGRATION")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print()

    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    migrate()

    print("\n✅ Migration completed successfully!")
    print("\nNext steps:")
    print("  - User-created tags will have user_id set")
    print("  - System tags will have user_id = NULL")
    print("  - UI will only show tags where user_id = current_user_id")
