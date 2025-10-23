"""
CyberLearn Setup Script
Initializes database and loads sample lesson.
Run this once before starting the application.
"""

import json
from uuid import UUID
from pathlib import Path

# Import after path is set
from utils.database import Database
from models.lesson import Lesson


def setup_database():
    """Initialize database and load sample content"""

    print("=" * 60)
    print("CyberLearn Setup Script")
    print("=" * 60)

    # Step 1: Initialize database
    print("\n📊 Step 1: Initializing database...")
    try:
        db = Database()
        print("✅ Database created successfully: cyberlearn.db")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Step 2: Load sample lesson
    print("\n📚 Step 2: Loading sample CIA Triad lesson...")
    lesson_path = Path("content/sample_lesson_cia_triad.json")

    if not lesson_path.exists():
        print(f"❌ Sample lesson not found at: {lesson_path}")
        print("   Make sure you're running this from the project root directory")
        db.close()
        return False

    try:
        with open(lesson_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert string UUIDs to UUID objects
        data["lesson_id"] = UUID(data["lesson_id"])

        # Safely parse prerequisites, filtering out invalid UUIDs
        prereqs = []
        for p in data.get("prerequisites", []):
            if p and isinstance(p, str):
                try:
                    prereqs.append(UUID(p))
                except (ValueError, AttributeError):
                    continue
        data["prerequisites"] = prereqs

        # Create lesson object
        lesson = Lesson(**data)

        # Save to database
        if db.create_lesson(lesson):
            print(f"✅ Lesson '{lesson.title}' loaded successfully!")
        else:
            print("ℹ️  Lesson already exists in database (this is OK)")

    except Exception as e:
        print(f"❌ Failed to load lesson: {e}")
        db.close()
        return False

    # Step 3: Verify setup
    print("\n🔍 Step 3: Verifying setup...")
    try:
        all_lessons = db.get_all_lessons_metadata()
        print(f"✅ Found {len(all_lessons)} lesson(s) in database")

        for lesson_meta in all_lessons:
            print(f"   - {lesson_meta.title} (Domain: {lesson_meta.domain})")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        db.close()
        return False

    db.close()

    # Success message
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open browser to: http://localhost:8501")
    print("3. Create an account and start learning!")
    print("\n📖 For more help, see QUICK_START.md")
    print("=" * 60)

    return True


def reset_database():
    """Reset database (WARNING: deletes all data)"""

    print("\n⚠️  WARNING: This will delete ALL data!")
    response = input("Are you sure? Type 'yes' to confirm: ")

    if response.lower() != "yes":
        print("❌ Reset cancelled")
        return

    import os

    db_path = "cyberlearn.db"

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Deleted {db_path}")
    else:
        print(f"ℹ️  No database found at {db_path}")

    print("\n🔄 Re-initializing...")
    setup_database()


def show_stats():
    """Show database statistics"""

    print("\n📊 Database Statistics")
    print("=" * 60)

    try:
        db = Database()

        # Get counts
        import sqlite3

        cursor = db.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lessons")
        lesson_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM progress")
        progress_count = cursor.fetchone()[0]

        print(f"👥 Users: {user_count}")
        print(f"📚 Lessons: {lesson_count}")
        print(f"📈 Progress Records: {progress_count}")

        if user_count > 0:
            print("\n👤 Recent Users:")
            cursor.execute(
                "SELECT username, created_at FROM users ORDER BY created_at DESC LIMIT 5"
            )
            for row in cursor.fetchall():
                print(f"   - {row[0]} (joined {row[1][:10]})")

        db.close()

    except Exception as e:
        print(f"❌ Failed to get stats: {e}")

    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "reset":
            reset_database()
        elif command == "stats":
            show_stats()
        elif command == "help":
            print(
                """
CyberLearn Setup Script

Usage:
  python setup.py           Initialize database and load sample lesson
  python setup.py reset     Reset database (deletes all data)
  python setup.py stats     Show database statistics
  python setup.py help      Show this help message

Examples:
  # First-time setup
  python setup.py

  # Check what's in database
  python setup.py stats

  # Start fresh (WARNING: deletes data)
  python setup.py reset
            """
            )
        else:
            print(f"❌ Unknown command: {command}")
            print("   Run 'python setup.py help' for usage")
    else:
        # Default: run setup
        setup_database()
