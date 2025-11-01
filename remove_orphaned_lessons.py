#!/usr/bin/env python3
"""
Sync Database with Lesson Files

This script:
1. Identifies and removes orphaned lessons (in database but no JSON file)
2. Detects modified lessons (JSON file changed after database entry)
3. Offers to reload modified lessons

Usage:
    python remove_orphaned_lessons.py                    # Dry run (show what would change)
    python remove_orphaned_lessons.py --confirm          # Delete orphaned + reload modified
    python remove_orphaned_lessons.py --orphaned-only    # Only remove orphaned lessons
"""

import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path(__file__).parent / 'content'
DB_PATH = "cyberlearn_template.db"  # Use template database


def get_lesson_files():
    """Get mapping of lesson_id -> file info from JSON files"""
    lesson_files = {}

    for filepath in CONTENT_DIR.glob('lesson_*.json'):
        try:
            # Get file modification time
            mtime = filepath.stat().st_mtime

            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)
                lesson_id = lesson.get('lesson_id')

                if lesson_id:
                    lesson_files[lesson_id] = {
                        'filepath': filepath,
                        'mtime': mtime,
                        'domain': lesson.get('domain'),
                        'title': lesson.get('title'),
                        'order_index': lesson.get('order_index')
                    }
        except Exception as e:
            print(f"[WARNING] Error reading {filepath.name}: {e}")

    return lesson_files


def find_orphaned_lessons(conn, lesson_files):
    """Find lessons in database that don't have JSON files"""
    cursor = conn.cursor()
    cursor.execute("SELECT lesson_id, domain, title, order_index FROM lessons")
    all_lessons = cursor.fetchall()

    orphaned = []
    for lesson in all_lessons:
        lesson_id, domain, title, order_index = lesson
        if lesson_id not in lesson_files:
            orphaned.append({
                'lesson_id': lesson_id,
                'domain': domain,
                'title': title,
                'order_index': order_index
            })

    return orphaned


def find_modified_lessons(conn, lesson_files):
    """Find lessons where JSON file is newer than database entry"""
    cursor = conn.cursor()

    # Get lessons with their last update time from database
    cursor.execute("""
        SELECT lesson_id, domain, title, order_index, updated_at
        FROM lessons
        WHERE lesson_id IN ({})
    """.format(','.join('?' * len(lesson_files))), list(lesson_files.keys()))

    db_lessons = cursor.fetchall()

    modified = []
    for db_lesson in db_lessons:
        lesson_id, domain, title, order_index, updated_at = db_lesson

        if lesson_id not in lesson_files:
            continue

        file_info = lesson_files[lesson_id]

        # Parse database timestamp (format: "2025-10-31 12:34:56")
        if updated_at:
            try:
                db_time = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S").timestamp()
            except:
                # If parsing fails, assume modified
                db_time = 0
        else:
            db_time = 0

        # If file is newer than database entry
        if file_info['mtime'] > db_time:
            modified.append({
                'lesson_id': lesson_id,
                'domain': file_info['domain'],
                'title': file_info['title'],
                'order_index': file_info['order_index'],
                'filepath': file_info['filepath'],
                'file_mtime': datetime.fromtimestamp(file_info['mtime']).strftime("%Y-%m-%d %H:%M:%S"),
                'db_mtime': updated_at or 'Never'
            })

    return modified


