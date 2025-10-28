#!/usr/bin/env python3
"""
Debug script to check actual database state and identify issues
"""

import sqlite3
import os

def debug_database():
    """Check database state"""

    db_path = "cyberlearn.db"
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("DATABASE DEBUG REPORT")
    print("="*60)

    # Check users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for user in users:
        print(f"\n[USER: {user['username']}]")
        print(f"  User ID: {user['user_id']}")
        print(f"  Total XP: {user['total_xp']}")
        print(f"  Level: {user['level']}")
        print(f"  Total Lessons Completed: {user['total_lessons_completed']}")

        # Calculate what level should be based on XP
        total_xp = user['total_xp']
        if total_xp < 1000:
            expected_level = 1
        elif total_xp < 3000:
            expected_level = 2
        elif total_xp < 7000:
            expected_level = 3
        elif total_xp < 15000:
            expected_level = 4
        elif total_xp < 30000:
            expected_level = 5
        else:
            expected_level = 6

        print(f"  Expected Level (based on XP): {expected_level}")
        if expected_level != user['level']:
            print(f"  ⚠️  LEVEL MISMATCH! Should be {expected_level}, is {user['level']}")

        # Check progress records
        cursor.execute(
            "SELECT lesson_id, status, attempts, best_score, completed_at FROM progress WHERE user_id = ?",
            (user['user_id'],)
        )
        progress_records = cursor.fetchall()

        print(f"\n  Progress Records: {len(progress_records)} total")

        # Count by status
        completed = sum(1 for p in progress_records if p['status'] == 'completed')
        mastered = sum(1 for p in progress_records if p['status'] == 'mastered')
        in_progress = sum(1 for p in progress_records if p['status'] == 'in_progress')

        print(f"    - Completed: {completed}")
        print(f"    - Mastered: {mastered}")
        print(f"    - In Progress: {in_progress}")
        print(f"    - Total Completed + Mastered: {completed + mastered}")

        if user['total_lessons_completed'] != (completed + mastered):
            print(f"  ⚠️  COMPLETION COUNT MISMATCH!")
            print(f"     Database says: {user['total_lessons_completed']}")
            print(f"     Actual unique: {completed + mastered}")

        # Show lessons with multiple attempts (retakes)
        retakes = [p for p in progress_records if p['attempts'] > 1]
        if retakes:
            print(f"\n  Lessons Retaken ({len(retakes)}):")
            for p in retakes:
                cursor.execute("SELECT title FROM lessons WHERE lesson_id = ?", (p['lesson_id'],))
                lesson = cursor.fetchone()
                lesson_title = lesson['title'] if lesson else "Unknown"
                print(f"    - {lesson_title}: {p['attempts']} attempts, best score: {p['best_score']}%")

    # Check if lessons exist
    cursor.execute("SELECT COUNT(*) as count FROM lessons")
    lesson_count = cursor.fetchone()['count']
    print(f"\n[LESSONS]")
    print(f"  Total lessons in database: {lesson_count}")

    # Check lessons by domain
    cursor.execute("SELECT domain, COUNT(*) as count FROM lessons GROUP BY domain ORDER BY domain")
    domains = cursor.fetchall()
    print(f"\n  Lessons by domain:")
    for d in domains:
        print(f"    - {d['domain']}: {d['count']} lessons")

    conn.close()

    print("\n" + "="*60)
    print("END OF REPORT")
    print("="*60 + "\n")

if __name__ == "__main__":
    debug_database()
