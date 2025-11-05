#!/usr/bin/env python3
"""
Force update lessons that had video replacements.

This script updates all lessons that appear in the replace_broken_videos.py
output, since the regular update script doesn't detect changes within
content blocks (only counts them).

Usage:
    python force_update_video_lessons.py
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Database configuration
DB_PATH = "cyberlearn.db"
CONTENT_DIR = Path("content")
MAPPING_FILE = Path("broken_videos_mapping.json")


def load_lesson_from_file(file_path: Path) -> dict:
    """Load and parse a lesson JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_lesson_in_db(conn: sqlite3.Connection, lesson_data: dict) -> bool:
    """Update a lesson in the database."""
    try:
        cursor = conn.cursor()

        # Prepare data
        lesson_id = lesson_data['lesson_id']
        domain = lesson_data['domain']
        title = lesson_data['title']
        subtitle = lesson_data.get('subtitle')
        difficulty = lesson_data['difficulty']
        estimated_time = lesson_data['estimated_time']
        order_index = lesson_data['order_index']
        prerequisites = json.dumps([str(p) for p in lesson_data.get('prerequisites', [])])
        learning_objectives = json.dumps(lesson_data['learning_objectives'])
        content_blocks = json.dumps(lesson_data['content_blocks'])
        pre_assessment = json.dumps(lesson_data['pre_assessment']) if lesson_data.get('pre_assessment') else None
        post_assessment = json.dumps(lesson_data['post_assessment'])
        mastery_threshold = lesson_data.get('mastery_threshold', 80)
        jim_kwik_principles = json.dumps(lesson_data['jim_kwik_principles'])
        base_xp_reward = lesson_data.get('base_xp_reward', 100)
        badge_unlock = lesson_data.get('badge_unlock')
        is_core_concept = int(lesson_data.get('is_core_concept', False))
        author = lesson_data.get('author')
        version = lesson_data.get('version', '1.0')

        # Update updated_at timestamp
        updated_at = datetime.utcnow().isoformat()

        # Update the lesson
        cursor.execute("""
            UPDATE lessons SET
                domain = ?,
                title = ?,
                subtitle = ?,
                difficulty = ?,
                estimated_time = ?,
                order_index = ?,
                prerequisites = ?,
                learning_objectives = ?,
                content_blocks = ?,
                pre_assessment = ?,
                post_assessment = ?,
                mastery_threshold = ?,
                jim_kwik_principles = ?,
                base_xp_reward = ?,
                badge_unlock = ?,
                is_core_concept = ?,
                updated_at = ?,
                author = ?,
                version = ?
            WHERE lesson_id = ?
        """, (
            domain, title, subtitle, difficulty, estimated_time, order_index,
            prerequisites, learning_objectives, content_blocks,
            pre_assessment, post_assessment, mastery_threshold,
            jim_kwik_principles, base_xp_reward, badge_unlock,
            is_core_concept, updated_at, author, version,
            lesson_id
        ))

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"[ERROR] Failed to update lesson {lesson_id}: {e}")
        conn.rollback()
        return False


def get_affected_lesson_files() -> list:
    """Get all lesson files that contain broken video IDs."""

    # Load mapping of broken videos
    if not MAPPING_FILE.exists():
        print(f"[ERROR] {MAPPING_FILE} not found!")
        return []

    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        replacements = json.load(f)

    broken_video_ids = list(replacements.keys())

    # Find all lesson files that contain these video IDs
    affected_files = []

    for lesson_file in CONTENT_DIR.glob("lesson_*_RICH.json"):
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if any broken video ID is in this file
            if any(video_id in content for video_id in broken_video_ids):
                lesson_data = load_lesson_from_file(lesson_file)
                affected_files.append((lesson_file, lesson_data))

        except Exception as e:
            print(f"[ERROR] Failed to read {lesson_file.name}: {e}")

    return affected_files


def main():
    """Force update all lessons with video replacements."""

    print("=" * 80)
    print("FORCE UPDATE LESSONS WITH VIDEO REPLACEMENTS")
    print("=" * 80)
    print()

    # Get affected lessons
    print("[FILES] Finding lessons with video replacements...")
    affected_files = get_affected_lesson_files()

    if not affected_files:
        print("[WARN]  No affected lessons found")
        return

    print(f"        Found {len(affected_files)} lessons to update")
    print()

    # Connect to database
    print("[DB]    Connecting to database...")
    conn = sqlite3.connect(DB_PATH)

    try:
        print("[UPDATE] Force updating lessons...")
        print()

        updated_count = 0
        failed_count = 0

        for lesson_file, lesson_data in affected_files:
            title = lesson_data.get('title', 'Unknown')
            lesson_id = lesson_data.get('lesson_id', 'Unknown')

            print(f"[UPDATE] {lesson_file.name}")
            print(f"         Title: {title}")
            print(f"         ID: {lesson_id}")

            if update_lesson_in_db(conn, lesson_data):
                print(f"         Status: SUCCESS")
                updated_count += 1
            else:
                print(f"         Status: FAILED")
                failed_count += 1

            print()

        # Summary
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total lessons:           {len(affected_files)}")
        print(f"Successfully updated:    {updated_count}")
        print(f"Failed to update:        {failed_count}")
        print()

        if updated_count > 0:
            print("[OK]    Database has been updated with fixed video URLs!")
            print()
            print("NEXT STEPS:")
            print("  1. Test in Streamlit app to verify video URLs")
            print("  2. Update template: python update_template_database.py")
            print("  3. Commit template: git add cyberlearn_template.db")
        else:
            print("[WARN]  No lessons were updated")

        print()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
