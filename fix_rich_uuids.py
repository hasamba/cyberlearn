"""
Fix UUID issues in rich lesson files
Converts all string IDs to proper UUIDs
"""

import json
import uuid
from pathlib import Path

def fix_lesson_uuids(filepath):
    """Fix all UUID fields in a lesson file"""

    print(f"Fixing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    # Fix lesson_id
    if not is_valid_uuid(lesson.get('lesson_id')):
        lesson['lesson_id'] = str(uuid.uuid4())
        print(f"  [OK] Fixed lesson_id")

    # Fix block_ids in content_blocks
    for block in lesson.get('content_blocks', []):
        if 'block_id' in block and not is_valid_uuid(block['block_id']):
            block['block_id'] = str(uuid.uuid4())

    print(f"  [OK] Fixed {len(lesson.get('content_blocks', []))} block_ids")

    # Save fixed lesson
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Saved fixed version")
    return True


def is_valid_uuid(val):
    """Check if string is a valid UUID"""
    if not isinstance(val, str):
        return False
    try:
        uuid.UUID(val)
        return True
    except:
        return False


def main():
    print("=" * 60)
    print("Fixing UUID Issues in Rich Lessons")
    print("=" * 60)
    print()

    # Find all _RICH lesson files
    content_dir = Path('content')
    rich_files = list(content_dir.glob('*_RICH.json'))

    if not rich_files:
        print("No _RICH files found")
        return

    print(f"Found {len(rich_files)} rich lesson files\n")

    for filepath in rich_files:
        try:
            fix_lesson_uuids(filepath)
            print()
        except Exception as e:
            print(f"  [ERROR] {e}")
            print()

    print("=" * 60)
    print("[SUCCESS] All UUID issues fixed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python load_all_lessons.py")
    print("2. Run: python check_database.py reset yourusername")
    print("3. Run: streamlit run app.py")


if __name__ == "__main__":
    main()
