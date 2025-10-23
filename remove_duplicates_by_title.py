#!/usr/bin/env python3
"""
Remove duplicate lessons from the database based on title.
Keeps the most recent version of each title.
"""

import sqlite3
from pathlib import Path

def remove_duplicates_by_title():
    """Remove duplicate lessons by title"""

    db_path = Path('cyberlearn.db')

    if not db_path.exists():
        print("[ERROR] Database not found: cyberlearn.db")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 80)
    print("REMOVING DUPLICATE LESSONS BY TITLE")
    print("=" * 80)
    print()

    # Find duplicates by title
    cursor.execute("""
        SELECT title, COUNT(*) as count
        FROM lessons
        GROUP BY title
        HAVING count > 1
        ORDER BY count DESC, title
    """)

    duplicates = cursor.fetchall()

    if not duplicates:
        print("[SUCCESS] No duplicate lesson titles found!")
        conn.close()
        return

    print(f"Found {len(duplicates)} lesson titles with duplicates")
    print()

    total_removed = 0

    for dup in duplicates:
        title = dup['title']
        count = dup['count']

        print(f"[DUPLICATE] {title}")
        print(f"  Count: {count} copies")

        # Get all rows with this title
        cursor.execute("""
            SELECT rowid, lesson_id, created_at, updated_at
            FROM lessons
            WHERE title = ?
            ORDER BY updated_at DESC, created_at DESC
        """, (title,))

        rows = cursor.fetchall()

        # Keep the first one (most recent), delete the rest
        keep_rowid = rows[0]['rowid']
        keep_id = rows[0]['lesson_id']
        print(f"  Keeping: rowid={keep_rowid}, lesson_id={keep_id[:8]}... (most recent)")

        for row in rows[1:]:
            rowid = row['rowid']
            lesson_id = row['lesson_id']
            print(f"  Deleting: rowid={rowid}, lesson_id={lesson_id[:8]}...")
            cursor.execute("DELETE FROM lessons WHERE rowid = ?", (rowid,))
            total_removed += 1

        print()

    # Commit changes
    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(DISTINCT title) as unique_titles FROM lessons")
    unique_titles = cursor.fetchone()['unique_titles']

    conn.close()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Removed: {total_removed} duplicate entries")
    print(f"Total lessons in database: {total}")
    print(f"Unique titles: {unique_titles}")

    if total == unique_titles:
        print()
        print("[SUCCESS] All duplicates removed! Database is clean.")
    else:
        print()
        print("[WARNING] Some duplicates may remain. Run again if needed.")
    print("=" * 80)

if __name__ == '__main__':
    remove_duplicates_by_title()
