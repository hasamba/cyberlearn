#!/usr/bin/env python3
"""
Regenerate UUIDs for OSINT lessons.

The OSINT lessons currently have UUIDs that conflict with existing lessons
in the database. This script generates new unique UUIDs for each OSINT lesson.
"""

import json
import uuid
from pathlib import Path

def regenerate_osint_uuids():
    """Regenerate UUIDs for all OSINT lesson files"""
    content_dir = Path(__file__).parent / "content"
    osint_files = sorted(content_dir.glob("lesson_osint_*_RICH.json"))

    print("="*60)
    print("Regenerating OSINT Lesson UUIDs")
    print("="*60)

    if not osint_files:
        print("No OSINT lesson files found!")
        return

    print(f"\nFound {len(osint_files)} OSINT lesson files\n")

    for filepath in osint_files:
        print(f"Processing: {filepath.name}")

        # Read lesson
        with open(filepath, 'r', encoding='utf-8') as f:
            lesson = json.load(f)

        # Store old UUID
        old_uuid = lesson['lesson_id']
        print(f"  Old UUID: {old_uuid}")

        # Generate new UUID
        new_uuid = str(uuid.uuid4())
        lesson['lesson_id'] = new_uuid
        print(f"  New UUID: {new_uuid}")

        # Also regenerate UUIDs for post_assessment questions
        if 'post_assessment' in lesson:
            for i, qa in enumerate(lesson['post_assessment']):
                if 'question_id' in qa:
                    old_q_uuid = qa['question_id']
                    new_q_uuid = str(uuid.uuid4())
                    qa['question_id'] = new_q_uuid
                    print(f"  Question {i+1} UUID: {old_q_uuid} -> {new_q_uuid}")

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)

        print(f"  [OK] Updated: {filepath.name}\n")

    print("="*60)
    print("[SUCCESS] All OSINT lesson UUIDs regenerated!")
    print("\nNext steps:")
    print("  1. Commit the changes: git add content/ && git commit -m 'Regenerate OSINT UUIDs'")
    print("  2. Push to remote: git push")
    print("  3. On VM: git pull")
    print("  4. On VM: python force_load_osint.py")
    print("="*60)

def main():
    regenerate_osint_uuids()

if __name__ == "__main__":
    main()
