"""
Bulk tag lessons with specific tags.

Usage:
    python bulk_tag_lessons.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def bulk_tag_lessons():
    """Tag specific lessons with specific tags."""

    db_path = Path(__file__).parent.parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if tags exist
        cursor.execute("SELECT tag_id, name FROM tags WHERE name IN ('Course: PEN-200', 'APT')")
        existing_tags = {name: tag_id for tag_id, name in cursor.fetchall()}

        if 'Course: PEN-200' not in existing_tags:
            print("❌ Tag 'Course: PEN-200' not found in database")
            print("   Please create this tag first in the Tag Management page")
            return

        if 'APT' not in existing_tags:
            print("❌ Tag 'APT' not found in database")
            print("   Please create this tag first in the Tag Management page")
            return

        pen200_tag_id = existing_tags['Course: PEN-200']
        apt_tag_id = existing_tags['APT']

        print("="*60)
        print("BULK TAGGING LESSONS")
        print("="*60)

        # Get pentest lessons 11-30
        print("\n1. Finding pentest lessons (order_index 11-30)...")
        cursor.execute("""
            SELECT lesson_id, title, order_index
            FROM lessons
            WHERE domain = 'pentest' AND order_index BETWEEN 11 AND 30
            ORDER BY order_index
        """)
        pentest_lessons = cursor.fetchall()

        print(f"   Found {len(pentest_lessons)} pentest lessons")

        # Get red_team lessons 52-56
        print("\n2. Finding red_team lessons (order_index 52-56)...")
        cursor.execute("""
            SELECT lesson_id, title, order_index
            FROM lessons
            WHERE domain = 'red_team' AND order_index BETWEEN 52 AND 56
            ORDER BY order_index
        """)
        redteam_lessons = cursor.fetchall()

        print(f"   Found {len(redteam_lessons)} red_team lessons")

        # Tag pentest lessons with PEN-200
        print("\n3. Tagging pentest lessons with 'Course: PEN-200'...")
        now = datetime.utcnow().isoformat()
        tagged_count = 0
        skipped_count = 0

        for lesson_id, title, order_index in pentest_lessons:
            # Check if already tagged
            cursor.execute("""
                SELECT 1 FROM lesson_tags
                WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, pen200_tag_id))

            if cursor.fetchone():
                print(f"   → Lesson {order_index}: {title[:50]} (already tagged)")
                skipped_count += 1
            else:
                cursor.execute("""
                    INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                    VALUES (?, ?, ?)
                """, (lesson_id, pen200_tag_id, now))
                print(f"   ✓ Lesson {order_index}: {title[:50]}")
                tagged_count += 1

        print(f"\n   Tagged: {tagged_count}, Skipped (already tagged): {skipped_count}")

        # Tag red_team lessons with APT
        print("\n4. Tagging red_team lessons with 'APT'...")
        tagged_count = 0
        skipped_count = 0

        for lesson_id, title, order_index in redteam_lessons:
            # Check if already tagged
            cursor.execute("""
                SELECT 1 FROM lesson_tags
                WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, apt_tag_id))

            if cursor.fetchone():
                print(f"   → Lesson {order_index}: {title[:50]} (already tagged)")
                skipped_count += 1
            else:
                cursor.execute("""
                    INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                    VALUES (?, ?, ?)
                """, (lesson_id, apt_tag_id, now))
                print(f"   ✓ Lesson {order_index}: {title[:50]}")
                tagged_count += 1

        print(f"\n   Tagged: {tagged_count}, Skipped (already tagged): {skipped_count}")

        conn.commit()

        print("\n" + "="*60)
        print("✅ BULK TAGGING COMPLETED!")
        print("="*60)
        print("\nSummary:")
        print(f"  • Pentest lessons (11-30): Tagged with 'Course: PEN-200'")
        print(f"  • Red Team lessons (52-56): Tagged with 'APT'")
        print("\nRefresh the app to see the new tags!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during bulk tagging: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    bulk_tag_lessons()
