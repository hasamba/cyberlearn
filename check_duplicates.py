#!/usr/bin/env python3
"""
Check for duplicate lessons in the database.
Checks both lesson_id duplicates and title duplicates.
"""

import sqlite3
from pathlib import Path

def check_duplicates():
    """Check for duplicate lessons"""

    db_path = Path('cyberlearn.db')

    if not db_path.exists():
        print("[ERROR] Database not found: cyberlearn.db")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 80)
    print("CHECKING FOR DUPLICATES")
    print("=" * 80)
    print()

    # Check 1: Duplicate lesson_ids
    print("[1] Checking for duplicate lesson_ids...")
    cursor.execute("""
        SELECT lesson_id, title, COUNT(*) as count
        FROM lessons
        GROUP BY lesson_id
        HAVING count > 1
        ORDER BY count DESC, title
    """)

    id_duplicates = cursor.fetchall()

    if id_duplicates:
        print(f"  Found {len(id_duplicates)} lesson_ids with duplicates:")
        for dup in id_duplicates:
            print(f"    - {dup['title']} (ID: {dup['lesson_id'][:8]}..., {dup['count']} copies)")
    else:
        print("  ✓ No duplicate lesson_ids found")
    print()

    # Check 2: Duplicate titles
    print("[2] Checking for duplicate titles...")
    cursor.execute("""
        SELECT title, COUNT(*) as count, GROUP_CONCAT(lesson_id) as ids
        FROM lessons
        GROUP BY title
        HAVING count > 1
        ORDER BY count DESC, title
    """)

    title_duplicates = cursor.fetchall()

    if title_duplicates:
        print(f"  Found {len(title_duplicates)} titles with duplicates:")
        for dup in title_duplicates:
            print(f"    - '{dup['title']}' ({dup['count']} copies)")
            ids = dup['ids'].split(',')
            for lesson_id in ids:
                print(f"      * {lesson_id}")
    else:
        print("  ✓ No duplicate titles found")
    print()

    # Check 3: Total counts
    print("[3] Database statistics...")
    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(DISTINCT lesson_id) as unique_ids FROM lessons")
    unique_ids = cursor.fetchone()['unique_ids']

    cursor.execute("SELECT COUNT(DISTINCT title) as unique_titles FROM lessons")
    unique_titles = cursor.fetchone()['unique_titles']

    print(f"  Total entries: {total}")
    print(f"  Unique lesson_ids: {unique_ids}")
    print(f"  Unique titles: {unique_titles}")
    print()

    # Check 4: List all lessons by domain
    print("[4] Lessons by domain...")
    cursor.execute("""
        SELECT domain, title, lesson_id, order_index
        FROM lessons
        ORDER BY domain, order_index, title
    """)

    lessons = cursor.fetchall()
    current_domain = None

    for lesson in lessons:
        if lesson['domain'] != current_domain:
            current_domain = lesson['domain']
            print(f"\n  {current_domain.upper()}:")
        print(f"    {lesson['order_index']:2d}. {lesson['title'][:60]}")

    conn.close()

    print()
    print("=" * 80)

    if id_duplicates or title_duplicates:
        print("[ACTION NEEDED] Duplicates found! Run remove_duplicates_by_title.py")
    else:
        print("[SUCCESS] No duplicates found!")

    print("=" * 80)

if __name__ == '__main__':
    check_duplicates()
