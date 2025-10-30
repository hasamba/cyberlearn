"""
Add 13Cubed course tags and tag DFIR lessons appropriately.

- Course: 13Cubed-Investigating Windows Memory (DFIR 11-41)
- Course: 13Cubed-Investigating Windows Endpoints (DFIR 42-70)
"""

import sqlite3
from pathlib import Path
import uuid
from datetime import datetime

def add_13cubed_tags():
    """Add 13Cubed course tags and tag lessons"""

    db_path = Path(__file__).parent / "cyberlearn.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("=" * 70)
        print("ADDING 13CUBED COURSE TAGS")
        print("=" * 70)

        # Create the two 13Cubed course tags
        tags_to_add = [
            {
                "name": "Course: 13Cubed-Investigating Windows Memory",
                "color": "#10B981",  # Green
                "icon": "🧠",
                "description": "13Cubed Windows Memory Forensics course lessons"
            },
            {
                "name": "Course: 13Cubed-Investigating Windows Endpoints",
                "color": "#8B5CF6",  # Purple
                "icon": "💻",
                "description": "13Cubed Windows Endpoint Investigation course lessons"
            }
        ]

        now = datetime.utcnow().isoformat()
        tag_ids = {}

        for tag_info in tags_to_add:
            tag_id = str(uuid.uuid4())
            try:
                cursor.execute("""
                    INSERT INTO tags (tag_id, name, color, icon, description, created_at, is_system)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (tag_id, tag_info["name"], tag_info["color"], tag_info["icon"], tag_info["description"], now))

                tag_ids[tag_info["name"]] = tag_id
                print(f"[OK] Added: {tag_info['name']}")
            except sqlite3.IntegrityError:
                # Tag already exists, get its ID
                cursor.execute("SELECT tag_id FROM tags WHERE name = ?", (tag_info["name"],))
                tag_ids[tag_info["name"]] = cursor.fetchone()[0]
                print(f"[SKIP] Already exists: {tag_info['name']}")

        conn.commit()

        # Tag DFIR lessons 11-41 with Windows Memory course
        print("\n" + "=" * 70)
        print("TAGGING DFIR LESSONS 11-41 (Windows Memory)")
        print("=" * 70)

        memory_tag_id = tag_ids["Course: 13Cubed-Investigating Windows Memory"]
        cursor.execute("""
            SELECT lesson_id, title, order_index FROM lessons
            WHERE domain = 'dfir' AND order_index BETWEEN 11 AND 41
            ORDER BY order_index
        """)
        memory_lessons = cursor.fetchall()

        tagged_count = 0
        for lesson_id, title, order_index in memory_lessons:
            cursor.execute("""
                SELECT 1 FROM lesson_tags WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, memory_tag_id))

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                    VALUES (?, ?, ?)
                """, (lesson_id, memory_tag_id, now))
                tagged_count += 1

        print(f"[OK] Tagged {tagged_count} lessons with Windows Memory course")

        # Tag DFIR lessons 42-70 with Windows Endpoints course
        print("\n" + "=" * 70)
        print("TAGGING DFIR LESSONS 42-70 (Windows Endpoints)")
        print("=" * 70)

        endpoints_tag_id = tag_ids["Course: 13Cubed-Investigating Windows Endpoints"]
        cursor.execute("""
            SELECT lesson_id, title, order_index FROM lessons
            WHERE domain = 'dfir' AND order_index BETWEEN 42 AND 70
            ORDER BY order_index
        """)
        endpoints_lessons = cursor.fetchall()

        tagged_count = 0
        for lesson_id, title, order_index in endpoints_lessons:
            cursor.execute("""
                SELECT 1 FROM lesson_tags WHERE lesson_id = ? AND tag_id = ?
            """, (lesson_id, endpoints_tag_id))

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                    VALUES (?, ?, ?)
                """, (lesson_id, endpoints_tag_id, now))
                tagged_count += 1

        print(f"[OK] Tagged {tagged_count} lessons with Windows Endpoints course")

        conn.commit()

        # Summary
        cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM lesson_tags lt
            JOIN tags t ON lt.tag_id = t.tag_id
            WHERE t.name LIKE 'Course: 13Cubed%'
        """)
        total_tagged = cursor.fetchone()[0]

        print("\n" + "=" * 70)
        print("[SUCCESS] 13CUBED TAGGING COMPLETE")
        print("=" * 70)
        print(f"Total tags in database: {total_tags}")
        print(f"Total lessons tagged with 13Cubed courses: {total_tagged}")
        print(f"  - Windows Memory (11-41): {len(memory_lessons)}")
        print(f"  - Windows Endpoints (42-70): {len(endpoints_lessons)}")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_13cubed_tags()
