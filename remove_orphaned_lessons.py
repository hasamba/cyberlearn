#!/usr/bin/env python3
"""
Remove Orphaned Lessons from Database

This script identifies and removes lessons from the database that no longer
have corresponding JSON files in the content/ directory.

Usage:
    python remove_orphaned_lessons.py           # Dry run (show what would be deleted)
    python remove_orphaned_lessons.py --confirm # Actually delete orphaned lessons
"""

import sys
import argparse
from pathlib import Path
from database import SessionLocal, Lesson

CONTENT_DIR = Path(__file__).parent / 'content'


def get_existing_lesson_ids():
    """Get set of lesson_ids from JSON files in content/"""
    import json

    existing_ids = set()

    for filepath in CONTENT_DIR.glob('lesson_*.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)
                lesson_id = lesson.get('lesson_id')
                if lesson_id:
                    existing_ids.add(lesson_id)
        except Exception as e:
            print(f"[WARNING] Error reading {filepath.name}: {e}")

    return existing_ids


def find_orphaned_lessons(db):
    """Find lessons in database that don't have JSON files"""
    existing_ids = get_existing_lesson_ids()
    all_lessons = db.query(Lesson).all()

    orphaned = []
    for lesson in all_lessons:
        if lesson.lesson_id not in existing_ids:
            orphaned.append(lesson)

    return orphaned


def remove_orphaned_lessons(confirm=False):
    """Remove orphaned lessons from database"""
    db = SessionLocal()

    try:
        print("Scanning for orphaned lessons...")
        print(f"Content directory: {CONTENT_DIR}")
        print()

        orphaned = find_orphaned_lessons(db)

        if not orphaned:
            print("✅ No orphaned lessons found! Database is clean.")
            return

        print(f"Found {len(orphaned)} orphaned lesson(s):")
        print("=" * 80)

        for lesson in orphaned:
            print(f"  - [{lesson.domain}] {lesson.title}")
            print(f"    lesson_id: {lesson.lesson_id}")
            print(f"    order_index: {lesson.order_index}")
            print()

        print("=" * 80)

        if not confirm:
            print()
            print("⚠️  DRY RUN MODE - No changes made")
            print()
            print("To actually delete these lessons, run:")
            print("  python remove_orphaned_lessons.py --confirm")
            return

        # Confirm deletion
        print()
        response = input(f"Delete {len(orphaned)} orphaned lesson(s)? (yes/no): ").strip().lower()

        if response != 'yes':
            print("Cancelled. No changes made.")
            return

        # Delete orphaned lessons
        deleted_count = 0
        for lesson in orphaned:
            try:
                db.delete(lesson)
                deleted_count += 1
                print(f"✅ Deleted: [{lesson.domain}] {lesson.title}")
            except Exception as e:
                print(f"❌ Error deleting {lesson.title}: {e}")

        db.commit()

        print()
        print(f"Successfully deleted {deleted_count} orphaned lesson(s).")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description='Remove orphaned lessons from database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python remove_orphaned_lessons.py           # Dry run (show what would be deleted)
  python remove_orphaned_lessons.py --confirm # Actually delete orphaned lessons
        """
    )
    parser.add_argument(
        '--confirm',
        action='store_true',
        help='Actually delete orphaned lessons (default is dry run)'
    )

    args = parser.parse_args()

    remove_orphaned_lessons(confirm=args.confirm)


if __name__ == '__main__':
    main()