def reload_lesson(conn, lesson_id, filepath):
    """Reload a lesson from JSON file into database"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        cursor = conn.cursor()

        # Update lesson in database
        cursor.execute("""
            UPDATE lessons
            SET
                domain = ?,
                title = ?,
                difficulty = ?,
                order_index = ?,
                estimated_time = ?,
                lesson_content = ?,
                updated_at = datetime('now')
            WHERE lesson_id = ?
        """, (
            lesson.get('domain'),
            lesson.get('title'),
            lesson.get('difficulty'),
            lesson.get('order_index'),
            lesson.get('estimated_time'),
            json.dumps(lesson),
            lesson_id
        ))

        return True
    except Exception as e:
        print(f"[ERROR] Failed to reload {filepath.name}: {e}")
        return False


def sync_database(confirm=False, orphaned_only=False):
    """Sync database with lesson files"""
    conn = sqlite3.connect(DB_PATH)

    try:
        print("Scanning lesson files and database...")
        print(f"Content directory: {CONTENT_DIR}")
        print(f"Database: {DB_PATH}")
        print()

        # Get all lesson files
        lesson_files = get_lesson_files()
        print(f"Found {len(lesson_files)} lesson files in content/")

        # Find orphaned lessons
        orphaned = find_orphaned_lessons(conn, lesson_files)

        # Find modified lessons (unless orphaned-only mode)
        modified = [] if orphaned_only else find_modified_lessons(conn, lesson_files)

        print()
        print("=" * 80)

        # Report orphaned lessons
        if orphaned:
            print(f"[ORPHANED] {len(orphaned)} lesson(s) in database without JSON files:")
            print("-" * 80)
            for lesson in orphaned:
                print(f"  - [{lesson['domain']}] {lesson['title']}")
                print(f"    lesson_id: {lesson['lesson_id']}")
                print(f"    order_index: {lesson['order_index']}")
                print()
        else:
            print("[OK] No orphaned lessons found")

        print("=" * 80)

        # Report modified lessons
        if not orphaned_only:
            if modified:
                print(f"[MODIFIED] {len(modified)} lesson(s) with newer JSON files:")
                print("-" * 80)
                for lesson in modified:
                    print(f"  - [{lesson['domain']}] {lesson['title']}")
                    print(f"    File modified: {lesson['file_mtime']}")
                    print(f"    DB updated:    {lesson['db_mtime']}")
                    print()
            else:
                print("[OK] No modified lessons found")

            print("=" * 80)

        # If nothing to do
        if not orphaned and not modified:
            print()
            print("[OK] Database is in sync with lesson files!")
            return

        # Dry run mode
        if not confirm:
            print()
            print("[DRY RUN] No changes made")
            print()
            print("Actions that would be performed:")
            if orphaned:
                print(f"  - Delete {len(orphaned)} orphaned lesson(s)")
            if modified and not orphaned_only:
                print(f"  - Reload {len(modified)} modified lesson(s)")
            print()
            print("To actually perform these actions, run:")
            if orphaned_only:
                print("  python remove_orphaned_lessons.py --orphaned-only --confirm")
            else:
                print("  python remove_orphaned_lessons.py --confirm")
            return

        # Confirm actions
        print()
        actions = []
        if orphaned:
            actions.append(f"delete {len(orphaned)} orphaned lesson(s)")
        if modified and not orphaned_only:
            actions.append(f"reload {len(modified)} modified lesson(s)")

        response = input(f"Proceed to {' and '.join(actions)}? (yes/no): ").strip().lower()

        if response != 'yes':
            print("Cancelled. No changes made.")
            return

        # Delete orphaned lessons
        if orphaned:
            print()
            print("Deleting orphaned lessons...")
            cursor = conn.cursor()
            deleted_count = 0

            for lesson in orphaned:
                try:
                    # Delete from lesson_tags first (foreign key constraint)
                    cursor.execute("DELETE FROM lesson_tags WHERE lesson_id = ?", (lesson['lesson_id'],))

                    # Delete from lessons table
                    cursor.execute("DELETE FROM lessons WHERE lesson_id = ?", (lesson['lesson_id'],))

                    deleted_count += 1
                    print(f"[OK] Deleted: [{lesson['domain']}] {lesson['title']}")
                except Exception as e:
                    print(f"[ERROR] Error deleting {lesson['title']}: {e}")

            conn.commit()
            print(f"Successfully deleted {deleted_count} orphaned lesson(s).")

        # Reload modified lessons
        if modified and not orphaned_only:
            print()
            print("Reloading modified lessons...")
            reloaded_count = 0

            for lesson in modified:
                if reload_lesson(conn, lesson['lesson_id'], lesson['filepath']):
                    reloaded_count += 1
                    print(f"[OK] Reloaded: [{lesson['domain']}] {lesson['title']}")

            conn.commit()
            print(f"Successfully reloaded {reloaded_count} modified lesson(s).")

        print()
        print("[DONE] Database sync complete!")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Sync database with lesson files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python remove_orphaned_lessons.py                    # Dry run (show what would change)
  python remove_orphaned_lessons.py --confirm          # Delete orphaned + reload modified
  python remove_orphaned_lessons.py --orphaned-only    # Only check/remove orphaned lessons
        """
    )
    parser.add_argument(
        '--confirm',
        action='store_true',
        help='Actually perform changes (default is dry run)'
    )
    parser.add_argument(
        '--orphaned-only',
        action='store_true',
        help='Only remove orphaned lessons, skip modified lesson detection'
    )

    args = parser.parse_args()

    sync_database(confirm=args.confirm, orphaned_only=args.orphaned_only)


if __name__ == '__main__':
    main()
