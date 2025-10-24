#!/usr/bin/env python3
"""
Remove placeholder (non-RICH) lesson files.
These are old template lessons that cause duplicates in the database.
"""

from pathlib import Path
import shutil

def remove_placeholder_lessons():
    """Remove all non-RICH lesson files"""

    content_dir = Path('content')

    # Find all non-RICH lesson files
    all_lessons = list(content_dir.glob('lesson_*.json'))
    placeholder_lessons = [f for f in all_lessons if '_RICH.json' not in f.name]

    if not placeholder_lessons:
        print("[SUCCESS] No placeholder lessons found!")
        return

    print("=" * 80)
    print("REMOVING PLACEHOLDER LESSON FILES")
    print("=" * 80)
    print()
    print(f"Found {len(placeholder_lessons)} placeholder lessons to remove")
    print()

    # Create backup directory
    backup_dir = Path('content/backup_placeholders')
    backup_dir.mkdir(exist_ok=True)

    removed_count = 0

    for filepath in sorted(placeholder_lessons):
        # Move to backup instead of deleting (safer)
        backup_path = backup_dir / filepath.name
        shutil.move(str(filepath), str(backup_path))
        print(f"[MOVED] {filepath.name} → backup_placeholders/")
        removed_count += 1

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Placeholder lessons moved to backup: {removed_count}")
    print(f"Backup location: {backup_dir}")
    print()
    print("[NEXT STEP] Reload lessons to remove duplicates:")
    print("  python load_all_lessons.py")
    print()
    print("[NEXT STEP] Remove duplicates from database:")
    print("  python remove_duplicates_by_title.py")
    print("=" * 80)

if __name__ == '__main__':
    remove_placeholder_lessons()
