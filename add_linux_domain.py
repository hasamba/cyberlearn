#!/usr/bin/env python3
"""
Database migration script to add Linux domain skill column.
Run this ONCE after pulling the Linux domain update.
"""

import sqlite3
import os

def main():
    db_path = "cyberlearn.db"

    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found at {db_path}")
        print("[INFO] Run 'python load_all_lessons.py' first to create database")
        return

    print("[START] Adding Linux domain to database...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if linux column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'linux' in columns:
        print("[SKIP] Linux column already exists in users table")
        conn.close()
        return

    try:
        # Add linux column to users table
        print("[MIGRATE] Adding 'linux' skill column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN linux INTEGER DEFAULT 0")

        conn.commit()
        print("[SUCCESS] Linux domain added successfully!")
        print("[INFO] All existing users now have linux skill = 0")

    except sqlite3.Error as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

    print("\n[NEXT STEPS]")
    print("1. Load Linux lessons: python load_all_lessons.py")
    print("2. Restart application: ./start.sh")

if __name__ == "__main__":
    main()
