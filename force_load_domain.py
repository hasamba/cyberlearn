#!/usr/bin/env python3
"""
Force reload lessons for a specific domain into database.
This script deletes existing lessons for a domain and reloads them from JSON files.

Usage:
    python force_load_domain.py osint
    python force_load_domain.py threat_hunting
"""

import json
import sqlite3
import sys
from pathlib import Path
from models.lesson import Lesson

def delete_domain_lessons(domain):
    """Delete all existing lessons for a domain from database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    # Check how many lessons exist
    cursor.execute("SELECT COUNT(*) FROM lessons WHERE domain=?", (domain,))
    count = cursor.fetchone()[0]
    print(f"Found {count} existing {domain} lessons in database")

    if count > 0:
        # Delete them
        cursor.execute("DELETE FROM lessons WHERE domain=?", (domain,))
        conn.commit()
        print(f"Deleted {count} {domain} lessons")
    else:
        print(f"No {domain} lessons to delete")

    conn.close()

def load_domain_lessons(domain):
    """Load lessons for a domain from JSON files"""
    content_dir = Path(__file__).parent / "content"

    # Handle both underscore and no underscore in filenames
    patterns = [
        f"lesson_{domain}_*_RICH.json",
        f"lesson_{domain.replace('_', '')}_*_RICH.json"
    ]

    lesson_files = []
    for pattern in patterns:
        lesson_files.extend(content_dir.glob(pattern))

    lesson_files = sorted(set(lesson_files))  # Remove duplicates

    print(f"\nFound {len(lesson_files)} {domain} lesson files")

    if len(lesson_files) == 0:
        print(f"⚠ No lesson files found for domain '{domain}'")
        print(f"   Searched for patterns: {patterns}")
        return 0, 0

    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    loaded = 0
    errors = 0

    for filepath in lesson_files:
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
                (str(lesson.lesson_id),)  # Convert UUID to string
            )
            if cursor.fetchone():
                print(f"  ⚠ Already exists, skipping")
                continue

            # Insert into database (convert UUID to string)
            cursor.execute("""
                INSERT INTO lessons (
                    lesson_id, domain, title, difficulty, order_index,
                    prerequisites, concepts, estimated_time, learning_objectives,
                    content_blocks, post_assessment, jim_kwik_principles, mitre_attack_tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(lesson.lesson_id),  # Convert UUID to string
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

def verify_domain_lessons(domain):
    """Verify lessons for a domain in database"""
    conn = sqlite3.connect('cyberlearn.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lesson_id, title, difficulty, order_index
        FROM lessons
        WHERE domain=?
        ORDER BY order_index
    """, (domain,))

    lessons = cursor.fetchall()

    print(f"\n{'='*60}")
    print(f"{domain.upper()} Lessons in Database: {len(lessons)}")
    print(f"{'='*60}")

    if lessons:
        for lesson_id, title, difficulty, order_index in lessons:
            print(f"{order_index}. {title} (difficulty: {difficulty})")
            print(f"   ID: {lesson_id}")
    else:
        print(f"⚠ No {domain} lessons found")

    conn.close()
    return len(lessons)

def main():
    if len(sys.argv) < 2:
        print("Usage: python force_load_domain.py <domain>")
        print("\nExamples:")
        print("  python force_load_domain.py osint")
        print("  python force_load_domain.py threat_hunting")
        print("  python force_load_domain.py blueteam")
        sys.exit(1)

    domain = sys.argv[1]

    print("="*60)
    print(f"Force Reload {domain.upper()} Lessons")
    print("="*60)

    # Step 1: Delete existing lessons
    print(f"\nStep 1: Deleting existing {domain} lessons...")
    delete_domain_lessons(domain)

    # Step 2: Load lessons from files
    print(f"\nStep 2: Loading {domain} lessons from JSON files...")
    loaded, errors = load_domain_lessons(domain)

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Loaded: {loaded}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")

    # Step 3: Verify
    print(f"\nStep 3: Verifying {domain} lessons in database...")
    count = verify_domain_lessons(domain)

    if loaded > 0 and count > 0:
        print(f"\n✓ Success! {loaded} {domain} lessons loaded into database")
        print("\nNext steps:")
        print("  1. Restart Streamlit: streamlit run app.py")
        print(f"  2. Go to My Learning → {domain.replace('_', ' ').title()} tab")
        print("  3. Verify all lessons appear")
    elif count == 0 and loaded == 0 and errors == 0:
        print(f"\n⚠ No lesson files found for domain '{domain}'")
        print(f"   Create lesson files first: content/lesson_{domain}_*_RICH.json")
    else:
        print("\n✗ No lessons were loaded. Check validation errors above.")

if __name__ == "__main__":
    main()
