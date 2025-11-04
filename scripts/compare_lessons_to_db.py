"""
Compare lesson files in content/ directory with lessons in the template database.

This script ensures:
1. All lessons in DB exist as files
2. All lesson files exist in DB
3. All lessons in DB are at their latest version (match file content)
4. No extra lessons in DB that don't have corresponding files

Usage:
    python compare_lessons_to_db.py
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Database configuration
# You can check either database:
# - cyberlearn.db (working database on dev machine)
# - cyberlearn_template.db (template to be deployed to VMs)
DB_PATH = "cyberlearn_template.db"
CONTENT_DIR = Path("content")

def load_lesson_from_file(file_path: Path) -> Dict:
    """Load and parse a lesson JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_lesson_files() -> Dict[str, Tuple[Path, Dict]]:
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
            else:
                print(f"[WARN]  {file_path.name} has no lesson_id")

        except Exception as e:
            print(f"[ERROR] Failed to load {file_path.name}: {e}")

    return lesson_files

def get_all_db_lessons(conn: sqlite3.Connection) -> Dict[str, Dict]:
    """Get all lessons from database.

    Returns:
        Dict mapping lesson_id to lesson data dict
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT lesson_id, title, domain, difficulty, order_index,
               estimated_time, prerequisites, learning_objectives,
               jim_kwik_principles, content_blocks, post_assessment
        FROM lessons
    """)

    lessons = {}
    for row in cursor.fetchall():
        lesson_id = row[0]
        lessons[lesson_id] = {
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

    return lessons

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
                differences.append(f"  - {field}: Lists don't match")
        elif file_value != db_value:
            differences.append(f"  - {field}: File='{file_value}' vs DB='{db_value}'")

    # Compare content blocks count
    file_blocks = len(file_data.get('content_blocks', []))
    db_blocks = len(db_lesson.get('content_blocks', []))

    if file_blocks != db_blocks:
        differences.append(f"  - content_blocks: File has {file_blocks} blocks, DB has {db_blocks} blocks")

    # Compare post_assessment count
    file_assessments = len(file_data.get('post_assessment', []))
    db_assessments = len(db_lesson.get('post_assessment', []))

    if file_assessments != db_assessments:
        differences.append(f"  - post_assessment: File has {file_assessments} questions, DB has {db_assessments} questions")

    return differences

def main():
    """Main comparison logic."""
    print("=" * 80)
    print("LESSON FILES vs DATABASE COMPARISON")
    print("=" * 80)
    print()

    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at {DB_PATH}")
        return

    # Check if content directory exists
    if not CONTENT_DIR.exists():
        print(f"[ERROR] Content directory not found at {CONTENT_DIR}")
        return

    # Load lesson files
    print("[FILES] Loading lesson files from content/...")
    lesson_files = get_all_lesson_files()
    print(f"        Found {len(lesson_files)} lesson files")
    print()

    # Connect to database
    print("[DB]    Connecting to database...")
    conn = sqlite3.connect(DB_PATH)

    try:
        db_lessons = get_all_db_lessons(conn)
        print(f"   Found {len(db_lessons)} lessons in database")
        print()

        # Get lesson IDs
        file_ids = set(lesson_files.keys())
        db_ids = set(db_lessons.keys())

        # Find differences
        only_in_files = file_ids - db_ids
        only_in_db = db_ids - file_ids
        in_both = file_ids & db_ids

        # Report: Lessons only in files (missing from DB)
        if only_in_files:
            print("[ERROR] MISSING FROM DATABASE:")
            print(f"        {len(only_in_files)} lessons exist as files but NOT in database")
            print()
            for lesson_id in sorted(only_in_files):
                file_path, lesson_data = lesson_files[lesson_id]
                title = lesson_data.get('title', 'Unknown')
                domain = lesson_data.get('domain', 'Unknown')
                print(f"        - {file_path.name}")
                print(f"          ID: {lesson_id}")
                print(f"          Title: {title}")
                print(f"          Domain: {domain}")
                print()
        else:
            print("[OK]    All lesson files are present in database")
            print()

        # Report: Lessons only in DB (missing files)
        if only_in_db:
            print("[ERROR] EXTRA IN DATABASE:")
            print(f"        {len(only_in_db)} lessons exist in database but NO corresponding files")
            print()
            for lesson_id in sorted(only_in_db):
                db_lesson = db_lessons[lesson_id]
                print(f"        - Lesson ID: {lesson_id}")
                print(f"          Title: {db_lesson['title']}")
                print(f"          Domain: {db_lesson['domain']}")
                print(f"          Order: {db_lesson['order_index']}")
                print()
        else:
            print("[OK]    No extra lessons in database (all have corresponding files)")
            print()

        # Report: Content version mismatches
        print("[CHECK] Checking content versions...")
        print(f"        Comparing {len(in_both)} lessons that exist in both file and database...")
        print()

        outdated_count = 0
        for lesson_id in sorted(in_both):
            file_path, file_data = lesson_files[lesson_id]
            db_lesson = db_lessons[lesson_id]

            differences = compare_lesson_content(file_data, db_lesson)

            if differences:
                outdated_count += 1
                print(f"[WARN]  OUTDATED: {file_path.name}")
                print(f"        ID: {lesson_id}")
                print(f"        Title: {file_data.get('title')}")
                print(f"        Differences found:")
                for diff in differences:
                    print(f"        {diff}")
                print()

        if outdated_count == 0:
            print("[OK]    All lessons in database are at their latest version")
            print()
        else:
            print(f"[ERROR] {outdated_count} lessons in database are OUTDATED")
            print()

        # Summary
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total lesson files:           {len(lesson_files)}")
        print(f"Total lessons in database:    {len(db_lessons)}")
        print(f"Lessons in both:              {len(in_both)}")
        print(f"Missing from database:        {len(only_in_files)}")
        print(f"Extra in database (no file):  {len(only_in_db)}")
        print(f"Outdated in database:         {outdated_count}")
        print()

        # Overall status
        if only_in_files or only_in_db or outdated_count > 0:
            print("[ERROR] DATABASE IS OUT OF SYNC")
            print()
            print("RECOMMENDED ACTIONS:")
            if only_in_files:
                print("  1. Run: python load_all_lessons.py")
                print("     (This will add missing lessons to database)")
            if only_in_db:
                print("  2. Manually review and remove extra lessons from database")
                print("     (Or delete cyberlearn_template.db and reload from scratch)")
            if outdated_count > 0:
                print("  3. Run: python update_outdated_lessons.py")
                print("     (This will update outdated lessons)")
            print()
            print("  4. After fixes, run: python update_template_database.py")
            print("  5. Commit updated template: git add cyberlearn_template.db")
        else:
            print("[OK]    DATABASE IS IN SYNC")
            print("        All lesson files match database content perfectly!")
        print()

    finally:
        conn.close()

if __name__ == "__main__":
    main()
