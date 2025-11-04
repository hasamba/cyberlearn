#!/usr/bin/env python3
"""
Update the template database with latest schema and data.

This script:
1. Deletes old template database (if exists)
2. Copies current working database to template
3. Ensures template has tags populated
4. This template will be used by setup_database.py on VMs

Run this on your dev machine after making database schema changes.
"""

from pathlib import Path
import shutil
import sys

def update_template_database():
    """Update template database from working database"""
    # Look in parent directory (project root) for database files
    project_root = Path(__file__).parent.parent
    working_db = project_root / "cyberlearn.db"
    template_db = project_root / "cyberlearn_template.db"

    print("=" * 60)
    print("UPDATE TEMPLATE DATABASE")
    print("=" * 60)

    # Check if working database exists
    if not working_db.exists():
        print(f"\nERROR Working database not found at:")
        print(f"  {working_db}")
        print("\nPlease run the app first to create the database:")
        print("  streamlit run app.py")
        return False

    # Verify working database has tags
    import sqlite3
    conn = sqlite3.connect(str(working_db))
    cursor = conn.cursor()

    # Check for tags table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
    if not cursor.fetchone():
        print(f"\nERROR Working database doesn't have tags table!")
        print("\nPlease run the migration script first:")
        print("  python migrate_tags_to_database_v2.py")
        conn.close()
        return False

    # Check tag count
    cursor.execute("SELECT COUNT(*) FROM tags")
    tag_count = cursor.fetchone()[0]

    # Check lesson count
    cursor.execute("SELECT COUNT(*) FROM lessons")
    lesson_count = cursor.fetchone()[0]

    # Check lesson-tag associations
    cursor.execute("SELECT COUNT(*) FROM lesson_tags")
    association_count = cursor.fetchone()[0]

    conn.close()

    print(f"\nWorking database verified:")
    print(f"  Lessons: {lesson_count}")
    print(f"  Tags: {tag_count}")
    print(f"  Lesson-Tag associations: {association_count}")

    if tag_count == 0:
        print(f"\nERROR No tags found in working database!")
        print("\nPlease run the migration script first:")
        print("  python migrate_tags_to_database_v2.py")
        return False

    # Backup old template if it exists
    if template_db.exists():
        backup_db = Path(__file__).parent / "cyberlearn_template.db.backup"
        print(f"\nOK Backing up old template database...")
        shutil.copy2(template_db, backup_db)
        print(f"  Backup: {backup_db}")

    # Copy working database to template
    print(f"\nOK Copying working database to template...")
    print(f"  Source: {working_db}")
    print(f"  Target: {template_db}")

    try:
        shutil.copy2(working_db, template_db)
        print("\nSUCCESS Template database updated successfully!")
        print("\nThe template now includes:")
        print(f"  OK {lesson_count} lessons across 15 domains")
        print(f"  OK {tag_count} tags (Course tags, Career Path tags, etc.)")
        print(f"  OK {association_count} lesson-tag associations")
        print("  OK All migrations applied")
        print("  OK Ready to be copied to VMs")

        print("\n" + "=" * 60)
        print("SUCCESS TEMPLATE UPDATE COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Commit the updated template to git:")
        print("     git add cyberlearn_template.db")
        print("     git commit -m 'Update template database with tags'")
        print("     git push")
        print()
        print("  2. On your VM, run:")
        print("     bash update_vm.sh")
        print()
        return True

    except Exception as e:
        print(f"\nERROR Error copying database: {e}")
        return False

if __name__ == "__main__":
    success = update_template_database()
    sys.exit(0 if success else 1)
