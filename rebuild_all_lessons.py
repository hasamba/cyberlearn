#!/usr/bin/env python3
"""
Delete all lessons from database and reload from content/ directory.
This ensures the database matches exactly what's in the content folder.
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from uuid import UUID

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import Database
from models.lesson import Lesson

def delete_all_lessons(db_path="cyberlearn.db"):
    """Delete all lessons from database"""
    print("\n" + "="*80)
    print("DELETING ALL LESSONS FROM DATABASE")
    print("="*80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get count before deletion
        cursor.execute("SELECT COUNT(*) FROM lessons")
        count_before = cursor.fetchone()[0]
        print(f"\nLessons in database: {count_before}")

        if count_before == 0:
            print("No lessons to delete.")
            conn.close()
            return

        # Delete lesson_tags first (foreign key constraint)
        cursor.execute("DELETE FROM lesson_tags")
        tags_deleted = cursor.rowcount

        # Delete all lessons
        cursor.execute("DELETE FROM lessons")
        lessons_deleted = cursor.rowcount

        conn.commit()

        print(f"[✓] Deleted {tags_deleted} lesson-tag associations")
        print(f"[✓] Deleted {lessons_deleted} lessons")

    except Exception as e:
        print(f"[ERROR] Failed to delete lessons: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)
    finally:
        conn.close()

def auto_tag_lessons(db_path="cyberlearn.db"):
    """Automatically tag lessons with appropriate package tags after loading"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get the Eric Zimmerman Tools tag
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Package: Eric Zimmerman Tools'")
        ez_tag = cursor.fetchone()

        if not ez_tag:
            print("[WARN] Package: Eric Zimmerman Tools tag not found, skipping auto-tagging")
            return

        ez_tag_id = ez_tag[0]

        # Get DFIR lessons 11-24 (Eric Zimmerman Tools)
        cursor.execute("""
            SELECT lesson_id FROM lessons
            WHERE domain = 'dfir' AND order_index BETWEEN 11 AND 24
        """)
        ez_lessons = cursor.fetchall()

        if not ez_lessons:
            return

        # Tag each lesson
        now = datetime.utcnow().isoformat()
        tagged_count = 0

        for (lesson_id,) in ez_lessons:
            cursor.execute("""
                INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                VALUES (?, ?, ?)
            """, (lesson_id, ez_tag_id, now))
            tagged_count += 1

        conn.commit()

        if tagged_count > 0:
            print(f"[AUTO-TAG] Tagged {tagged_count} Eric Zimmerman Tools lessons")

    except Exception as e:
        conn.rollback()
        print(f"[WARN] Auto-tagging failed: {e}")
    finally:
        conn.close()

def load_all_lessons(db_path="cyberlearn.db"):
    """Load all lesson JSON files from content directory"""
    print("\n" + "="*80)
    print("LOADING ALL LESSONS FROM CONTENT/")
    print("="*80)

    db = Database(db_path=db_path)
    content_dir = Path("content")

    lesson_files = list(content_dir.glob("lesson_*.json"))

    if not lesson_files:
        print("[ERROR] No lesson files found in content/ directory")
        print("        Files should be named: lesson_*.json")
        return

    print(f"\n[FOUND] {len(lesson_files)} lesson files\n")

    loaded = 0
    errors = 0

    for lesson_file in sorted(lesson_files):
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert lesson_id to UUID
            data['lesson_id'] = UUID(data['lesson_id'])

            # Prerequisites should remain as strings
            data['prerequisites'] = [str(p) for p in data['prerequisites']]

            # Create lesson
            lesson = Lesson(**data)

            if db.create_lesson(lesson):
                print(f"[OK] {lesson.domain}{lesson.order_index:02d}: {lesson.title}")
                loaded += 1
            else:
                print(f"[WARN] Skipped (already exists): {lesson.title}")

        except Exception as e:
            print(f"[ERROR] Loading {lesson_file.name}: {e}")
            errors += 1

    db.close()

    print("\n" + "="*80)
    print(f"[LOADED] {loaded} lessons")
    print(f"[ERRORS] {errors} lessons")
    print(f"[TOTAL] {loaded} lessons in database")
    print("="*80)

    # Auto-tag lessons with package tags
    if loaded > 0:
        auto_tag_lessons(db_path)

def main():
    """Main entry point"""
    db_path = "cyberlearn.db"

    print("\n" + "="*80)
    print("REBUILD ALL LESSONS")
    print("="*80)
    print(f"\nDatabase: {db_path}")
    print("Content: content/")
    print("\nThis will:")
    print("  1. Delete ALL lessons from the database")
    print("  2. Load ALL lessons from content/ directory")
    print("  3. Auto-tag lessons with package tags")

    response = input("\nProceed? (yes/no): ").strip().lower()

    if response != 'yes':
        print("Cancelled. No changes made.")
        return

    # Step 1: Delete all lessons
    delete_all_lessons(db_path)

    # Step 2: Load all lessons
    load_all_lessons(db_path)

    print("\n" + "="*80)
    print("[✓] REBUILD COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("  - Run: streamlit run app.py")
    print("  - Verify lessons are loaded correctly")

if __name__ == "__main__":
    main()
