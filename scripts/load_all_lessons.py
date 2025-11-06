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

def is_lesson_outdated(db, lesson: Lesson) -> bool:
    """Check if lesson in database is outdated compared to file"""
    cursor = db.conn.cursor()
    cursor.execute(
        "SELECT updated_at FROM lessons WHERE lesson_id = ?",
        (str(lesson.lesson_id),)
    )
    row = cursor.fetchone()

    if not row:
        return False  # Lesson doesn't exist

    db_updated_at = row[0]
    file_updated_at = lesson.updated_at.isoformat()

    return file_updated_at > db_updated_at


def update_lesson(db, lesson: Lesson) -> bool:
    """Update existing lesson in database"""
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            """
            UPDATE lessons SET
                domain = ?, title = ?, subtitle = ?, difficulty = ?,
                estimated_time = ?, order_index = ?, prerequisites = ?,
                learning_objectives = ?, content_blocks = ?,
                pre_assessment = ?, post_assessment = ?,
                mastery_threshold = ?, jim_kwik_principles = ?,
                base_xp_reward = ?, badge_unlock = ?, is_core_concept = ?,
                updated_at = ?, author = ?, version = ?
            WHERE lesson_id = ?
            """,
            (
                lesson.domain,
                lesson.title,
                lesson.subtitle,
                lesson.difficulty,
                lesson.estimated_time,
                lesson.order_index,
                json.dumps([str(p) for p in lesson.prerequisites]),
                json.dumps(lesson.learning_objectives),
                json.dumps([json.loads(block.model_dump_json()) for block in lesson.content_blocks]),
                (
                    json.dumps([json.loads(q.model_dump_json()) for q in lesson.pre_assessment])
                    if lesson.pre_assessment
                    else None
                ),
                json.dumps([json.loads(q.model_dump_json()) for q in lesson.post_assessment]),
                lesson.mastery_threshold,
                json.dumps(lesson.jim_kwik_principles),
                lesson.base_xp_reward,
                lesson.badge_unlock,
                int(lesson.is_core_concept),
                lesson.updated_at.isoformat(),
                lesson.author,
                lesson.version,
                str(lesson.lesson_id),
            ),
        )
        db.conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to update lesson: {e}")
        return False


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
    updated = 0
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

            # Try to create lesson first
            if db.create_lesson(lesson):
                print(f"[NEW] Loaded: {lesson.title}")
                loaded += 1
            else:
                # Lesson exists - check if outdated
                if is_lesson_outdated(db, lesson):
                    if update_lesson(db, lesson):
                        print(f"[UPDATE] Updated: {lesson.title}")
                        updated += 1
                    else:
                        print(f"[ERROR] Failed to update: {lesson.title}")
                        errors += 1
                else:
                    print(f"[SKIP] Up to date: {lesson.title}")
                    skipped += 1

        except Exception as e:
            print(f"[ERROR] Loading {lesson_file.name}: {e}")
            errors += 1

    db.close()

    print("=" * 60)
    print(f"[NEW] {loaded} lessons")
    print(f"[UPDATED] {updated} lessons")
    print(f"[SKIPPED] {skipped} lessons")
    print(f"[ERRORS] {errors} lessons")
    print(f"[TOTAL] {loaded + updated + skipped} lessons in database")

    # Auto-tag lessons with package tags
    if loaded > 0 or updated > 0 or skipped > 0:
        auto_tag_lessons()


if __name__ == "__main__":
    load_all_lessons()
