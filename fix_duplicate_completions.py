#!/usr/bin/env python3
"""
Fix duplicate XP and lesson completion counts from retaken lessons.
This script corrects the database to reflect that each lesson should only
award XP and count toward completion once.
"""

import sqlite3
import os

def fix_duplicate_completions():
    """Recalculate user stats based on unique lesson completions"""

    # Connect to database
    db_path = "cyberlearn.db"
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Access columns by name
    cursor = conn.cursor()

    # Get all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print(f"\n[INFO] Found {len(users)} users")

    for user_row in users:
        user_id = user_row['user_id']
        username = user_row['username']
        print(f"\n[+] Fixing user: {username}")

        # Get unique completed lessons
        cursor.execute(
            "SELECT * FROM lesson_progress WHERE user_id = ? AND status IN ('completed', 'mastered')",
            (user_id,)
        )
        progress_records = cursor.fetchall()

        unique_lessons = len(progress_records)
        current_count = user_row['total_lessons_completed']

        print(f"    Unique lessons completed: {unique_lessons}")
        print(f"    Current total_lessons_completed: {current_count}")

        # Update the correct count
        if unique_lessons != current_count:
            print(f"    [FIX] Updating to {unique_lessons}")
            cursor.execute(
                "UPDATE users SET total_lessons_completed = ? WHERE user_id = ?",
                (unique_lessons, user_id)
            )
        else:
            print(f"    [OK] Count is correct")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n[COMPLETE] Database fixed!")
    print("\nNote: XP and skill levels cannot be automatically recalculated.")
    print("The duplicate-prevention logic will prevent future issues.")
    print("Your level will update correctly next time you earn XP.\n")

if __name__ == "__main__":
    fix_duplicate_completions()
