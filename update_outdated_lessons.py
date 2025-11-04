"""
Update outdated lessons in the database from lesson files.

This script:
1. Compares lessons in the database with lesson files
2. Identifies outdated lessons (where file content differs from DB)
3. Updates those lessons in the database with the latest content from files

Usage:
    python update_outdated_lessons.py
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Database configuration
DB_PATH = "cyberlearn.db"  # Use working database, not template
CONTENT_DIR = Path("content")


def load_lesson_from_file(file_path: Path) -> Dict:
    """Load and parse a lesson JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_lesson_files() -> Dict[str, tuple]:
    """Get all lesson files from content/ directory.

    Returns:
        Dict mapping lesson_id to (file_path, lesson_data)
    """
    lesson_files = {}

    for file_path in CONTENT_DIR.glob("lesson_*.json"):
        try:
            lesson_data = load_lesson_from_file(file_path)
            lesson_id = lesson_data.get('lesson_id')

            if lesson_id:
                lesson_files[lesson_id] = (file_path, lesson_data)

        except Exception as e:
            print(f"[ERROR] Failed to load {file_path.name}: {e}")

    return lesson_files


def update_lesson_in_db(conn: sqlite3.Connection, lesson_data: Dict) -> bool:
    """Update a lesson in the database.

    Args:
        conn: Database connection
        lesson_data: Complete lesson data from JSON file

    Returns:
        True if updated successfully, False otherwise
    """
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
        return True

    except Exception as e:
        print(f"[ERROR] Failed to update lesson {lesson_id}: {e}")
        conn.rollback()
        return False


def compare_lesson_content(file_data: Dict, db_lesson: Dict) -> List[str]:
    """Compare lesson file content with database content.

    Returns:
        List of differences found (empty if identical)
    """
    differences = []

    # Compare key fields
    fields_to_compare = [
        'title', 'domain', 'difficulty', 'order_index',
        'estimated_time', 'learning_objectives',
        'prerequisites', 'jim_kwik_principles'
    ]

    for field in fields_to_compare:
        file_value = file_data.get(field)
        db_value = db_lesson.get(field)

        # Handle list comparisons
        if isinstance(file_value, list) and isinstance(db_value, list):
            if sorted(str(x) for x in file_value) != sorted(str(x) for x in db_value):
                differences.append(field)
        elif file_value != db_value:
            differences.append(field)

    # Compare content blocks count
    file_blocks = len(file_data.get('content_blocks', []))
    db_blocks = len(db_lesson.get('content_blocks', []))
    if file_blocks != db_blocks:
        differences.append('content_blocks')

    # Compare post_assessment count
    file_assessments = len(file_data.get('post_assessment', []))
    db_assessments = len(db_lesson.get('post_assessment', []))
    if file_assessments != db_assessments:
        differences.append('post_assessment')

    return differences


def get_db_lesson(conn: sqlite3.Connection, lesson_id: str) -> Dict:
    """Get a single lesson from database by ID."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT lesson_id, title, domain, difficulty, order_index,
               estimated_time, prerequisites, learning_objectives,
               jim_kwik_principles, content_blocks, post_assessment
        FROM lessons
        WHERE lesson_id = ?
    """, (lesson_id,))

    row = cursor.fetchone()
    if not row:
        return None

    return {
        'lesson_id': row[0],
        'title': row[1],
        'domain': row[2],
        'difficulty': row[3],
        'order_index': row[4],
        'estimated_time': row[5],
        'prerequisites': json.loads(row[6]) if row[6] else [],
        'learning_objectives': json.loads(row[7]) if row[7] else [],
        'jim_kwik_principles': json.loads(row[8]) if row[8] else [],
        'content_blocks': json.loads(row[9]) if row[9] else [],
        'post_assessment': json.loads(row[10]) if row[10] else [],
    }


def main():
    """Main update logic."""
    print("=" * 80)
    print("UPDATE OUTDATED LESSONS IN DATABASE")
    print("=" * 80)
    print()

    # Load lesson files
    print("[FILES] Loading lesson files from content/...")
    lesson_files = get_all_lesson_files()
    print(f"        Found {len(lesson_files)} lesson files")
    print()

    # Connect to database
    print("[DB]    Connecting to database...")
    conn = sqlite3.connect(DB_PATH)

    try:
        # Find outdated lessons
        print("[CHECK] Checking for outdated lessons...")
        outdated = []

        for lesson_id, (file_path, file_data) in lesson_files.items():
            db_lesson = get_db_lesson(conn, lesson_id)

            if db_lesson:
                differences = compare_lesson_content(file_data, db_lesson)
                if differences:
                    outdated.append((lesson_id, file_path, file_data, differences))

        print(f"        Found {len(outdated)} outdated lessons")
        print()

        if not outdated:
            print("[OK]    All lessons are up to date!")
            return

        # Update outdated lessons
        print("[UPDATE] Updating outdated lessons...")
        print()

        updated_count = 0
        failed_count = 0

        for lesson_id, file_path, file_data, differences in outdated:
            title = file_data.get('title', 'Unknown')
            print(f"[UPDATE] {file_path.name}")
            print(f"         Title: {title}")
            print(f"         Changed fields: {', '.join(differences)}")

            if update_lesson_in_db(conn, file_data):
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
        print(f"Total outdated lessons:  {len(outdated)}")
        print(f"Successfully updated:    {updated_count}")
        print(f"Failed to update:        {failed_count}")
        print()

        if updated_count > 0:
            print("[OK]    Database has been updated!")
            print()
            print("NEXT STEPS:")
            print("  1. Verify changes: python compare_lessons_to_db.py")
            print("  2. Update template: python update_template_database.py")
            print("  3. Commit changes: git add cyberlearn_template.db")
        else:
            print("[WARN]  No lessons were updated")

        print()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
