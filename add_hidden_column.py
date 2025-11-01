#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add 'hidden' column to lessons table for hide/unhide lessons feature.

This migration adds:
- hidden INTEGER DEFAULT 0 to lessons table
"""

import sqlite3
import sys
from pathlib import Path

# Fix unicode output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = Path(__file__).parent / "cyberlearn.db"


def add_hidden_column():
    """Add hidden column to lessons table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("ADDING 'hidden' COLUMN TO LESSONS TABLE")
    print("=" * 60)
    print(f"Database: {DB_PATH}\n")

    try:
        # Check if hidden column already exists
        cursor.execute("PRAGMA table_info(lessons)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'hidden' in columns:
            print("✓ Column 'hidden' already exists in lessons table")
            print("\nNo changes needed.")
        else:
            # Add hidden column
            print("Adding 'hidden' column...")
            cursor.execute("""
                ALTER TABLE lessons
                ADD COLUMN hidden INTEGER DEFAULT 0
            """)
            conn.commit()
            print("✅ Column 'hidden' added successfully!")

            # Verify
            cursor.execute("PRAGMA table_info(lessons)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'hidden' in columns:
                print("✓ Verification: Column exists")
            else:
                print("❌ Verification failed: Column not found")
                return False

        # Show summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE hidden = 1")
        hidden_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM lessons")
        total_count = cursor.fetchone()[0]

        print(f"Total lessons: {total_count}")
        print(f"Hidden lessons: {hidden_count}")
        print(f"Visible lessons: {total_count - hidden_count}")

        print("\n✅ Migration completed successfully!")
        print("\nNext steps:")
        print("  1. Update template database: python update_template_database.py")
        print("  2. Create PR for testing")

        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        exit(1)

    success = add_hidden_column()
    exit(0 if success else 1)
