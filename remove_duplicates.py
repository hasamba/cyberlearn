#!/usr/bin/env python3
"""
Remove duplicate lessons from the database.
Keeps the most recent version of each lesson based on lesson_id.
"""

import sqlite3
from pathlib import Path
from collections import defaultdict

def remove_duplicates():
    """Remove duplicate lessons from database"""

    db_path = Path('cyberlearn.db')

    if not db_path.exists():
        print("[ERROR] Database not found: cyberlearn.db")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find duplicates
    cursor.execute("""
        SELECT lesson_id, title, COUNT(*) as count
        FROM lessons
        GROUP BY lesson_id
        HAVING count > 1
        ORDER BY count DESC, title
    """)

    duplicates = cursor.fetchall()

    if not duplicates:
        print("[SUCCESS] No duplicate lessons found!")
        conn.close()
        return

    print("=" * 80)
    print(f"Found {len(duplicates)} lessons with duplicates")
    print("=" * 80)
    print()

    total_removed = 0

    for dup in duplicates:
        lesson_id = dup['lesson_id']
        title = dup['title']
        count = dup['count']

        print(f"[DUPLICATE] {title}")
        print(f"  Lesson ID: {lesson_id}")
        print(f"  Count: {count} copies")

        # Get all rows with this lesson_id
        cursor.execute("""
            SELECT rowid, created_at, updated_at
            FROM lessons
            WHERE lesson_id = ?
            ORDER BY updated_at DESC, created_at DESC
        """, (lesson_id,))

        rows = cursor.fetchall()

        # Keep the first one (most recent), delete the rest
        keep_rowid = rows[0]['rowid']
        print(f"  Keeping: rowid={keep_rowid} (most recent)")

        for row in rows[1:]:
            rowid = row['rowid']
            print(f"  Deleting: rowid={rowid}")
            cursor.execute("DELETE FROM lessons WHERE rowid = ?", (rowid,))
            total_removed += 1

        print()

    # Commit changes
    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(DISTINCT lesson_id) as unique_count
        FROM lessons
    """)
    unique = cursor.fetchone()['unique_count']

    conn.close()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Removed: {total_removed} duplicate entries")
    print(f"Total lessons in database: {total}")
    print(f"Unique lessons: {unique}")

    if total == unique:
        print()
        print("[SUCCESS] All duplicates removed! Database is clean.")
    else:
        print()
        print("[WARNING] Some duplicates may remain. Run again if needed.")
    print("=" * 80)

if __name__ == '__main__':
    remove_duplicates()
