"""
Tag all lessons without tags as "Built-In"

This ensures all lessons have at least one tag for better organization and filtering.
Lessons that are already part of a course or package will keep their existing tags.
"""

import sqlite3
from datetime import datetime

def tag_builtin_lessons(db_path: str = "cyberlearn.db"):
    """Tag all untagged lessons with Built-In tag"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get the Built-In tag
        cursor.execute("SELECT tag_id FROM tags WHERE name = 'Built-In'")
        builtin_tag = cursor.fetchone()

        if not builtin_tag:
            print("[ERROR] Built-In tag not found in database")
            print("Please ensure tags are initialized")
            return

        builtin_tag_id = builtin_tag[0]

        # Find all lessons without any tags
        cursor.execute("""
            SELECT l.lesson_id, l.title, l.domain
            FROM lessons l
            WHERE NOT EXISTS (
                SELECT 1 FROM lesson_tags lt
                WHERE lt.lesson_id = l.lesson_id
            )
            ORDER BY l.domain, l.order_index
        """)

        untagged_lessons = cursor.fetchall()

        if not untagged_lessons:
            print("[INFO] All lessons already have tags")
            return

        print(f"[INFO] Found {len(untagged_lessons)} lessons without tags\n")

        # Tag each untagged lesson
        now = datetime.utcnow().isoformat()
        tagged_count = 0

        for lesson_id, title, domain in untagged_lessons:
            cursor.execute("""
                INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                VALUES (?, ?, ?)
            """, (lesson_id, builtin_tag_id, now))
            tagged_count += 1

            if tagged_count <= 10:  # Show first 10
                print(f"  [{domain:20s}] {title[:60]}")

        if tagged_count > 10:
            print(f"  ... and {tagged_count - 10} more lessons")

        conn.commit()

        print(f"\n[SUCCESS] Tagged {tagged_count} lessons as 'Built-In'")

        # Verify final counts
        cursor.execute("""
            SELECT COUNT(DISTINCT lesson_id) FROM lesson_tags
        """)
        tagged_lessons = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lessons")
        total_lessons = cursor.fetchone()[0]

        print(f"\n=== Final Status ===")
        print(f"Total lessons: {total_lessons}")
        print(f"Tagged lessons: {tagged_lessons}")
        print(f"Untagged lessons: {total_lessons - tagged_lessons}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[ERROR] Tagging failed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    print("=== Tagging Built-In Lessons ===\n")
    tag_builtin_lessons()
    print("\n=== Complete ===")
