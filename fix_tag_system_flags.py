#!/usr/bin/env python3
"""
Fix tag is_system flags.

Problem: All tags are marked as is_system=1, even custom user tags.
Solution: Only Career Path, Course, and Package tags should be system tags.
          All other tags (category='Custom') should be user tags (is_system=0).
"""

import sqlite3
from pathlib import Path

def fix_tag_system_flags(db_path: str = "cyberlearn.db"):
    """Update is_system flags based on tag category"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Fixing tag is_system flags in {db_path}...")

    # Get current status
    cursor.execute("SELECT COUNT(*) as total FROM tags")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as system FROM tags WHERE is_system = 1")
    system_before = cursor.fetchone()['system']

    cursor.execute("SELECT COUNT(*) as user FROM tags WHERE is_system = 0")
    user_before = cursor.fetchone()['user']

    print(f"\nBefore fix:")
    print(f"  Total tags: {total}")
    print(f"  System tags (is_system=1): {system_before}")
    print(f"  User tags (is_system=0): {user_before}")

    # Fix: Set is_system based on category
    # System tags: Career Path, Course, Package
    # User tags: Custom (and anything else)

    # Mark Career Path, Course, Package as system tags
    cursor.execute("""
        UPDATE tags
        SET is_system = 1
        WHERE category IN ('Career Path', 'Course', 'Package')
    """)
    system_updated = cursor.rowcount

    # Mark all other tags as user tags
    cursor.execute("""
        UPDATE tags
        SET is_system = 0
        WHERE category NOT IN ('Career Path', 'Course', 'Package')
    """)
    user_updated = cursor.rowcount

    conn.commit()

    # Get new status
    cursor.execute("SELECT COUNT(*) as system FROM tags WHERE is_system = 1")
    system_after = cursor.fetchone()['system']

    cursor.execute("SELECT COUNT(*) as user FROM tags WHERE is_system = 0")
    user_after = cursor.fetchone()['user']

    print(f"\nAfter fix:")
    print(f"  System tags (is_system=1): {system_after} (updated {system_updated})")
    print(f"  User tags (is_system=0): {user_after} (updated {user_updated})")

    # Show breakdown by category
    print(f"\nBreakdown by category:")
    cursor.execute("""
        SELECT category, is_system, COUNT(*) as count
        FROM tags
        GROUP BY category, is_system
        ORDER BY category, is_system
    """)

    for row in cursor.fetchall():
        tag_type = "system" if row['is_system'] else "user"
        print(f"  {row['category']:20} | {tag_type:10} | {row['count']} tags")

    # Show some examples
    print(f"\nSample tags:")
    cursor.execute("""
        SELECT name, category, is_system
        FROM tags
        ORDER BY is_system DESC, category, name
        LIMIT 15
    """)

    for row in cursor.fetchall():
        tag_type = "SYSTEM" if row['is_system'] else "USER  "
        print(f"  [{tag_type}] {row['name']:50} ({row['category']})")

    conn.close()
    print(f"\n✅ Tag system flags fixed successfully!")
    return True

if __name__ == "__main__":
    # Fix main database
    fix_tag_system_flags("cyberlearn.db")

    # Also fix template database
    template_db = Path("cyberlearn_template.db")
    if template_db.exists():
        print("\n" + "="*80)
        fix_tag_system_flags("cyberlearn_template.db")
