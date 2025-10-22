"""
Load all lessons from content directory into database
"""

import json
import os
from uuid import UUID
from pathlib import Path
from utils.database import Database
from models.lesson import Lesson

def load_all_lessons():
    """Load all lesson JSON files from content directory"""

    db = Database()
    content_dir = Path("content")

    lesson_files = list(content_dir.glob("lesson_*.json"))

    if not lesson_files:
        print("❌ No lesson files found in content/ directory")
        print("   Files should be named: lesson_*.json")
        return

    print(f"📚 Found {len(lesson_files)} lesson files")
    print("=" * 60)

    loaded = 0
    skipped = 0
    errors = 0

    for lesson_file in sorted(lesson_files):
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert lesson_id to UUID, but keep prerequisites as strings
            data['lesson_id'] = UUID(data['lesson_id'])
            # Prerequisites should remain as strings (as per model definition)
            data['prerequisites'] = [str(p) for p in data['prerequisites']]

            # Create lesson
            lesson = Lesson(**data)

            if db.create_lesson(lesson):
                print(f"✅ Loaded: {lesson.title}")
                loaded += 1
            else:
                print(f"⏭️  Skipped (already exists): {lesson.title}")
                skipped += 1

        except Exception as e:
            print(f"❌ Error loading {lesson_file.name}: {e}")
            errors += 1

    db.close()

    print("=" * 60)
    print(f"✅ Loaded: {loaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total lessons in database: {loaded + skipped}")


if __name__ == "__main__":
    load_all_lessons()
