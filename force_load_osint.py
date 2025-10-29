#!/usr/bin/env python3
"""
Force reload OSINT lessons into database.
This script deletes existing OSINT lessons and reloads them from JSON files.
"""

import json
import sqlite3
from pathlib import Path
from models.lesson import Lesson

def delete_osint_lessons():
    """Delete all existing OSINT lessons from database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Check how many OSINT lessons exist
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain='osint'")
    count = cursor.fetchone()[0]
    print(f"Found {count} existing OSINT lessons in database")

    if count > 0:
        # Delete them
        cursor.execute("DELETE FROM lessons WHERE domain='osint'")
        conn.commit()
        print(f"Deleted {count} OSINT lessons")
    else:
        print("No OSINT lessons to delete")

    conn.close()

def load_osint_lessons():
    """Load OSINT lessons from JSON files"""
    content_dir = Path(__file__).parent / "content"
    osint_files = sorted(content_dir.glob("lesson_osint_*_RICH.json"))

    print(f"\nFound {len(osint_files)} OSINT lesson files")

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    loaded = 0
    errors = 0

    for filepath in osint_files:
        try:
            print(f"\nProcessing: {filepath.name}")

            # Read JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson_data = json.load(f)

            # Validate with Pydantic
            try:
                lesson = Lesson(**lesson_data)
                print(f"  ✓ Validated: {lesson.title}")
            except Exception as e:
                print(f"  ✗ Validation error: {e}")
                errors += 1
                continue

            # Check if already exists
            cursor.execute(
                "SELECT lesson_id FROM lessons WHERE lesson_id = ?",
                (lesson.lesson_id,)
            )
            if cursor.fetchone():
                print(f"  ⚠ Already exists, skipping")
                continue

            # Insert into database
            cursor.execute("""
                INSERT INTO lessons (
                    lesson_id, domain, title, difficulty, order_index,
                    prerequisites, concepts, estimated_time, learning_objectives,
                    content_blocks, post_assessment, jim_kwik_principles, mitre_attack_tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lesson.lesson_id,
                lesson.domain,
                lesson.title,
                lesson.difficulty,
                lesson.order_index,
                json.dumps(lesson.prerequisites),
                json.dumps(lesson.concepts),
                lesson.estimated_time,
                json.dumps(lesson.learning_objectives),
                json.dumps([block.model_dump() for block in lesson.content_blocks]),
                json.dumps([qa.model_dump() for qa in lesson.post_assessment]),
                json.dumps(lesson.jim_kwik_principles),
                json.dumps(lesson.mitre_attack_tags) if lesson.mitre_attack_tags else None
            ))

            conn.commit()
            print(f"  ✓ Loaded into database")
            loaded += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")
            errors += 1

    conn.close()

    return loaded, errors

def verify_osint_lessons():
    """Verify OSINT lessons in database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lesson_id, title, difficulty, order_index
        FROM lessons
        WHERE domain='osint'
        ORDER BY order_index
    """)

    lessons = cursor.fetchall()

    print(f"\n{'='*60}")
    print(f"OSINT Lessons in Database: {len(lessons)}")
    print(f"{'='*60}")

    if lessons:
        for lesson_id, title, difficulty, order_index in lessons:
            print(f"{order_index}. {title} (difficulty: {difficulty})")
            print(f"   ID: {lesson_id}")
    else:
        print("⚠ No OSINT lessons found")

    conn.close()

def main():
    print("="*60)
    print("Force Reload OSINT Lessons")
    print("="*60)

    # Step 1: Delete existing OSINT lessons
    print("\nStep 1: Deleting existing OSINT lessons...")
    delete_osint_lessons()

    # Step 2: Load OSINT lessons from files
    print("\nStep 2: Loading OSINT lessons from JSON files...")
    loaded, errors = load_osint_lessons()

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Loaded: {loaded}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")

    # Step 3: Verify
    print("\nStep 3: Verifying OSINT lessons in database...")
    verify_osint_lessons()

    if loaded > 0:
        print(f"\n✓ Success! {loaded} OSINT lessons loaded into database")
        print("\nNext steps:")
        print("  1. Restart Streamlit: streamlit run app.py")
        print("  2. Go to My Learning → OSINT tab")
        print("  3. Verify all lessons appear")
    else:
        print("\n✗ No lessons were loaded. Check validation errors above.")

if __name__ == "__main__":
    main()
