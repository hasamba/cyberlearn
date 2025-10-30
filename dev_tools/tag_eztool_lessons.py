"""
Tag Eric Zimmerman Tools lessons with the 'Package: Eric Zimmerman Tools' tag.

This script tags DFIR lessons 11-24 which are all Eric Zimmerman forensic tools:
- AmcacheParser
- AppCompatCacheParser
- bstrings
- EvtxECmd
- JLECmd
- LECmd
- MFTECmd
- PECmd
- RBCmd
- RECmd
- SBECmd
- SQLECmd
- WxTCmd
- Timeline Explorer

Usage:
    python dev_tools/tag_eztool_lessons.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def tag_eztool_lessons():
    """Tag Eric Zimmerman Tools lessons."""

    db_path = Path(__file__).parent.parent / "cyberlearn.db"

    if not db_path.exists():
        print(f"[ERROR] Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if the Eric Zimmerman Tools tag exists
        cursor.execute("SELECT tag_id, name FROM tags WHERE name = 'Package: Eric Zimmerman Tools'")
        tag_result = cursor.fetchone()

        if not tag_result:
            print("[ERROR] Tag 'Package: Eric Zimmerman Tools' not found in database")
            print("   Please run add_tags_system.py first to create system tags")
            return

        ez_tag_id = tag_result[0]

        print("="*70)
        print("TAGGING ERIC ZIMMERMAN TOOLS LESSONS")
        print("="*70)

        # Get DFIR lessons 11-24 (all Eric Zimmerman tools)
        print("\nFinding DFIR lessons (order_index 11-24)...")
        cursor.execute("""
            SELECT lesson_id, title, order_index
            FROM lessons
            WHERE domain = 'dfir' AND order_index BETWEEN 11 AND 24
            ORDER BY order_index
        """)
        ez_lessons = cursor.fetchall()

        print(f"Found {len(ez_lessons)} Eric Zimmerman Tools lessons\n")

        if len(ez_lessons) == 0:
            print("[WARN] No lessons found. Please load the lessons into the database first:")
            print("   python load_all_lessons.py")
            return

        # Tag each lesson
        now = datetime.utcnow().isoformat()
        tagged_count = 0
        skipped_count = 0

        for lesson_id, title, order_index in ez_lessons:
            # Check if already tagged
            cursor.execute("""
                SELECT 1 FROM lesson_tags
                WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, ez_tag_id))

            if cursor.fetchone():
                print(f"   [SKIP] Lesson {order_index:2d}: {title[:60]} (already tagged)")
                skipped_count += 1
            else:
                cursor.execute("""
                    INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                    VALUES (?, ?, ?)
                """, (lesson_id, ez_tag_id, now))
                print(f"   [OK] Lesson {order_index:2d}: {title[:60]}")
                tagged_count += 1

        conn.commit()

        print("\n" + "="*70)
        print("[SUCCESS] TAGGING COMPLETED!")
        print("="*70)
        print(f"\nSummary:")
        print(f"  - Total lessons found: {len(ez_lessons)}")
        print(f"  - Newly tagged: {tagged_count}")
        print(f"  - Already tagged: {skipped_count}")
        print(f"\nAll DFIR lessons (11-24) now tagged with 'Package: Eric Zimmerman Tools'")
        print("\nRefresh the app to see the new tags!")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Error during tagging: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    tag_eztool_lessons()
