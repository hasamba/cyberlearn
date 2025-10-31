"""
Create Package: OWASP AI Top 10 tag and tag all OWASP LLM lessons
"""

import sqlite3
from datetime import datetime

def tag_owasp_lessons(db_path: str = "cyberlearn.db"):
    """Create OWASP AI Top 10 tag and tag lessons"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("TAGGING OWASP AI TOP 10 LESSONS")
    print("=" * 60)

    # Step 1: Check if tag exists
    cursor.execute("SELECT tag_id FROM tags WHERE name = ?", ("Package: OWASP AI Top 10",))
    tag = cursor.fetchone()

    if tag:
        tag_id = tag[0]
        print(f"\n[OK] Tag already exists: Package: OWASP AI Top 10")
    else:
        # Create the tag
        tag_id = 18  # Next available ID after 17 existing tags
        cursor.execute('''
            INSERT INTO tags (tag_id, name, color, icon, description, is_system, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tag_id,
            "Package: OWASP AI Top 10",
            "#F59E0B",  # Orange/amber color
            "🔶",
            "OWASP LLM Top 10 security vulnerabilities for AI applications",
            1,  # System tag
            datetime.now().isoformat()
        ))
        print(f"\n[CREATED] Tag: Package: OWASP AI Top 10 (ID: {tag_id})")

    # Step 2: Find all OWASP LLM lessons
    cursor.execute('''
        SELECT lesson_id, title
        FROM lessons
        WHERE title LIKE '%OWASP LLM%'
        ORDER BY order_index
    ''')

    owasp_lessons = cursor.fetchall()
    print(f"\n[FOUND] {len(owasp_lessons)} OWASP LLM lessons:")

    # Step 3: Tag each lesson
    tagged_count = 0
    for lesson_id, title in owasp_lessons:
        # Check if already tagged
        cursor.execute('''
            SELECT 1 FROM lesson_tags
            WHERE lesson_id = ? AND tag_id = ?
        ''', (lesson_id, tag_id))

        if cursor.fetchone():
            print(f"  [SKIP] {title}")
        else:
            cursor.execute('''
                INSERT INTO lesson_tags (lesson_id, tag_id, added_at)
                VALUES (?, ?, ?)
            ''', (lesson_id, tag_id, datetime.now().isoformat()))
            print(f"  [TAG] {title}")
            tagged_count += 1

    conn.commit()

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Tagged {tagged_count} lessons")
    print("=" * 60)
    print(f"\nAll {len(owasp_lessons)} OWASP LLM lessons now have:")
    print(f"  - Package: OWASP AI Top 10 tag")
    print()

    conn.close()

if __name__ == "__main__":
    import sys
    tag_owasp_lessons()
    sys.exit(0)
