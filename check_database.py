"""
Check database contents and optionally reset user data
"""

import sqlite3
import sys

db_path = "cyberlearn.db"

def check_database():
    """Check what's in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("CyberLearn Database Check")
    print("=" * 60)

    # Check users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"\n👥 Users: {user_count}")

    if user_count > 0:
        cursor.execute("SELECT username, total_xp, level, diagnostic_completed FROM users")
        for row in cursor.fetchall():
            print(f"   - {row[0]}: Level {row[2]}, {row[1]} XP, Diagnostic: {'✅' if row[3] else '❌'}")

    # Check lessons
    cursor.execute("SELECT COUNT(*) FROM lessons")
    lesson_count = cursor.fetchone()[0]
    print(f"\n📚 Lessons: {lesson_count}")

    if lesson_count > 0:
        cursor.execute("SELECT title, domain, difficulty FROM lessons")
        for row in cursor.fetchall():
            print(f"   - {row[0]} (Domain: {row[1]}, Difficulty: {row[2]})")
    else:
        print("   ⚠️  No lessons found! Run: python setup.py")

    # Check progress
    cursor.execute("SELECT COUNT(*) FROM progress")
    progress_count = cursor.fetchone()[0]
    print(f"\n📈 Progress Records: {progress_count}")

    conn.close()
    print("=" * 60)


def reset_user(username):
    """Reset a specific user's progress"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Reset user skills to zero
    cursor.execute("""
        UPDATE users
        SET skill_levels = '{"fundamentals":0,"dfir":0,"malware":0,"active_directory":0,"pentest":0,"redteam":0,"blueteam":0}',
            diagnostic_completed = 0,
            total_xp = 0,
            level = 1,
            total_lessons_completed = 0
        WHERE username = ?
    """, (username,))

    # Delete user's progress
    cursor.execute("DELETE FROM progress WHERE user_id = (SELECT user_id FROM users WHERE username = ?)", (username,))

    conn.commit()
    conn.close()

    print(f"✅ Reset user '{username}' - skills, XP, and progress cleared")
    print("   Run diagnostic again to get proper skill assessment")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        if len(sys.argv) > 2:
            reset_user(sys.argv[2])
        else:
            print("Usage: python check_database.py reset <username>")
    else:
        check_database()
