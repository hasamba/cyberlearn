"""
Debug script to verify tag data in database
Run this on the VM to check tag status
"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "cyberlearn.db"

if not db_path.exists():
    print(f"ERROR: Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("TAG SYSTEM DEBUG REPORT")
print("=" * 60)

# Check if tags table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
if not cursor.fetchone():
    print("\nERROR: 'tags' table does not exist!")
    print("Run the tag system migration script first.")
    conn.close()
    exit(1)

# Check if lesson_tags table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lesson_tags'")
if not cursor.fetchone():
    print("\nERROR: 'lesson_tags' table does not exist!")
    print("Run the tag system migration script first.")
    conn.close()
    exit(1)

print("\n[OK] Both tables exist")

# Count tags
cursor.execute("SELECT COUNT(*) FROM tags")
tag_count = cursor.fetchone()[0]
print(f"\nTotal tags in database: {tag_count}")

# List all tags
cursor.execute("SELECT name, color FROM tags ORDER BY name")
tags = cursor.fetchall()
print("\nAll tags:")
for tag in tags:
    name, color = tag
    print(f"  - {name} ({color})")

# Count lesson_tags entries
cursor.execute("SELECT COUNT(*) FROM lesson_tags")
lt_count = cursor.fetchone()[0]
print(f"\nTotal lesson_tags entries: {lt_count}")

# Count lessons with tags
cursor.execute("SELECT COUNT(DISTINCT lesson_id) FROM lesson_tags")
lessons_with_tags = cursor.fetchone()[0]
print(f"Lessons with at least one tag: {lessons_with_tags}")

# Count total lessons
cursor.execute("SELECT COUNT(*) FROM lessons")
total_lessons = cursor.fetchone()[0]
print(f"Total lessons in database: {total_lessons}")

# Calculate coverage
if total_lessons > 0:
    coverage = (lessons_with_tags / total_lessons) * 100
    print(f"Tag coverage: {coverage:.1f}%")

# Check Built-In tag specifically
cursor.execute("SELECT tag_id FROM tags WHERE name = 'Built-In'")
builtin_tag = cursor.fetchone()
if builtin_tag:
    builtin_id = builtin_tag[0]
    cursor.execute("SELECT COUNT(*) FROM lesson_tags WHERE tag_id = ?", (builtin_id,))
    builtin_count = cursor.fetchone()[0]
    print(f"\nLessons with 'Built-In' tag: {builtin_count}")
else:
    print("\nWARNING: 'Built-In' tag not found!")

# Sample 5 lessons with their tags
print("\n" + "=" * 60)
print("SAMPLE: First 5 lessons with their tags")
print("=" * 60)

cursor.execute("""
    SELECT l.lesson_id, l.title, l.domain
    FROM lessons l
    ORDER BY l.order_index
    LIMIT 5
""")

for lesson in cursor.fetchall():
    lesson_id, title, domain = lesson
    print(f"\n{title}")
    print(f"  Domain: {domain}")
    print(f"  ID: {lesson_id}")

    cursor.execute("""
        SELECT t.name
        FROM lesson_tags lt
        JOIN tags t ON lt.tag_id = t.tag_id
        WHERE lt.lesson_id = ?
    """, (lesson_id,))

    lesson_tags = cursor.fetchall()
    if lesson_tags:
        print(f"  Tags ({len(lesson_tags)}):")
        for tag in lesson_tags:
            print(f"    - {tag[0]}")
    else:
        print("  Tags: NONE (ERROR!)")

print("\n" + "=" * 60)

# Check new domains in users table
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
new_domains = ['ai_security', 'iot_security', 'web3_security']
print("\nNew domain columns in users table:")
for domain in new_domains:
    status = "[OK] EXISTS" if domain in columns else "[X] MISSING"
    print(f"  {domain}: {status}")

conn.close()

print("\n" + "=" * 60)
print("Debug report complete.")
print("=" * 60)
