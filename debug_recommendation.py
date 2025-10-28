"""Debug recommendation engine to see why completed lessons are recommended"""

import sqlite3
import json
from pathlib import Path

def debug_recommendations():
    db_path = Path("cyberlearn.db")

    if not db_path.exists():
        print("Error: cyberlearn.db not found")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get user info
    cursor.execute("SELECT user_id, username, lessons_completed FROM users")
    users = cursor.fetchall()

    print("\n=== Users ===")
    for user in users:
        print(f"User: {user['username']} (ID: {user['user_id']})")
        print(f"  Lessons completed (user record): {user['lessons_completed']}")

        # Get their progress
        cursor.execute("""
            SELECT lesson_id, status, completed_at, attempts, best_score
            FROM progress
            WHERE user_id = ?
            ORDER BY completed_at DESC
        """, (user['user_id'],))

        progress_records = cursor.fetchall()
        print(f"  Progress records: {len(progress_records)}")

        for prog in progress_records:
            print(f"    - Lesson: {prog['lesson_id']}")
            print(f"      Status: {prog['status']}")
            print(f"      Completed at: {prog['completed_at']}")
            print(f"      Attempts: {prog['attempts']}")
            print(f"      Best score: {prog['best_score']}")

        # Get lessons metadata
        cursor.execute("""
            SELECT lesson_id, title, domain, difficulty
            FROM lessons
        """)
        lessons = cursor.fetchall()

        print(f"\n  Total lessons in database: {len(lessons)}")

        # Check which lessons match progress
        completed_lesson_ids = [p['lesson_id'] for p in progress_records
                               if p['status'] in ['completed', 'mastered']]
        print(f"  Completed lesson IDs: {completed_lesson_ids}")

        # Check if any completed lessons are available
        for lesson in lessons:
            if lesson['lesson_id'] in completed_lesson_ids:
                print(f"\n  Completed lesson found: {lesson['title']}")
                print(f"    ID: {lesson['lesson_id']}")
                print(f"    Domain: {lesson['domain']}")

        print("\n" + "="*60)

    conn.close()

if __name__ == "__main__":
    debug_recommendations()
