"""
Load all lessons from content directory into database
"""

import json
import os
import sqlite3
from uuid import UUID
from pathlib import Path
from datetime import datetime
from utils.database import Database
from models.lesson import Lesson

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

        # Tag each lesson if not already tagged
        now = datetime.utcnow().isoformat()
        tagged_count = 0

        for (lesson_id,) in ez_lessons:
            # Check if already tagged
            cursor.execute("""
                SELECT 1 FROM lesson_tags
                WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, ez_tag_id))

            if not cursor.fetchone():
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

def load_all_lessons():
    """Load all lesson JSON files from content directory"""

    db = Database()
    content_dir = Path("content")

    lesson_files = list(content_dir.glob("lesson_*.json"))

    if not lesson_files:
        print("[ERROR] No lesson files found in content/ directory")
        print("        Files should be named: lesson_*.json")
        return

    print(f"[FOUND] {len(lesson_files)} lesson files")
    print("=" * 60)

    loaded = 0
    skipped = 0
    errors = 0

    for lesson_file in sorted(lesson_files):
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert lesson_id to UUID, but keep prerequisites as strings
            data['lesson_id'] = UUID(data['lesson_id'])
            # Prerequisites should remain as strings (as per model definition)
            data['prerequisites'] = [str(p) for p in data['prerequisites']]

            # Create lesson
            lesson = Lesson(**data)

            if db.create_lesson(lesson):
                print(f"[OK] Loaded: {lesson.title}")
                loaded += 1
            else:
                print(f"[SKIP] Already exists: {lesson.title}")
                skipped += 1

        except Exception as e:
            print(f"[ERROR] Loading {lesson_file.name}: {e}")
            errors += 1

    db.close()

    print("=" * 60)
    print(f"[LOADED] {loaded} lessons")
    print(f"[SKIPPED] {skipped} lessons")
    print(f"[ERRORS] {errors} lessons")
    print(f"[TOTAL] {loaded + skipped} lessons in database")

    # Auto-tag lessons with package tags
    if loaded > 0 or skipped > 0:
        auto_tag_lessons()


if __name__ == "__main__":
    load_all_lessons()
