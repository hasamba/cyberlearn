#!/usr/bin/env python3
"""
Sync database with lesson files in content/ directory.
Removes lessons from database that no longer have corresponding JSON files.
"""

import json
import sqlite3
from pathlib import Path

def get_lesson_files():
    """Get all lesson IDs from JSON files"""
    content_dir = Path('content')
    lesson_files = content_dir.glob('lesson_*.json')

    file_lesson_ids = set()
    file_titles = {}

    for filepath in lesson_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lesson_id = data.get('lesson_id')
                title = data.get('title', 'Unknown')
                if lesson_id:
                    file_lesson_ids.add(str(lesson_id))
                    file_titles[str(lesson_id)] = title
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")

    return file_lesson_ids, file_titles

def get_database_lessons():
    """Get all lessons from database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    cursor.execute("SELECT lesson_id, title FROM lessons")
    db_lessons = cursor.fetchall()

    db_lesson_ids = {lesson_id: title for lesson_id, title in db_lessons}

    conn.close()
    return db_lesson_ids

def sync_database():
    """Remove lessons from database that don't have corresponding files"""
    print("="*70)
    print("Database Sync - Remove orphaned lessons")
    print("="*70)

    # Get lesson IDs from files
    print("\nScanning content/ directory for lesson files...")
    file_lesson_ids, file_titles = get_lesson_files()
    print(f"Found {len(file_lesson_ids)} lesson files")

    # Get lesson IDs from database
    print("\nQuerying database for existing lessons...")
    db_lesson_ids = get_database_lessons()
    print(f"Found {len(db_lesson_ids)} lessons in database")

    # Find orphaned lessons (in DB but no file)
    orphaned = set(db_lesson_ids.keys()) - file_lesson_ids

    if not orphaned:
        print("\n" + "="*70)
        print("✓ Database is in sync - no orphaned lessons found")
        print("="*70)
        return

    print(f"\n{'='*70}")
    print(f"Found {len(orphaned)} orphaned lessons (in DB but no file):")
    print(f"{'='*70}")

    for lesson_id in sorted(orphaned):
        title = db_lesson_ids[lesson_id]
        print(f"  - {title[:60]:<60} [{lesson_id[:8]}...]")

    # Ask for confirmation
    print(f"\n{'='*70}")
    response = input(f"Delete these {len(orphaned)} lessons from database? (yes/no): ")

    if response.lower() not in ['yes', 'y']:
        print("Aborted - no changes made")
        return

    # Delete orphaned lessons
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    deleted_count = 0
    for lesson_id in orphaned:
        try:
            cursor.execute("DELETE FROM lessons WHERE lesson_id = ?", (lesson_id,))
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {lesson_id}: {e}")

    conn.commit()
    conn.close()

    print(f"\n{'='*70}")
    print(f"✓ Deleted {deleted_count} orphaned lessons from database")
    print(f"{'='*70}")

    # Show updated stats
    print("\nUpdated database:")
    remaining = len(db_lesson_ids) - deleted_count
    print(f"  Total lessons: {remaining}")
    print(f"  Lessons with files: {len(file_lesson_ids)}")

    # Show lessons in files but not in DB (need to be loaded)
    missing = file_lesson_ids - set(db_lesson_ids.keys())
    if missing:
        print(f"\n⚠️  {len(missing)} lessons in files but not in database:")
        for lesson_id in list(missing)[:5]:  # Show first 5
            title = file_titles.get(lesson_id, 'Unknown')
            print(f"     - {title}")
        if len(missing) > 5:
            print(f"     ... and {len(missing)-5} more")
        print("\n   Run: python load_all_lessons.py")

def main():
    sync_database()

if __name__ == "__main__":
    main()
